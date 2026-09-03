# A12. Preserve prahari.db (D4)

Prepend `00_MASTER_CONTEXT.md`. AGENT + HUMAN.

## Goal

Stage demo does not wipe the eight-point `GJ01AB1234` track.

## Agent

1. `FINALE_RUNCARD.md`: add a line **Do not delete `data/prahari.db`. Do not re-run first-boot seed if the file exists.** Confirm `app/db.py` seeds only when tables are empty (already true). Do not change that.
2. Add a one-line check in `scripts/preflight_demo.ps1`: detections ≥ 6 still.
3. Pack list in runcard already includes `prahari.db`. Keep it.

## HUMAN

Copy `02_Code/prahari/data/prahari.db` onto both finale laptops. Do not regenerate from CSV on the train.

## Done when

- Runcard forbids wipe.
- CSV A12-001 DONE.

## Do not

`del prahari.db` as a troubleshooting step in any README.
