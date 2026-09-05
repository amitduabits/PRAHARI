#!/usr/bin/env python3
"""
SYNTHETIC mock. Uses time.sleep() and numpy.random. Headline paper numbers
must come from 02_Code/prahari/scripts/instrument.py (MEASURED on analyse()).

P1-ProvenanceDispatch: Invocation-level provenance control measurement

Standalone harness (no PRAHARI codebase dependency).
Measures CPU/latency/audit for CONFIG A (baseline) vs CONFIG B (provenance gated).

Usage:
  python instrument_p1.py --config a --output results/config_a.json
  python instrument_p1.py --config b --output results/config_b.json
  python analyse_p1.py results/config_a.json results/config_b.json
"""

import argparse
import json
import logging
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class FaceModel:
    """Mock face model (simulates VGGFace2 + InceptionResnetV1)."""
    
    def __init__(self):
        self.loaded = False
        self.load_time = 0.0
    
    def load(self):
        """Simulate model weight loading (~2 seconds)."""
        start = time.time()
        time.sleep(0.2)  # Simulate load overhead
        self.load_time = time.time() - start
        self.loaded = True
        log.info(f"Face model loaded in {self.load_time:.3f}s")
    
    def match(self, frame: np.ndarray) -> dict:
        """Simulate face matching (~50 ms)."""
        if not self.loaded:
            self.load()
        
        start = time.time()
        time.sleep(0.05)  # Simulate embedding + cosine similarity
        latency = time.time() - start
        
        # Return a mock detection
        return {
            "face_id": f"WL-{np.random.randint(1, 10):03d}",
            "confidence": 0.85 + np.random.random() * 0.15,
            "bbox": [100, 100, 200, 250],
            "latency_ms": latency * 1000,
        }


class ANPRModel:
    """Mock ANPR model."""
    
    def recognize(self, frame: np.ndarray) -> dict:
        """Simulate plate recognition (~30 ms)."""
        start = time.time()
        time.sleep(0.03)
        latency = time.time() - start
        
        return {
            "plate": "GJ01AB1234",
            "confidence": 0.90 + np.random.random() * 0.09,
            "bbox": [200, 300, 400, 350],
            "latency_ms": latency * 1000,
        }


def engines_for_config_a(camera: dict) -> list[str]:
    """CONFIG A: All cameras invoke all engines (baseline)."""
    return ["anpr", "objects", "faces"]


def engines_for_config_b(camera: dict) -> list[str]:
    """CONFIG B: Gov/sandbox cameras skip faces (provenance gated)."""
    engines = ["anpr", "objects", "faces"]
    
    ownership = str(camera.get("ownership") or "")
    cam_id = str(camera.get("camera_id") or "")
    
    # Gate: refuse faces on Gov or sandbox (camNN)
    if ownership != "Own" or cam_id.lower().startswith("cam"):
        engines = [e for e in engines if e != "faces"]
    
    return engines


def simulate_frame(idx: int) -> np.ndarray:
    """Generate a synthetic frame (1920x1080 RGB)."""
    return np.random.randint(0, 256, (1080, 1920, 3), dtype=np.uint8)


