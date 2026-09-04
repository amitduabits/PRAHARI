# C00 — Preflight

Prepend `00_MASTER_CONTEXT.md`. AGENT.

## Goal

Prove the ANPR platform is still green before adding engines. Capture the skip list. Do not “fix” architecture.

## Agent

1. `cd D:\1_Projects\Research_Ongoing\PRAHARI\02_Code\prahari`
2. Run `.\.venv\Scripts\python.exe -m pytest -q`. If venv missing, create it from `requirements.txt` and re-run.
3. Write `05_Output/experiments/PREFLIGHT.md` with: date, pytest summary, every SKIP reason, `python scripts/audit_gate.py` output.
4. Create `05_Output/experiments/EXPERIMENT_LOG.md` with a one-line header: `# PRAHARI experiment log` and a table header `id|utc|label|ok|skipped|metrics`.
5. Grep `02_Code/prahari/app/services` for `face`, `FRS`, `detect_objects`. Record in PREFLIGHT.md that they are absent (expected).
6. Do not edit product code in this phase unless pytest is red for a reason you introduced earlier. If an existing test is red, fix only that regression and stop.

## Done when

- PREFLIGHT.md exists.
- pytest is green or only skips with explicit reasons (Tesseract missing is allowed).
- audit_gate prints PASS.
- CSV C00-001..004 DONE.

## Do not

Add FRS or objects here. Touch the nested `PRAHARI/PRAHARI/` copy. Commit `.env`.
