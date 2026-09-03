# A06. Tesseract or confirm lock (D2, K2)

Prepend `00_MASTER_CONTEXT.md`. HUMAN + agent scripts.

## Goal

Either OCR works on PATH, or every spoken/demo artefact says operator confirm for `cam04`. Never both-and.

## HUMAN (Aria or Lead)

Install Tesseract and put it on PATH **or** skip and accept confirm. Windows: UB Mannheim installer or `choco install tesseract`. Then `tesseract --version`.

## Agent

1. Run `tesseract --version`. Record PRESENT or ABSENT.
2. If PRESENT: run ANPR on `03_Data/recordings/first_live_frame.png` via `POST /api/ingest/frame` with `camera_id=cam04` if the app is up, or via `recognize()` in a short script. If a normalised plate is returned, insert it and regenerate `gov_report.py`. If OCR returns nothing, keep confirm and set spoken lock to confirm.
3. If ABSENT: copy `08_Misc/21_Audit_Remediation/scripts/spoken_own.md` and `spoken_gov.md` over the deliverable scripts:
   - `05_Output/deliverables/own_feed_demo_script.md` must contain the MUST line about operator confirm and must not call the cam04 path ANPR.
   - Same for a new `05_Output/deliverables/gov_feed_demo_script.md` (create from `spoken_gov.md`).
4. `python scripts/audit_gate.py` prints `PASS D2` if either tesseract exists or the gov spoken script contains `operator confirm`.
5. Do not train a detector.

## Done when

- D2 gate PASS.
- CSV A06-001 DONE.

## Do not

Say “ANPR on Paldi” in a video if the CSV confidence is 1.0 from confirm.