def run_measurement(config: str, num_cameras: int = 50, frames_per_camera: int = 21) -> dict:
    """
    Run measurement for given configuration.
    
    Args:
        config: "a" (baseline) or "b" (provenance gated)
        num_cameras: Number of cameras to simulate
        frames_per_camera: Frames per camera
    
    Returns:
        dict with measurements
    """
    
    log.info(f"Starting CONFIG {config.upper()} measurement ({num_cameras} cameras, {frames_per_camera} frames each)")
    
    # Pick engine selection function
    engines_fn = engines_for_config_a if config == "a" else engines_for_config_b
    
    # Create camera registry (mix of Own and Gov)
    cameras = []
    for i in range(num_cameras):
        ownership = "Own" if i % 2 == 0 else "Gov"
        cameras.append({
            "camera_id": f"CAM-{'OWN' if ownership == 'Own' else 'GOV'}-{i:03d}",
            "ownership": ownership,
            "lat": 20.0 + i * 0.01,
            "lon": 72.0 + i * 0.01,
        })
    
    # Initialize models
    face_model = FaceModel()
    anpr_model = ANPRModel()
    
    # Metrics
    total_cpu_face = 0.0
    total_cpu_anpr = 0.0
    face_events = 0
    anpr_events = 0
    face_model_loads = 0
    latencies = []
    audit_trail = []
    
    # Run analysis
    total_frames = num_cameras * frames_per_camera
    
    for cam_idx, camera in enumerate(cameras):
        engines = engines_fn(camera)
        
        for frame_idx in range(frames_per_camera):
            frame = simulate_frame(frame_idx)
            frame_start = time.perf_counter()
            
            events = []
            
            # ANPR
            if "anpr" in engines:
                anpr_start = time.perf_counter()
                result = anpr_model.recognize(frame)
                anpr_cpu = time.perf_counter() - anpr_start
                total_cpu_anpr += anpr_cpu
                anpr_events += 1
                events.append(("anpr", result))
                audit_trail.append({
                    "ts": datetime.now(timezone.utc).isoformat(),
                    "camera_id": camera["camera_id"],
                    "engine": "anpr",
                    "invoked": True,
                })
            else:
                audit_trail.append({
                    "ts": datetime.now(timezone.utc).isoformat(),
                    "camera_id": camera["camera_id"],
                    "engine": "anpr",
                    "invoked": False,
                })
            
            # Faces
            if "faces" in engines:
                face_start = time.perf_counter()
                result = face_model.match(frame)
                face_cpu = time.perf_counter() - face_start
                total_cpu_face += face_cpu
                face_events += 1
                if not hasattr(face_model, "_loaded_once"):
                    face_model_loads += 1
                    face_model._loaded_once = True
                events.append(("faces", result))
                audit_trail.append({
                    "ts": datetime.now(timezone.utc).isoformat(),
                    "camera_id": camera["camera_id"],
                    "engine": "faces",
                    "invoked": True,
                })
            else:
                audit_trail.append({
                    "ts": datetime.now(timezone.utc).isoformat(),
                    "camera_id": camera["camera_id"],
                    "engine": "faces",
                    "invoked": False,
                })
            
            frame_latency = (time.perf_counter() - frame_start) * 1000
            latencies.append(frame_latency)
        
        if (cam_idx + 1) % 10 == 0:
            log.info(f"  {cam_idx + 1}/{num_cameras} cameras processed")
    
    # Compute statistics
    latencies = np.array(latencies)
    
    result = {
        "config": config.upper(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cameras_measured": num_cameras,
        "frames_total": total_frames,
        "face_events_total": face_events,
        "anpr_events_total": anpr_events,
        "face_model_loads": face_model_loads,
        "cpu_face_total_s": total_cpu_face,
        "cpu_anpr_total_s": total_cpu_anpr,
        "cpu_total_s": total_cpu_face + total_cpu_anpr,
        "latency_p50_ms": float(np.percentile(latencies, 50)),
        "latency_p99_ms": float(np.percentile(latencies, 99)),
        "latency_mean_ms": float(np.mean(latencies)),
        "latency_std_ms": float(np.std(latencies)),
        "audit_trail_len": len(audit_trail),
        "audit_violations": sum(
            1 for row in audit_trail
            if row["engine"] == "faces" and row["invoked"]
            and any(cam["camera_id"] == row["camera_id"] and cam["ownership"] != "Own"
                    for cam in cameras)
        ),
    }
    
    log.info(f"CONFIG {config.upper()} complete:")
    log.info(f"  Face events: {result['face_events_total']}")
    log.info(f"  ANPR events: {result['anpr_events_total']}")
    log.info(f"  Face CPU: {result['cpu_face_total_s']:.2f}s")
    log.info(f"  Latency p50: {result['latency_p50_ms']:.1f}ms")
    log.info(f"  Audit violations: {result['audit_violations']}")
    
    return result, audit_trail


def main():
    parser = argparse.ArgumentParser(description="P1 Provenance Dispatch measurement")
    parser.add_argument("--config", choices=["a", "b"], required=True, help="CONFIG A (baseline) or B (gated)")
    parser.add_argument("--cameras", type=int, default=50, help="Number of cameras (default 50)")
    parser.add_argument("--frames-per-camera", type=int, default=21, help="Frames per camera (default 21, total 1043)")
    parser.add_argument("--output", required=True, help="Output JSON file")
    
    args = parser.parse_args()
    
    result, audit_trail = run_measurement(
        config=args.config,
        num_cameras=args.cameras,
        frames_per_camera=args.frames_per_camera,
    )
    
    # Write result
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    with out_path.open("w") as f:
        json.dump(result, f, indent=2)
    
    log.info(f"Results written to {out_path}")
    
    # Write audit trail
    audit_path = out_path.parent / f"audit_{args.config}.jsonl"
    with audit_path.open("w") as f:
        for row in audit_trail:
            f.write(json.dumps(row) + "\n")
    
    log.info(f"Audit trail written to {audit_path}")


if __name__ == "__main__":
    main()
