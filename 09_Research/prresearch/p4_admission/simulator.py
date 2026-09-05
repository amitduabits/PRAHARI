"""Paper 4: deterministic concurrent decoder management.

Mirrors app/services/sessions.py::start, which refuses a new decoder session
once MAX_OPEN_CAPTURES is reached: no queue, no eviction, no quality drop. The
simulator compares that policy against the three alternatives a systems
reviewer will ask about, on the same arrival stream.

Policies
    refuse    the deployed policy: reject immediately when at the bound
    queue     unbounded FIFO wait for a free decoder
    evict     admit always, evict the least-recently-used session
    degrade   admit always, but every extra session slows all of them down

The single event loop is deterministic given the seed, so p50 and p99 latency
figures are reproducible across machines.
"""

from __future__ import annotations

import heapq
from dataclasses import dataclass
from typing import Literal

from prresearch.seeds import rng

Policy = Literal["refuse", "queue", "evict", "degrade"]


@dataclass
class Request:
    req_id: int
    camera_id: str
    arrival: float
    service: float          # decoder-seconds needed at nominal speed


@dataclass
class Outcome:
    req_id: int
    admitted: bool
    start: float | None
    finish: float | None
    evicted: bool = False
    wait: float = 0.0


def generate_arrivals(n: int, rate_per_s: float, mean_service_s: float, seed_name: str) -> list[Request]:
    g = rng(seed_name)
    t = 0.0
    reqs = []
    ids = g.integers(0, 80000, size=n)
    for i in range(n):
        t += float(g.exponential(1.0 / rate_per_s))
        service = float(g.gamma(shape=2.0, scale=mean_service_s / 2.0))
        reqs.append(Request(i, f"CAM{int(ids[i]):05d}", t, max(service, 0.05)))
    return reqs


def simulate(requests: list[Request], capacity: int, policy: Policy) -> dict:
    """One deterministic event loop. Returns aggregate metrics."""
    running: list[tuple[float, int]] = []      # (finish_time, req_id) min-heap
    lru: dict[int, float] = {}                 # req_id -> last activity
    waiting: list[Request] = []
    admitted, refused, evicted = 0, 0, 0
    latencies: list[float] = []
    waits: list[float] = []
    peak = 0
    area = 0.0
    last_t = 0.0

    def retire(now: float) -> None:
        while running and running[0][0] <= now:
            _, rid = heapq.heappop(running)
            lru.pop(rid, None)

    def concurrency_factor(k: int) -> float:
        if policy != "degrade":
            return 1.0
        return max(1.0, k / capacity)   # extra sessions slow everyone down

    for req in requests:
        now = req.arrival
        area += len(running) * (now - last_t)
        last_t = now
        retire(now)
        peak = max(peak, len(running))

        if policy == "queue":
            # Drain anything whose decoder freed before this arrival.
            while waiting and len(running) < capacity:
                w = waiting.pop(0)
                start = max(w.arrival, now)
                fin = start + w.service
                heapq.heappush(running, (fin, w.req_id))
                lru[w.req_id] = start
                latencies.append(fin - w.arrival)
                waits.append(start - w.arrival)
                admitted += 1

        if len(running) < capacity:
            k = len(running) + 1
            fin = now + req.service * concurrency_factor(k)
            heapq.heappush(running, (fin, req.req_id))
            lru[req.req_id] = now
            latencies.append(fin - now)
            waits.append(0.0)
            admitted += 1
            peak = max(peak, len(running))
            continue

        if policy == "refuse":
            refused += 1
        elif policy == "queue":
            waiting.append(req)
        elif policy == "evict":
            victim = min(lru, key=lru.get)
            running[:] = [x for x in running if x[1] != victim]
            heapq.heapify(running)
            lru.pop(victim, None)
            evicted += 1
            fin = now + req.service
            heapq.heappush(running, (fin, req.req_id))
            lru[req.req_id] = now
            latencies.append(fin - now)
            waits.append(0.0)
            admitted += 1
        elif policy == "degrade":
            k = len(running) + 1
            fin = now + req.service * concurrency_factor(k)
            heapq.heappush(running, (fin, req.req_id))
            lru[req.req_id] = now
            latencies.append(fin - now)
            waits.append(0.0)
            admitted += 1
            peak = max(peak, len(running))

    # Drain the queue at the end so the queue policy is not credited for work
    # it never finished.
    while waiting:
        w = waiting.pop(0)
        retire(last_t)
        start = max(w.arrival, running[0][0] if running else last_t)
        fin = start + w.service
        heapq.heappush(running, (fin, w.req_id))
        latencies.append(fin - w.arrival)
        waits.append(start - w.arrival)
        admitted += 1
        last_t = start

    import numpy as np

    lat = np.asarray(latencies, dtype=float)
    wt = np.asarray(waits, dtype=float)
    n = len(requests)
    return {
        "policy": policy,
        "capacity": capacity,
        "requests": n,
        "admitted": admitted,
        "refused": refused,
        "evicted": evicted,
        "refusal_rate": refused / n,
        "peak_concurrent_decoders": peak,
        "mean_concurrency": area / (last_t or 1.0),
        "p50_latency_s": float(np.percentile(lat, 50)) if lat.size else float("nan"),
        "p99_latency_s": float(np.percentile(lat, 99)) if lat.size else float("nan"),
        "max_latency_s": float(lat.max()) if lat.size else float("nan"),
        "p99_wait_s": float(np.percentile(wt, 99)) if wt.size else 0.0,
    }


