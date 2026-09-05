"""Paper 3 experiments.

E3.1  Top-1 / Top-3 accuracy across three topologies. The claim under test is
      that the implicit model matches the road-network oracle on a regular grid
      and beats it on irregular deployments.
E3.2  Robustness to sparse history: sweep the number of training trips and
      report where the frequency model overtakes the geographic fallback.
E3.3  Fallback share: how often the GIS path is taken, by training volume.
E3.4  Sensitivity of transition counts to the 120 s collapse window: detections
      merged inside one window do not create a transition.
"""

from __future__ import annotations

import json
from pathlib import Path

from prresearch.p3_nextcam.predictors import (
    ConstantVelocity,
    DistanceOnly,
    GraphNeighbour,
    MarkovBackoff,
    TransitionFrequency,
    evaluate,
)
from prresearch.traces import build_estate, generate_trips

RESULTS = Path(__file__).resolve().parents[2] / "results"
TOPOLOGIES = ("grid", "smallworld", "irregular")


def _split(trips, frac=0.7):
    k = int(len(trips) * frac)
    return trips[:k], trips[k:]


def e3_1_topologies(n_cameras: int = 400, n_vehicles: int = 4000) -> dict:
    rows = []
    for topo in TOPOLOGIES:
        estate = build_estate(n_cameras, topo, seed_name="p3")
        trips = generate_trips(estate, n_vehicles, seed_name=f"p3:trips:{topo}")
        train, test = _split(trips)
        for pred in (
            TransitionFrequency(estate).fit(train),
            MarkovBackoff(estate).fit(train),
            DistanceOnly(estate),
            ConstantVelocity(estate),
            GraphNeighbour(estate),
        ):
            r = evaluate(pred, test)
            r["topology"] = topo
            r["train_trips"] = len(train)
            rows.append(r)
    return {"experiment": "E3.1_accuracy_by_topology", "cameras": n_cameras, "rows": rows}


def e3_2_sparsity(n_cameras: int = 400) -> dict:
    rows = []
    for topo in ("grid", "irregular"):
        estate = build_estate(n_cameras, topo, seed_name="p3")
        trips = generate_trips(estate, 6000, seed_name=f"p3:trips:{topo}")
        test = trips[5000:]
        for n_train in (50, 200, 800, 2000, 5000):
            train = trips[:n_train]
            for pred in (
                TransitionFrequency(estate).fit(train),
                MarkovBackoff(estate).fit(train),
                DistanceOnly(estate),
            ):
                r = evaluate(pred, test)
                r["topology"] = topo
                r["train_trips"] = n_train
                rows.append(r)
    return {"experiment": "E3.2_history_sparsity", "rows": rows}


def e3_3_fallback_share(n_cameras: int = 400) -> dict:
    rows = []
    for topo in TOPOLOGIES:
        estate = build_estate(n_cameras, topo, seed_name="p3")
        trips = generate_trips(estate, 6000, seed_name=f"p3:trips:{topo}")
        test = trips[5000:]
        for n_train in (50, 200, 800, 2000, 5000):
            pred = TransitionFrequency(estate).fit(trips[:n_train])
            r = evaluate(pred, test)
            total = pred.history_uses + pred.fallback_uses
            rows.append(
                {
                    "topology": topo,
                    "train_trips": n_train,
                    "top1": r["top1"],
                    "top3": r["top3"],
                    "gis_fallback_share": pred.fallback_uses / (total or 1),
                    "cameras_with_history": len(pred.trans),
                    "cameras": n_cameras,
                }
            )
    return {"experiment": "E3.3_gis_fallback_share", "rows": rows}


def e3_4_collapse_window(n_cameras: int = 400, window_s: tuple = (0, 30, 60, 120, 240, 600)) -> dict:
    """Detections closer than the collapse window merge, so no transition is recorded."""
    rows = []
    estate = build_estate(n_cameras, "irregular", seed_name="p3")
    trips = generate_trips(estate, 6000, seed_name="p3:trips:irregular")
    train_raw, test = trips[:5000], trips[5000:]
    for w in window_s:
        collapsed = []
        merged = 0
        for trip in train_raw:
            out = [trip[0]]
            for cam, t in trip[1:]:
                if cam == out[-1][0] or (t - out[-1][1]) <= w:
                    merged += 1
                    continue
                out.append((cam, t))
            if len(out) >= 2:
                collapsed.append(out)
        pred = TransitionFrequency(estate).fit(collapsed)
        r = evaluate(pred, test)
        rows.append(
            {
                "collapse_window_s": w,
                "top1": r["top1"],
                "top3": r["top3"],
                "observations_merged": merged,
                "distinct_transitions": sum(len(c) for c in pred.trans.values()),
            }
        )
    return {"experiment": "E3.4_collapse_window_sensitivity", "rows": rows}


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    out = {
        "paper": "P3 Implicit motion models: next-camera prediction without road networks",
        "results": [e3_1_topologies(), e3_2_sparsity(), e3_3_fallback_share(), e3_4_collapse_window()],
    }
    path = RESULTS / "p3_nextcam.json"
    path.write_text(json.dumps(out, indent=2))
    print(f"wrote {path}")
    for block in out["results"]:
        print("\n#", block["experiment"])
        for row in block["rows"]:
            print(" ", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in row.items()})


if __name__ == "__main__":
    main()
