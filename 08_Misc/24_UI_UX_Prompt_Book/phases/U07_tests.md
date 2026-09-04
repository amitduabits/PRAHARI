# U07 — Tests and score

AGENT. Depends on U01–U06.

## Goal

Anti-slop tests green. Audit score ≥ 40 / 48. pytest and audit_gate still PASS.

## Agent

1. Add `tests/test_ux_duty_desk.py` and `tests/test_ux_contrast.py` as specified in `04_QUANTIFIED_BAR.md`.
2. `python -m pytest -q`
3. `python scripts/audit_gate.py`
4. Re-score `02_CURRENT_AUDIT.md` into `05_Output/experiments/U07_UX.md`.
5. Tick U07-001.

## Do not

Install axe-core as a required CI package if it needs npm. Hex math in pytest is enough. Skip Lighthouse unless the machine has Chrome already.
