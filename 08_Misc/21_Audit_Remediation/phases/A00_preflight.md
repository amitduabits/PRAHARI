# A00. Preflight and audit gate

Prepend `00_MASTER_CONTEXT.md`. First session of this book.

## Goal

Install the machine gate. Prove secrets are gitignored. Do not write product features.

## Agent

1. Confirm `02_Code/prahari/scripts/audit_gate.py` exists (already in tree). If missing, recreate it from the copy in git. The script must:
   - Scan source for S2 jail (`resolve_media_path` rejects paths outside allowed roots).
   - Scan source for S3 host pin (HLS origin fetch checks `SENTINEL_HOST`).
   - Scan source for S4: `hexdigest()` used without `[:32]` in `app/auth.py`; `compare_digest` in `lookup_user`.
   - Scan `app/static/index.html` for `jsdelivr` (must be absent) and `app/static/hls.min.js` (must exist) for S5.
   - Scan demo scripts / HLD / slides / notes for K1 needles (`integrated with VAHAN`, `live VAHAN`, `live eGujCop`) and K3 (the string `80,000` or `80{,}000` must sit within 80 characters of `DESIGN TARGET` or `design target`).
   - Scan UI `app.js` for D3: a branch when `lat === 0 && lon === 0` that still allows table open.
   - Print one line per ID: `PASS` or `FAIL` plus a short reason.
   - Exit 1 if any of S2 S3 S4 S5 K1 K3 fail. D2 is informational (`tesseract` binary). S1 is informational (does not read `.env` values into stdout).
2. Run `git check-ignore -v 02_Code/prahari/.env` and `git check-ignore -v "Screenshot 2026-09-03 111443.png"`. Both must match `.gitignore`.
3. Run `python -m pytest -q` from `02_Code/prahari`. Record the count.
4. Do not fix FAIL rows in this session. Report them. A02–A08 own the fixes.

## Done when

- `scripts/audit_gate.py` exists and runs.
- Ignore checks printed.
- CSV row A00-001 DONE.

## Do not

Read `.env` into the chat. Print `SENTINEL_PASSWORD`. Commit the screenshot.
