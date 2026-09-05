"""Paper 6 experiments.

E6.1  Onboarding cost from 800 to 80,000 cameras, by mode. The architectural
      claim is that bulk registry import, not a federation API, is what makes
      multi-authority onboarding tractable.
E6.2  Transport negotiation mix, and how much of the estate needs a decoder at
      all. This is the input to the Paper 4 concurrency bound.
E6.3  Registry and audit footprint over a year.
E6.4  End-to-end: given the decoder bound from E6.2 and the sweep model from
      Paper 4, what coverage interval does each scale hold?
"""

from __future__ import annotations

import json
from pathlib import Path

from prresearch.p4_admission.simulator import rotational_sweep
from prresearch.p6_platform.platform_model import (
    default_estate,
    onboarding_cost,
    registry_footprint,
    transport_negotiation,
)

RESULTS = Path(__file__).resolve().parents[2] / "results"
SCALES = (800, 8000, 80000)


def e6_1_onboarding() -> dict:
    rows = []
    for scale in SCALES:
        est = default_estate(scale)
        c = onboarding_cost(est)
        rows.append({"scale": scale, **{k: v for k, v in c.items() if k != "per_authority"}})
        for r in c["per_authority"]:
            rows.append({"scale": scale, **r})
    # Counterfactual: onboard the whole estate through the web form.
    alt = []
    for scale in SCALES:
        est = [type(a)(a.name, a.cameras, a.transport_mix, "web_form") for a in default_estate(scale)]
        alt.append({"scale": scale, "all_web_form_hours": onboarding_cost(est)["total_hours"]})
    return {"experiment": "E6.1_onboarding_cost", "rows": rows, "counterfactual": alt}


def e6_2_transports() -> dict:
    rows = []
    for scale in SCALES:
        t = transport_negotiation(default_estate(scale))
        rows.append({"scale": scale, **t})
    return {"experiment": "E6.2_transport_negotiation", "rows": rows}


def e6_3_footprint() -> dict:
    rows = []
    for scale in SCALES:
        for audit_per_day in (12.0, 120.0, 1200.0):
            rows.append({"scale": scale, **registry_footprint(scale, 365, audit_per_day)})
    return {"experiment": "E6.3_registry_and_audit_footprint", "rows": rows}


def e6_4_end_to_end() -> dict:
    rows = []
    for scale in SCALES:
        t = transport_negotiation(default_estate(scale))
        need = max(t["cameras_needing_decoder"], 1)
        for capacity in (4, 8, 16, 32):
            sweep = rotational_sweep(
                n_cameras=need,
                capacity=capacity,
                probe_seconds=1.2,
                duration_s=3.0 * need / capacity * 1.2,
                flap_rate=0.05,
                seed_name=f"p6:{scale}:{capacity}",
            )
            rows.append(
                {
                    "scale": scale,
                    "cameras_needing_decoder": need,
                    "capacity": capacity,
                    "mean_coverage_interval_s": sweep["mean_coverage_interval_s"],
                    "coverage_interval_minutes": round(sweep["mean_coverage_interval_s"] / 60.0, 2),
                    "analytic_bound_s": sweep["analytic_bound_s"],
                }
            )
    return {"experiment": "E6.4_scale_to_coverage_interval", "rows": rows}


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    out = {
        "paper": "P6 Platform design for heterogeneous video analytics across multi-authority deployments",
        "results": [e6_1_onboarding(), e6_2_transports(), e6_3_footprint(), e6_4_end_to_end()],
    }
    path = RESULTS / "p6_platform.json"
    path.write_text(json.dumps(out, indent=2))
    print(f"wrote {path}")
    for block in out["results"]:
        print("\n#", block["experiment"])
        for row in block["rows"]:
            print(" ", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in row.items()})


if __name__ == "__main__":
    main()
