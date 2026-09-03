# A03. Pin HLS origin (S3)

Prepend `00_MASTER_CONTEXT.md`. AGENT.

## Goal

`origin_get` must not send the Sentinel cookie to an arbitrary URL an operator pasted into a camera row.

## Agent

1. In `app/services/catalogue.py` add `def origin_allowed(url: str, host: str | None = None) -> bool`:
   - Parse the URL host.
   - Allow if it equals `SENTINEL_HOST` (with or without scheme), or `cctv.corp8.cloud`, or `SENTINEL_RTSP_HOST` for RTSP-related HTTP.
   - Deny everything else.
2. `origin_get` returns a dummy 403 response (or raises) when `origin_allowed` is false. Do not attach cookies to denied URLs.
3. Stream proxy: if origin denied, HTTP 502 with detail `hls origin not pinned`.
4. Test: monkeypatch a camera `hls` to `https://example.invalid/x.m3u8`. Fetching the stream must not call out with the Sentinel cookie. Unit-test `origin_allowed`.
5. `python scripts/audit_gate.py` prints `PASS S3`.
6. `pytest -q tests/test_catalogue.py tests/test_no_rtsp_leak.py` green.

## Done when

- Pin function exists and is used on every `origin_get`.
- CSV A03-001 DONE.

## Do not

Hard-code camera ids. Do not put the access password in tests.
