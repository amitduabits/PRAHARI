# C08 — Experiment harness

Prepend `00_MASTER_CONTEXT.md`. AGENT. Depends on C02–C06 at least stubbed.

## Goal

One command produces MEASURED logs the jury (and we) can read.

## Agent

1. `scripts/run_experiments.py` argparse `--suite smoke|anpr|objects|faces|gov|scale|all`.

   smoke = E-A1, E-O1, E-F1, E-I1, E-W1, Tesseract probe, health.

   Each case writes `05_Output/experiments/{id}_{utc}.json` per catalogue schema and appends a Markdown row to `EXPERIMENT_LOG.md`.

2. Do not require SENTINEL_HOST for smoke. Gov suite SKIPPED with reason if host empty.

3. Exit code 0 if every non-skipped case ok. Skips are not failures. A failed MEASURED case is exit 1.

4. README subsection: how to run the harness.

5. Run `--suite smoke` once and leave the log in git (no secrets, no RTSP URLs).

## Done when

- `python scripts/run_experiments.py --suite smoke` runs.
- EXPERIMENT_LOG.md has rows.
- CSV C08-* DONE.

## Do not

Print JUDGE_PASSWORD. Dump raw RTSP. Hang on a live RTSP open in smoke.
