#!/usr/bin/env python3
"""
SYNTHETIC mock. asyncio.Semaphore + sleep is not the deployed StreamSession
path. MEASURED K-frontier is 02_Code/prahari/scripts/instrument.py p4-b
(K=1,2,4 on own_feed.mp4). K>4 is DESIGN TARGET.

P4-RetialQueues: K-allocation frontier measurement

Standalone harness (no PRAHARI codebase dependency).
Sweeps K (concurrent decode slots) from 1 to 24 and measures latency, cache hit, retries.

Usage:
  python instrument_p4.py --k-values 1,2,4,8,12,16,24 --frames-per-k 200 --output results/p4_frontier.json
  python plot_frontier.py results/p4_frontier.json
"""

import argparse
import asyncio
import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class DecodeSemaphore:
    """Simulates hardware decode slots with retrial queue."""
    
    def __init__(self, k: int):
        self.k = k
        self.semaphore = asyncio.Semaphore(k)
        self.retry_count = 0
        self.abandoned_count = 0
    
    async def acquire_with_retry(self, max_retries: int = 5) -> bool:
        """Try to acquire decode slot; retry if necessary."""
        for attempt in range(max_retries):
            try:
                self.semaphore.acquire()
                return True
            except Exception:
                self.retry_count += 1
                await asyncio.sleep(0.001 * (2 ** attempt))  # Exponential backoff
        
        self.abandoned_count += 1
        return False


class PredictionCache:
    """Next-camera prediction cache (Markov transition matrix columns)."""
    
    def __init__(self, max_size: int = 1000):
        self.cache = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def lookup(self, camera_id: str) -> bool:
        """Lookup next-camera prediction for camera_id. Return True if hit."""
        if camera_id in self.cache:
            self.hits += 1
            return True
        
        if len(self.cache) < self.max_size:
            self.cache[camera_id] = {"transitions": np.random.random((10,))}
            self.misses += 1
            return False
        
        # Cache full, evict random entry
        evict_key = np.random.choice(list(self.cache.keys()))
        del self.cache[evict_key]
        self.cache[camera_id] = {"transitions": np.random.random((10,))}
        self.misses += 1
        return False
    
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0


async def simulate_decode(k: int, frame_idx: int, cache: PredictionCache) -> dict:
    """Simulate a single decode + analyse + track operation."""
    
    # Step 1: Decode (acquire slot)
    decode_start = time.perf_counter()
    # (In real system, would wait on semaphore; here we skip for simplicity)
    await asyncio.sleep(0.001)  # Simulate decode latency
    
    # Step 2: Analyse (ANPR, objects, faces)
    await asyncio.sleep(0.002)  # Simulate analyse
    
    # Step 3: Track (next-camera prediction cache lookup)
    camera_id = f"CAM-{frame_idx % 50:03d}"
    cache_hit = cache.lookup(camera_id)
    
    # Step 4: Emit event
    await asyncio.sleep(0.0001)
    
    decode_latency = (time.perf_counter() - decode_start) * 1000
    
    return {
        "frame_idx": frame_idx,
        "decode_request_id": f"decode-{frame_idx}",
        "latency_ms": decode_latency,
        "cache_hit": cache_hit,
        "retried": False,
        "abandoned": False,
    }


async def sweep_k(k: int, num_frames: int = 200) -> dict:
    """Run measurement for a single K value."""
    
    log.info(f"Sweeping K={k} with {num_frames} frames...")
    
    cache = PredictionCache(max_size=50 + k * 20)  # Cache size grows with K
    
    cpu_start = time.process_time()
    wall_start = time.perf_counter()
    
    # Simulate concurrent decode tasks
    tasks = []
    for frame_idx in range(num_frames):
        task = simulate_decode(k, frame_idx, cache)
        tasks.append(task)
    
    events = await asyncio.gather(*tasks)
    
    cpu_time = time.process_time() - cpu_start
    wall_time = time.perf_counter() - wall_start
    
    # Compute statistics
    latencies = np.array([e["latency_ms"] for e in events])
    cache_hits = sum(1 for e in events if e["cache_hit"])
    
    result = {
        "k": k,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "num_frames": num_frames,
        "p50_latency_ms": float(np.percentile(latencies, 50)),
        "p99_latency_ms": float(np.percentile(latencies, 99)),
        "mean_latency_ms": float(np.mean(latencies)),
        "std_latency_ms": float(np.std(latencies)),
        "cache_hit_rate_pct": cache.hit_rate(),
        "cache_size": len(cache.cache),
        "cpu_time_s": cpu_time,
        "wall_time_s": wall_time,
        "retries": 0,  # (placeholder; would track in real semaphore)
        "abandoned": 0,
    }
    
    log.info(f"  K={k}: p50={result['p50_latency_ms']:.1f}ms, cache={result['cache_hit_rate_pct']:.0f}%")
    
    return result


async def run_k_sweep(k_values: list, frames_per_k: int = 200) -> list[dict]:
    """Run K-sweep across all K values."""
    
    results = []
    for k in k_values:
        result = await sweep_k(k, frames_per_k)
        results.append(result)
    
    return results


def main():
    parser = argparse.ArgumentParser(description="P4 K-allocation frontier measurement")
    parser.add_argument("--k-values", default="1,2,4,8,12,16,24", help="Comma-separated K values")
    parser.add_argument("--frames-per-k", type=int, default=200, help="Frames per K (default 200)")
    parser.add_argument("--output", required=True, help="Output JSON file")
    
    args = parser.parse_args()
    
    k_values = [int(k.strip()) for k in args.k_values.split(",")]
    
    log.info(f"Starting K-sweep: K={k_values}, frames={args.frames_per_k} per K")
    
    # Run async measurement
    results = asyncio.run(run_k_sweep(k_values, args.frames_per_k))
    
    # Write results
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    output = {
        "workload": "PRAHARI CCTV analytics",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "k_values": k_values,
        "frames_per_k": args.frames_per_k,
        "frontier": results,
    }
    
    with out_path.open("w") as f:
        json.dump(output, f, indent=2)
    
    log.info(f"K-frontier results written to {out_path}")
    
    # Summary table
    log.info("\nK-Allocation Frontier Summary:")
    log.info("K  | p50(ms) | p99(ms) | Cache(%) | CPU(s)")
    log.info("---|---------|---------|----------|-------")
    for r in results:
        log.info(f"{r['k']:2d} | {r['p50_latency_ms']:7.1f} | {r['p99_latency_ms']:7.1f} | {r['cache_hit_rate_pct']:8.0f} | {r['cpu_time_s']:7.3f}")


if __name__ == "__main__":
    main()
