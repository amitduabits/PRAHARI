"""Run every paper's experiments, then render the figures."""

from __future__ import annotations

import importlib
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

MODULES = [
    ("P1", "prresearch.p1_provenance.experiment"),
    ("P2", "prresearch.p2_fallback.experiment"),
    ("P3", "prresearch.p3_nextcam.experiment"),
    ("P4", "prresearch.p4_admission.experiment"),
    ("P5", "prresearch.p5_fusion.experiment"),
    ("P6", "prresearch.p6_platform.experiment"),
]


def main(only: str | None = None) -> None:
    for tag, mod in MODULES:
        if only and only.upper() != tag:
            continue
        t0 = time.time()
        print(f"\n===== {tag} {mod}")
        importlib.import_module(mod).main()
        print(f"----- {tag} done in {time.time() - t0:.1f}s")
    import make_figures

    make_figures.main()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
