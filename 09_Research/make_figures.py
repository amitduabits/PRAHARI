"""Render one figure per paper from the results JSON. Run experiments first."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"

INK = "#1c1c1c"
SERIES = ["#2f5d8a", "#c2622d", "#4a7a52", "#8a4f6d", "#6b6b6b"]


def _load(name: str) -> dict:
    return json.loads((RESULTS / name).read_text())


def _block(doc: dict, key: str) -> dict:
    return next(b for b in doc["results"] if b["experiment"].startswith(key))


def _style(ax, title: str, xlabel: str, ylabel: str) -> None:
    ax.set_title(title, fontsize=10, color=INK, loc="left")
    ax.set_xlabel(xlabel, fontsize=9, color=INK)
    ax.set_ylabel(ylabel, fontsize=9, color=INK)
    ax.tick_params(labelsize=8, colors=INK)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(True, axis="y", alpha=0.25, linewidth=0.6)
    ax.legend(fontsize=8, frameon=False)


def fig_p1() -> None:
    b = _block(_load("p1_provenance.json"), "E1.1")
    fig, ax = plt.subplots(figsize=(5.2, 3.2), dpi=160)
    for i, method in enumerate(("provenance_gated", "query_time_rbac")):
        rows = [r for r in b["rows"] if r["method"] == method]
        ax.plot([r["policy_rules"] for r in rows], [r["median_ns"] for r in rows],
                marker="o", ms=4, color=SERIES[i], label=method.replace("_", " "))
    ax.set_yscale("log")
    _style(ax, "P1  Dispatch cost is flat in policy size", "policy rules", "median dispatch, ns")
    fig.tight_layout(); fig.savefig(FIGURES / "p1_dispatch_latency.png"); plt.close(fig)


def fig_p2() -> None:
    b = _block(_load("p2_fallback.json"), "E2.1")
    fig, ax = plt.subplots(figsize=(5.2, 3.2), dpi=160)
    pairs = sorted({r["pair"] for r in b["rows"]})
    for i, pair in enumerate(pairs):
        rows = sorted([r for r in b["rows"] if r["pair"] == pair], key=lambda r: r["injected_fail_rate"])
        ax.plot([r["injected_fail_rate"] for r in rows], [r["two_tier_accuracy"] for r in rows],
                marker="o", ms=4, color=SERIES[i], label=f"{pair} two-tier")
        ax.plot([r["injected_fail_rate"] for r in rows], [r["primary_only_accuracy_over_all"] for r in rows],
                marker="s", ms=3, ls="--", color=SERIES[i], alpha=0.6, label=f"{pair} primary only")
    _style(ax, "P2  Accuracy over all frames as the primary fails more often",
           "injected primary failure rate", "correct answers / frames")
    fig.tight_layout(); fig.savefig(FIGURES / "p2_yield_accuracy.png"); plt.close(fig)


def fig_p3() -> None:
    b = _block(_load("p3_nextcam.json"), "E3.1")
    topos = ["grid", "smallworld", "irregular"]
    methods = ["transition_frequency", "graph_neighbour_oracle", "distance_only", "constant_velocity"]
    fig, ax = plt.subplots(figsize=(5.8, 3.2), dpi=160)
    w = 0.2
    for i, m in enumerate(methods):
        vals = [next(r["top1"] for r in b["rows"] if r["topology"] == t and r["method"] == m) for t in topos]
        ax.bar([x + i * w for x in range(len(topos))], vals, width=w, color=SERIES[i], label=m.replace("_", " "))
    ax.set_xticks([x + 1.5 * w for x in range(len(topos))]); ax.set_xticklabels(topos)
    ax.set_ylim(0, 0.85)
    _style(ax, "P3  Top-1 next-camera accuracy by topology", "", "top-1 accuracy")
    fig.tight_layout(); fig.savefig(FIGURES / "p3_topology_accuracy.png"); plt.close(fig)


def fig_p4() -> None:
    b = _block(_load("p4_admission.json"), "E4.4")
    fig, ax = plt.subplots(figsize=(5.2, 3.2), dpi=160)
    for i, pol in enumerate(("refuse", "queue")):
        rows = sorted([r for r in b["rows"] if r["policy"] == pol], key=lambda r: r["offered_load"])
        ax.plot([r["offered_load"] for r in rows], [r["p99_latency_s"] for r in rows],
                marker="o", ms=4, color=SERIES[i], label=f"{pol} p99")
    ax.set_yscale("log")
    ax.axvline(1.0, color=INK, lw=0.7, ls=":")
    _style(ax, "P4  p99 latency either side of saturation", "offered load", "p99 latency, s")
    fig.tight_layout(); fig.savefig(FIGURES / "p4_latency_cliff.png"); plt.close(fig)


def fig_p5() -> None:
    b = _block(_load("p5_fusion.json"), "E5.2")
    rows = sorted(b["rows"], key=lambda r: r["window_s"])
    fig, ax = plt.subplots(figsize=(5.4, 3.2), dpi=160)
    ax.plot([r["window_s"] for r in rows], [r["alerts_per_incident"] for r in rows],
            marker="o", ms=4, color=SERIES[0], label="alerts per incident")
    ax2 = ax.twinx()
    ax2.plot([r["window_s"] for r in rows], [r["distinct_incident_recall"] for r in rows],
             marker="s", ms=4, color=SERIES[1], label="distinct-incident recall")
    ax2.set_ylabel("distinct-incident recall", fontsize=9, color=INK)
    ax2.tick_params(labelsize=8)
    ax.axvline(b["deployed_window_s"], color=INK, lw=0.7, ls=":")
    ax.set_xscale("symlog", linthresh=10)
    ax.set_xlim(left=0)
    _style(ax, "P5  The collapse window trades fatigue against masked incidents",
           "collapse window, s", "alerts per incident")
    ax2.legend(fontsize=8, frameon=False, loc="lower left")
    fig.tight_layout(); fig.savefig(FIGURES / "p5_window_tradeoff.png"); plt.close(fig)


def fig_p6() -> None:
    b = _block(_load("p6_platform.json"), "E6.4")
    fig, ax = plt.subplots(figsize=(5.4, 3.2), dpi=160)
    scales = sorted({r["scale"] for r in b["rows"]})
    for i, scale in enumerate(scales):
        rows = sorted([r for r in b["rows"] if r["scale"] == scale], key=lambda r: r["capacity"])
        ax.plot([r["capacity"] for r in rows], [r["coverage_interval_minutes"] for r in rows],
                marker="o", ms=4, color=SERIES[i], label=f"{scale} cameras")
    ax.set_xscale("log", base=2); ax.set_yscale("log")
    _style(ax, "P6  Sweep coverage interval vs. decoder budget", "concurrent decoders", "coverage interval, minutes")
    fig.tight_layout(); fig.savefig(FIGURES / "p6_coverage_interval.png"); plt.close(fig)


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    made = []
    for fn in (fig_p1, fig_p2, fig_p3, fig_p4, fig_p5, fig_p6):
        try:
            fn()
            made.append(fn.__name__)
        except FileNotFoundError as exc:
            print(f"skip {fn.__name__}: {exc}", file=sys.stderr)
    print("figures:", ", ".join(made))


if __name__ == "__main__":
    main()
