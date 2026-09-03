# A02. Jail file-protocol paths (S2)

Prepend `00_MASTER_CONTEXT.md`. AGENT.

## Goal

A write-role user cannot point `protocol=file` at an arbitrary filesystem path and fetch it via `/api/stream`.

## Agent

1. Change `app/paths.py` `resolve_media_path`:
   - Resolve the path.
   - Allowed roots: `config.ROOT / "data"` and `config.SAMPLES_DIR` and `config.REPO_ROOT / "03_Data"`.
   - After resolve, require `allowed in path.parents or path == allowed` for at least one allowed root.
   - If not, raise `ValueError("file url outside media roots")`.
2. In `app/routers/stream.py` file branch: catch that error and return HTTP 400.
3. Add `tests/test_path_jail.py`:
   - Onboard (as judge) a camera `CAM-JAIL` with `protocol=file`, `url=../../../../Windows/win.ini` or `/etc/passwd` relative form, `lat=23`, `lon=72`, `consent=true`.
   - `GET /api/stream/{id}?token=` must not return file contents of the OS file. Expect 400 or 404.
   - Own-feed `CAM-OWN-001` still 200 when `own_feed.mp4` exists, or 404 with the honest drop-file message when missing.
4. `pytest -q tests/test_path_jail.py tests/test_security.py tests/test_no_rtsp_leak.py` green.
5. `python scripts/audit_gate.py` must print `PASS S2`.

## Done when

- Jail in `resolve_media_path`.
- Test exists and passes.
- CSV A02-001 DONE.

## Do not

Block HLS/RTSP. Do not store absolute Windows paths in the sample CSV.
