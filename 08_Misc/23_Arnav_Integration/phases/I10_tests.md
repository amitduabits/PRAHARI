# I10 — Full vision test pass

Prepend `00_MASTER_CONTEXT.md`. AGENT. Depends on I02–I08.

## Goal

Default suite still 74+ green without torch. New T-V tests exist. FRS law and GJ01AB1234 untouched.

## Agent

1. Implement any missing T-V01–V11 from `04_TEST_CATALOGUE.md`.
2. `python -m pytest -q`
3. `python scripts/audit_gate.py`
4. `python scripts/run_experiments.py --suite smoke` plus E-V4 cam04 refuse with FACE_ENGINE=facenet if importable else skip.
5. Log in `05_Output/experiments/I10_VISION.md`.

## Done when

- No failed tests. Skips named.
- CSV I10-* DONE.

## Do not

Install torch as a required step to get green CI on a judge laptop.
