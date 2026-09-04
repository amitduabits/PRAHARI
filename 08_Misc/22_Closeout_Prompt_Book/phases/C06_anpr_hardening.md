# C06 — ANPR hardening and honesty

Prepend `00_MASTER_CONTEXT.md`. AGENT. HUMAN installs Tesseract.

## Goal

Mandatory ANPR is tested on fixtures, own-feed stills, and negatives. Operator confirm cannot be labelled as ANPR.

## Agent

1. `tests/test_anpr_negative.py`:
   - confidence gate: a white PNG with no text → inserted False from /api/ingest/frame
   - unknown camera_id → 404
   - undecodable bytes → 400

2. `tests/test_anpr_variants.py`: normalise cases: `gj-01-ab-1234`, `GJ01 AB1234`, ` GJ01AB1234 `, reject `1234`, reject `G1AB1234`.

3. Add `source` on confirm events: `operator_confirm`. Add `source=anpr` only inside recognize-success insert. `tests/test_honesty.py`: confirm JSON/body stored source != `anpr`.

4. `scripts/grab_own_stills.py`: sample `03_Data/recordings/own_feed.mp4` at 1 fps for 8 frames into `05_Output/experiments/own_stills/`. Run recognize on each; append E-A2 to EXPERIMENT_LOG.md. If Tesseract missing, log SKIPPED and still write the JPEGs.

5. If Tesseract is present, un-skip `test_anpr_synthetic.py` path; if recognize misses the fixture, do **not** force a fake plate. Leave the skip/miss honest.

## HUMAN

Install Tesseract and put it on PATH (UB Mannheim or `choco install tesseract`). `tesseract --version`. Tick C06-001.

## Done when

- new tests green.
- E-A2 row in EXPERIMENT_LOG.md (ok or skipped).
- CSV C06-002..004 DONE. C06-001 HUMAN.

## Do not

Call confirm “ANPR” in CSV or UI. Train a plate detector. Claim cam04 OCR unless recognize actually returned a plate.
