"""Paper 4 experiments.

E4.1  Latency and resource envelope of refusal semantics vs. queue, evict and
      degrade, swept across offered load. The claim under test: refusal keeps
      p99 flat and bounds peak concurrency exactly; the alternatives trade a
      bounded refusal rate for an unbounded latency tail.
E4.2  Peak resource envelope is independent of estate cardinality.
E4.3  Rotational sweep coverage interval against the analytic bound, with and
      without three-strike health hysteresis on a flapping estate.
E4.4  The latency cliff: behaviour either side of saturation.
"""

from __future__ import annotations

import json
from pathlib import Path

from prresearch.p4_admission.simulator import generate_arrivals, rotational_sweep, simulate

RESULTS = Path(__file__).resolve().parents[2] / "results"
POLICIES = ("refuse", "queue", "evict", "degrade")


def e4_1_policies(capacity: int = 4, n: int = 20000) -> dict:
    rows = []
    mean_service = 2.0
    for rate in (0.5, 1.0, 2.0, 4.0, 6.0, 8.0):
        reqs = generate_arrivals(n, rate, mean_service, seed_name=f"p4:arr:{rate}")
        offered = rate * mean_service / capacity
        for pol in POLICIES:
            r = simulate(reqs, capacity, pol)
            r["arrival_rate_per_s"] = rate
            r["offered_load"] = offered
            rows.append(r)
    return {"experiment": "E4.1_policy_comparison", "mean_service_s": mean_service, "rows": rows}


def e4_2_estate_independence(capacity: int = 4, n: int = 20000) -> dict:
    """Peak decoders is a property of the bound, not of how many cameras exist."""
    rows = []
    for estate_size in (800, 8000, 80000):
        reqs = generate_arrivals(n, 4.0, 2.0, seed_name=f"p4:estate:{estate_size}")
        for req in reqs:
            req.camera_id = f"CAM{hash(req.req_id) % estate_size:05d}"
        for pol in ("refuse", "degrade"):
            r = simulate(reqs, capacity, pol)
            r["estate_cameras"] = estate_size
            rows.append(r)
    return {"experiment": "E4.2_peak_envelope_vs_estate_size", "rows": rows}


def e4_3_sweep() -> dict:
    rows = []
    for n_cameras in (800, 8000, 80000):
        for flap in (0.0, 0.05, 0.20):
            r = rotational_sweep(
                n_cameras=n_cameras,
                capacity=4,
                probe_seconds=1.2,
                duration_s=max(4.0 * n_cameras / 4 * 1.2, 3600.0),
                flap_rate=flap,
                seed_name=f"p4:sweep:{n_cameras}:{flap}",
            )
            r["flap_rate"] = flap
            rows.append(r)
    return {"experiment": "E4.3_rotational_sweep_coverage", "rows": rows}


def e4_4_cliff(capacity: int = 4, n: int = 20000) -> dict:
    rows = []
    mean_service = 2.0
    for rate in (1.6, 1.8, 1.9, 2.0, 2.1, 2.2, 2.4, 3.0):
        reqs = generate_arrivals(n, rate, mean_service, seed_name=f"p4:cliff:{rate}")
        for pol in ("refuse", "queue"):
            r = simulate(reqs, capacity, pol)
            rows.append(
                {
                    "policy": pol,
                    "arrival_rate_per_s": rate,
                    "offered_load": rate * mean_service / capacity,
                    "p50_latency_s": r["p50_latency_s"],
                    "p99_latency_s": r["p99_latency_s"],
                    "max_latency_s": r["max_latency_s"],
                    "refusal_rate": r["refusal_rate"],
                    "peak_concurrent_decoders": r["peak_concurrent_decoders"],
                }
            )
    return {"experiment": "E4.4_latency_cliff", "rows": rows}


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    out = {
        "paper": "P4 Deterministic concurrent decoder management",
        "results": [e4_1_policies(), e4_2_estate_independence(), e4_3_sweep(), e4_4_cliff()],
    }
    path = RESULTS / "p4_admission.json"
    path.write_text(json.dumps(out, indent=2))
    print(f"wrote {path}")
    for block in out["results"]:
        print("\n#", block["experiment"])
        for row in block["rows"]:
            print(" ", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in row.items()})


if __name__ == "__main__":
    main()