class ThreeStrikeHealth:
    """Health hysteresis from app/services/health_probe.py.

    A camera is marked offline only after three consecutive probe failures, and
    offline cameras are skipped by the sweep. That is what keeps a flapping
    estate from consuming the whole decoder budget.
    """

    def __init__(self, strikes: int = 3) -> None:
        self.strikes = strikes
        self.fail_count: dict[str, int] = {}
        self.health: dict[str, str] = {}

    def observe(self, camera_id: str, ok: bool) -> str:
        if ok:
            self.fail_count[camera_id] = 0
            self.health[camera_id] = "live"
        else:
            n = self.fail_count.get(camera_id, 0) + 1
            self.fail_count[camera_id] = n
            self.health[camera_id] = "offline" if n >= self.strikes else self.health.get(camera_id, "unknown")
        return self.health[camera_id]

    def eligible(self, camera_ids: list[str]) -> list[str]:
        return [c for c in camera_ids if self.health.get(c) != "offline"]


def rotational_sweep(
    n_cameras: int,
    capacity: int,
    probe_seconds: float,
    duration_s: float,
    flap_rate: float = 0.0,
    seed_name: str = "p4:sweep",
) -> dict:
    """Round-robin reachability sweep under the same concurrency bound.

    Coverage interval is the wall-clock time between two probes of the same
    camera. With refusal semantics the bound is exact: n/capacity * probe_time,
    shrinking as three-strike marks dead cameras offline.
    """
    g = rng(seed_name)
    ids = [f"CAM{i:05d}" for i in range(n_cameras)]
    truly_dead = set(ids[: int(n_cameras * flap_rate)])
    health = ThreeStrikeHealth()
    for c in ids:
        health.health[c] = "unknown"
    t = 0.0
    cursor = 0
    last_seen: dict[str, float] = {}
    intervals: list[float] = []
    probes = 0
    pool = list(ids)
    dirty = False
    while t < duration_s:
        if dirty:
            pool = health.eligible(pool)
            cursor = 0
            dirty = False
        if not pool:
            break
        batch = [pool[(cursor + i) % len(pool)] for i in range(min(capacity, len(pool)))]
        cursor = (cursor + capacity) % len(pool)
        for cam in batch:
            ok = cam not in truly_dead and float(g.random()) > 0.01
            before = health.health.get(cam)
            health.observe(cam, ok)
            if health.health.get(cam) == "offline" and before != "offline":
                dirty = True
            probes += 1
            if cam in last_seen:
                intervals.append(t - last_seen[cam])
            last_seen[cam] = t
        t += probe_seconds
    import numpy as np

    arr = np.asarray(intervals, dtype=float)
    offline = sum(1 for c in ids if health.health.get(c) == "offline")
    import numpy as _np  # noqa: F401
    return {
        "cameras": n_cameras,
        "capacity": capacity,
        "probe_seconds": probe_seconds,
        "duration_s": duration_s,
        "probes": probes,
        "cameras_marked_offline": offline,
        "true_dead": len(truly_dead),
        "false_offline": max(0, offline - len(truly_dead)),
        "mean_coverage_interval_s": float(arr.mean()) if arr.size else float("nan"),
        "p99_coverage_interval_s": float(np.percentile(arr, 99)) if arr.size else float("nan"),
        "analytic_bound_s": n_cameras / capacity * probe_seconds,
    }
