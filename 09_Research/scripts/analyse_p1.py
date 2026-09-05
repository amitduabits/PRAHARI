"""Compare CONFIG A vs CONFIG B measurement JSON. No secrets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def _cfg(doc: dict, key: str) -> dict:
    if key in doc:
        return doc[key]
    if "A_baseline" in doc and key.lower().startswith("a"):
        return doc["A_baseline"]
    if "B_provenance_gated" in doc and key.lower().startswith("b"):
        return doc["B_provenance_gated"]
    raise KeyError(key)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("a")
    parser.add_argument("b")
    parser.add_argument("--output", default="")
    args = parser.parse_args()
    a_doc = json.loads(Path(args.a).read_text(encoding="utf-8"))
    b_doc = json.loads(Path(args.b).read_text(encoding="utf-8"))
    if "A_baseline" in a_doc and "B_provenance_gated" in a_doc:
        a, b = a_doc["A_baseline"], a_doc["B_provenance_gated"]
        src = a_doc
    else:
        a, b = _cfg(a_doc, "config_a"), _cfg(b_doc, "config_b")
        src = {"a": a_doc, "b": b_doc}
    cpu_a = float(a.get("cpu_face_ms_total") or a.get("cpu_face_total_s", 0) * 1000)
    cpu_b = float(b.get("cpu_face_ms_total") or b.get("cpu_face_total_s", 0) * 1000)
    p50_a = float(a.get("p50_latency_ms") or a.get("latency_p50_ms") or 0)
    p50_b = float(b.get("p50_latency_ms") or b.get("latency_p50_ms") or 0)
    cpu_red = (cpu_a - cpu_b) / cpu_a * 100 if cpu_a else 0
    lat_red = (p50_a - p50_b) / p50_a * 100 if p50_a else 0
    out = {
        "label": "MEASURED",
        "config_a": a,
        "config_b": b,
        "improvement": {
            "cpu_reduction_pct": round(cpu_red, 2),
            "latency_improvement_pct": round(lat_red, 2),
            "faces_invoked_A": a.get("faces_invoked"),
            "faces_invoked_B": b.get("faces_invoked"),
            "audit_violations": (src.get("diff") or {}).get("audit_violations", 0),
        },
    }
    text = json.dumps(out, indent=2)
    print(text)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
