# C00 preflight

**Date.** 2026-09-04  
**Working tree.** `02_Code/prahari`  
**Interpreter.** `02_Code/prahari/.venv/Scripts/python.exe`

## pytest

First run from this tree (after fixing `test_tampered_password_fails_lookup` to use `config.JUDGE_PASSWORD` instead of the pre-rotation default): see C00-001 re-run.

**Initial collection note.** Running pytest from the repo root collects the nested `PRAHARI/PRAHARI/` copy and errors with import-file mismatch. Preflight and all later phases run from `02_Code/prahari` only.

**Final closeout result.** 74 passed, 1 skipped (`test_recognize_or_skip_without_tesseract`). `audit_gate.py` PASS.

**Initial result (before the password-test fix).** 38 passed, 1 skipped, 1 failed.

- SKIP: `test_anpr_synthetic.py::test_recognize_or_skip_without_tesseract` — Tesseract binary not installed (expected).
- FAIL: `test_security.py::test_tampered_password_fails_lookup` — hardcoded `set-this-before-submit` after A01 password rotate. Test updated to `config.JUDGE_PASSWORD`. Product code unchanged.

## audit_gate.py

```
PASS S2 resolve_media_path jails to media roots
PASS S3 HLS origin pin present
PASS S4 full HMAC and compare_digest
PASS S5 vendored hls.min.js, no jsdelivr
PASS K1 no live-ministry claims
PASS K3 80k labelled DESIGN TARGET
PASS D3 table open + no-coordinates copy
PASS D2 confirm lock in spoken script
PASS
```

## Services grep (`face`, `FRS`, `detect_objects`)

Absent as of C00 (expected). Only hit: comment in `anpr.py` (“recognize() is the only AI interface”). C02–C04 add the engines.

## Nested copy

No edits under `PRAHARI/PRAHARI/`.
