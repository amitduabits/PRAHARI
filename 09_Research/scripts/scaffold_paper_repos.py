"""Build six paper packages under PRAHARI-Research and push to GitHub."""

from __future__ import annotations

import shutil
import subprocess
import textwrap
from pathlib import Path

SRC = Path(r"D:\1_Projects\Research_Ongoing\PRAHARI")
DST = Path(r"D:\1_Projects\Research_Ongoing\PRAHARI-Research")
RS = SRC / "09_Research"
LIT = SRC / "Research papers"

REPOS = [
    {
        "name": "PRAHARI-P1-ProvenanceDispatch",
        "slug": "P1",
        "title": "Invocation-Level Provenance Control in Heterogeneous Biometric Systems",
        "tier": "A",
        "venue": "ACM CCS / USENIX Security / PETS",
        "tex": RS / "P1_main.tex",
        "bib": LIT / "P1_Provenance_Dispatch" / "literature" / "refs.bib",
        "code": ["instrument_p1.py"],
        "pkg": "p1_provenance",
        "fig": "p1_dispatch_latency.png",
        "result": "p1_provenance.json",
        "real": ["p1_invocation_measurements.json", "p1_a_summary.json", "p1_c_summary.json", "p1_audit_trail.csv"],
        "claim": "Blocking faces at invocation (not release) is a measurable harm: MEASURED 144 frames, 138 Gov skips, 96% face-path CPU cut, 0 audit violations.",
    },
    {
        "name": "PRAHARI-P2-NegativeResult",
        "slug": "P2",
        "title": "What Provenance Buys: A Negative Result on Label-Free Accuracy Estimation",
        "tier": "C",
        "venue": "Workshop (not ICCV)",
        "tex": None,
        "bib": LIT / "P2_Fallback_Engines" / "literature" / "refs.bib",
        "code": [],
        "pkg": "p2_fallback",
        "fig": "p2_yield_accuracy.png",
        "result": "p2_fallback.json",
        "real": [],
        "claim": "Average Confidence wins on batch accuracy; provenance stratification only buys per-path estimates.",
    },
    {
        "name": "PRAHARI-P3-NextCameraPrediction",
        "slug": "P3",
        "title": "When Counting Is Enough: Regime Characterisation for Next-Camera Prediction",
        "tier": "B",
        "venue": "IJCAI / IEEE T-ITS",
        "tex": None,
        "bib": LIT / "P3_NextCamera_Prediction" / "literature" / "refs.bib",
        "code": [],
        "pkg": "p3_nextcam",
        "fig": "p3_topology_accuracy.png",
        "result": "p3_nextcam.json",
        "real": [],
        "claim": "First-order transition tables are Makris 2004 / Gambs 2012. This paper characterises when counting suffices. Blocked on VeRi-776 and CityFlow.",
    },
    {
        "name": "PRAHARI-P4-RetialQueues",
        "slug": "P4",
        "title": "K-Allocation in Retrial Queues: Decode Admission and Probe Coverage",
        "tier": "A",
        "venue": "SIGMETRICS / IEEE TMM",
        "tex": RS / "P4_main.tex",
        "bib": LIT / "P4_Decoder_Admission" / "literature" / "refs.bib",
        "code": ["instrument_p4.py"],
        "pkg": "p4_admission",
        "fig": "p4_latency_cliff.png",
        "result": "p4_admission.json",
        "real": ["p4_frontier.json", "p4_retrial_analysis.md", "p4_resource_samples.json"],
        "claim": "MEASURED K=1,2,4 extra-admit retries succeed (0 abandoned). K>=8 is DESIGN TARGET, not an 8-12 optimum.",
    },
    {
        "name": "PRAHARI-P5-EventSchema",
        "slug": "P5",
        "title": "How Long Is a Presence? The Geometric 120s Window Is Wrong",
        "tier": "C",
        "venue": "Hold / IEEE TCSVT after reframe",
        "tex": None,
        "bib": LIT / "P5_CrossModal_Fusion" / "literature" / "refs.bib",
        "code": [],
        "pkg": "p5_fusion",
        "fig": "p5_window_tradeoff.png",
        "result": "p5_fusion.json",
        "real": [],
        "claim": "Own synthetic experiments put the knee at 15-30 s; geometric FOV/speed is 1.3-9.6 s. Do not submit the 120 s derivation.",
    },
    {
        "name": "PRAHARI-P6-PlatformArchitecture",
        "slug": "P6",
        "title": "Descriptor-First Federation for Live Camera Estates",
        "tier": "B",
        "venue": "IEEE TETC",
        "tex": None,
        "bib": LIT / "P6_Platform_Architecture" / "literature" / "refs.bib",
        "code": [],
        "pkg": "p6_platform",
        "fig": "p6_coverage_interval.png",
        "result": "p6_platform.json",
        "real": [],
        "claim": "Registry rows vs brokers is a known pattern. Need an NGSI-LD/ONVIF baseline and a falsifiable crossover.",
    },
]

