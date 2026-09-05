"""Plot K-frontier from MEASURED JSON. Usage: python plot_frontier.py path.json --output figs/fig1.pdf"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("json_path")
    parser.add_argument("--output", default="figs/fig1_k_frontier.png")
    args = parser.parse_args()
    doc = json.loads(Path(args.json_path).read_text(encoding="utf-8"))
    rows = doc.get("frontier") or []
    ks = [r.get("K") or r.get("k") for r in rows]
    p99 = [r.get("p99_latency_ms") or r.get("latency_p99_ms") for r in rows]
    hit = [r.get("cache_hit_rate_pct") for r in rows]
    fig, ax1 = plt.subplots(figsize=(6.2, 3.4), dpi=160)
    ax1.plot(ks, p99, marker="o", color="#2f5d8a", label="p99 latency (ms)")
    ax1.set_xlabel("K (concurrent captures)")
    ax1.set_ylabel("p99 latency (ms)", color="#2f5d8a")
    ax2 = ax1.twinx()
    ax2.plot(ks, hit, marker="s", color="#c2622d", label="cache hit %")
    ax2.set_ylabel("cache hit %", color="#c2622d")
    ax1.set_title("P4 MEASURED K-frontier (file/live decode)")
    ax1.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