GITIGNORE = """__pycache__/
*.pyc
.venv/
venv/
.env
.pytest_cache/
*.aux
*.log
*.out
*.bbl
*.blg
*.synctex.gz
results/**/*.jsonl
results/real/*.json
!results/.gitkeep
!results/real/.gitkeep
!results/synthetic/.gitkeep
data/*.jsonl
"""

LICENSE = """Paper files under paper/ are licensed CC BY 4.0.
Code files under code/ are licensed CC BY-SA 4.0.
Copyright (c) 2026 Amit Dua / Yushu Excellence Technologies Pvt. Ltd.

You may share the paper with attribution. Derivative code must remain CC BY-SA.
Do not commit Sentinel credentials, raw video, or live catalogue dumps.
"""

STUB_TEX = r"""\documentclass[11pt,a4paper]{article}
\usepackage[margin=1in]{geometry}
\usepackage{booktabs,hyperref,graphicx,amsmath}
\title{TITLE}
\author{Amit Dua\\Yushu Excellence Technologies Pvt.\ Ltd.}
\date{2026}
\begin{document}
\maketitle
\begin{abstract}
CLAIM
\end{abstract}
\section{Status}
Tier TIER. Target venue: VENUE.
This repository is the paper package. Synthetic experiments live in \texttt{code/prresearch}.
Headline numbers, if any, must be labelled MEASURED or DESIGN TARGET.
\section{Reproduction}
\begin{verbatim}
cd code
pip install -r requirements.txt
python -m pytest -q
\end{verbatim}
\end{document}
"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.replace("\r\n", "\n"), encoding="utf-8")


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))


def readme(meta: dict) -> str:
    return textwrap.dedent(
        f"""\
        # {meta['name']}

        **{meta['title']}**

        Author: Amit Dua (Yushu Excellence Technologies Pvt. Ltd.)  
        Tier: {meta['tier']} · Venue aim: {meta['venue']}

        ## Claim

        {meta['claim']}

        Parent platform: https://github.com/amitduabits/PRAHARI

        ## Layout

        ```
        paper/main.tex          draft
        paper/references.bib    verified BibTeX
        code/                   experiment harness + prresearch package
        data/                   fixtures and how to get live data
        results/                generated locally (gitignored JSON/JSONL)
        figs/                   figures
        ```

        ## Reproduce (synthetic, <5 min)

        ```bash
        cd code
        pip install -r requirements.txt
        python -m pytest -q
        python -c "from prresearch.{meta['pkg']}.experiment import main; main()"
        ```

        ## Reproduce (MEASURED P1/P4)

        From the parent PRAHARI tree, not this repo:

        ```bash
        cd 02_Code/prahari
        python scripts/instrument.py all --seconds 8 --frames 6 --k-frames 6 --seed-n 24 --k 1 2 4
        ```

        Live 24 h RTSP is `09_Research/scripts/capture_live.py` in the parent tree.
        Do not commit `.env`, raw video, or `*.jsonl`.

        ## Licence

        Paper: CC BY 4.0. Code: CC BY-SA 4.0.
        """
    )


def data_readme(meta: dict) -> str:
    return textwrap.dedent(
        f"""\
        # Data

        Paper {meta['slug']}. Do not commit live JSONL.

        - Synthetic experiment JSON: copy from parent `09_Research/results/{meta['result']}` after `python run_all.py`.
        - Live Sentinel capture: parent `09_Research/results/real/` (gitignored JSONL).
        - Fixtures in `data/fixtures/` are small MEASURED summaries, not 24 h soaks.

        24 h P1-A output names (when generated):

        - `p1_events_24h_*.jsonl`
        - `catalogue_*.json`
        """
    )


def code_readme(meta: dict) -> str:
    extra = ""
    if meta["slug"] == "P1":
        extra = """
## CONFIG A vs B

```bash
python analyse_p1.py ../data/fixtures/p1_invocation_measurements.json ../data/fixtures/p1_invocation_measurements.json
```

`instrument_p1.py` is a sleep() mock. Production MEASURED path is parent `02_Code/prahari/scripts/instrument.py`.
"""
    if meta["slug"] == "P4":
        extra = """
## K-frontier plot

```bash
python plot_frontier.py ../data/fixtures/p4_frontier.json --output ../figs/fig1_k_frontier.png
```

`instrument_p4.py` is a sleep() mock. MEASURED K is 1,2,4 on StreamSession. K>=8 is DESIGN TARGET.
"""
    return textwrap.dedent(
        f"""\
        # Code — {meta['slug']}

        Package: `prresearch.{meta['pkg']}`

        ```bash
        pip install -r requirements.txt
        python -c "from prresearch.{meta['pkg']}.experiment import main; main()"
        ```
        {extra}
        """
    )


def stub_tex(meta: dict) -> str:
    return (
        STUB_TEX.replace("TITLE", meta["title"])
        .replace("CLAIM", meta["claim"])
        .replace("TIER", meta["tier"])
        .replace("VENUE", meta["venue"])
    )


def build_one(meta: dict) -> Path:
    root = DST / meta["name"]
    if root.exists():
        shutil.rmtree(root)
    for d in ("paper", "code", "data/fixtures", "results/real", "results/synthetic", "figs"):
        (root / d).mkdir(parents=True, exist_ok=True)
        if d.startswith("results"):
            (root / d / ".gitkeep").write_text("", encoding="utf-8")
    (root / "figs" / ".gitkeep").write_text("", encoding="utf-8")
    write(root / ".gitignore", GITIGNORE)
    write(root / "LICENSE", LICENSE)
    write(root / "README.md", readme(meta))
    write(root / "data" / "README.md", data_readme(meta))
    write(root / "data" / ".gitignore", "*.jsonl\n")
    write(root / "results" / ".gitignore", "*.jsonl\n*.json\n*.csv\n!.gitkeep\n!real/.gitkeep\n!synthetic/.gitkeep\n")
    write(root / "code" / "README.md", code_readme(meta))
    write(root / "code" / "requirements.txt", "numpy>=2.0\nmatplotlib>=3.8\npytest>=8.0\n")

    if meta["tex"] and meta["tex"].is_file():
        shutil.copy2(meta["tex"], root / "paper" / "main.tex")
    else:
        write(root / "paper" / "main.tex", stub_tex(meta))
    if meta["bib"].is_file():
        shutil.copy2(meta["bib"], root / "paper" / "references.bib")
    else:
        write(root / "paper" / "references.bib", "% no bib yet\n")

    copy_tree(RS / "prresearch" / meta["pkg"], root / "code" / "prresearch" / meta["pkg"])
    shutil.copy2(RS / "prresearch" / "__init__.py", root / "code" / "prresearch" / "__init__.py")
    shutil.copy2(RS / "prresearch" / "seeds.py", root / "code" / "prresearch" / "seeds.py")
    shutil.copy2(RS / "prresearch" / "metrics.py", root / "code" / "prresearch" / "metrics.py")
    shutil.copy2(RS / "prresearch" / "traces.py", root / "code" / "prresearch" / "traces.py")

    test_src = RS / "tests" / f"test_{meta['slug'].lower()}.py"
    if test_src.is_file():
        (root / "code" / "tests").mkdir(exist_ok=True)
        shutil.copy2(test_src, root / "code" / "tests" / test_src.name)
        shutil.copy2(RS / "tests" / "test_traces.py", root / "code" / "tests" / "test_traces.py")

    for name in meta["code"]:
        src = RS / name
        if src.is_file():
            shutil.copy2(src, root / "code" / name)
    if meta["slug"] == "P1":
        shutil.copy2(RS / "scripts" / "analyse_p1.py", root / "code" / "analyse_p1.py")
    if meta["slug"] == "P4":
        shutil.copy2(RS / "scripts" / "plot_frontier.py", root / "code" / "plot_frontier.py")

    fig = RS / "figures" / meta["fig"]
    if fig.is_file():
        shutil.copy2(fig, root / "figs" / fig.name)
    res = RS / "results" / meta["result"]
    if res.is_file():
        shutil.copy2(res, root / "data" / "fixtures" / res.name)
    for name in meta["real"]:
        p = RS / "results" / "real" / name
        if p.is_file() and p.stat().st_size < 500_000:
            shutil.copy2(p, root / "data" / "fixtures" / name)
    write(root / "code" / "pytest.ini", "[pytest]\npythonpath = .\n")
    return root


def git_push(root: Path, name: str, desc: str) -> None:
    subprocess.run(["git", "init", "-b", "main"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(["git", "commit", "-m", f"Initial: {name} paper structure + harnesses"], cwd=root, check=True)
    r = subprocess.run(
        [
            "gh",
            "repo",
            "create",
            f"amitduabits/{name}",
            "--public",
            "--description",
            desc[:350],
            "--source",
            str(root),
            "--remote",
            "origin",
            "--push",
        ],
        cwd=root,
        capture_output=True,
        text=True,
    )
    print(r.stdout)
    print(r.stderr)
    if r.returncode != 0:
        # repo may already exist
        subprocess.run(["git", "remote", "remove", "origin"], cwd=root, check=False)
        subprocess.run(["git", "remote", "add", "origin", f"https://github.com/amitduabits/{name}.git"], cwd=root, check=True)
        push = subprocess.run(["git", "push", "-u", "origin", "main"], cwd=root, capture_output=True, text=True)
        print(push.stdout, push.stderr)
        if push.returncode != 0:
            push2 = subprocess.run(["git", "push", "-u", "origin", "main", "--force"], cwd=root, capture_output=True, text=True)
            print(push2.stdout, push2.stderr)
            if push2.returncode != 0:
                raise SystemExit(f"push failed for {name}")


def main() -> None:
    DST.mkdir(parents=True, exist_ok=True)
    for meta in REPOS:
        print("== build", meta["name"])
        root = build_one(meta)
        desc = f"{meta['title']} (Tier {meta['tier']}). {meta['claim'][:180]}"
        git_push(root, meta["name"], desc)
        print("done", meta["name"])


if __name__ == "__main__":
    main()
