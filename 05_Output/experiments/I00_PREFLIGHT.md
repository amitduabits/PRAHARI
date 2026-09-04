# I00 preflight — before any Arnav file is copied

**When.** 04 September 2026  
**Cwd.** `02_Code/prahari` with `.\.venv\Scripts\python.exe`  
**Remote.** origin remains `amitduabits/PRAHARI`. Arnav files not copied yet.

## pytest

```
74 passed, 1 skipped in 5.63s
```

Skipped: Tesseract-binary ANPR fixture path (confirm still covers the demo). No failures.

## audit_gate.py

```
PASS S2  resolve_media_path jails to media roots
PASS S3  HLS origin pin present
PASS S4  full HMAC and compare_digest
PASS S5  vendored hls.min.js, no jsdelivr
PASS K1  no live-ministry claims
PASS K3  80k labelled DESIGN TARGET
PASS D3  table open + no-coordinates copy
PASS D2  tesseract on PATH or confirm lock
PASS
```

## GJ01AB1234

`tests/test_track.py` still asserts `GET /api/track/GJ01AB1234` count ≥ 6 in seed order. Not touched in I00.

## Do-not

- Did not clone into `02_Code/prahari`.
- Did not change `origin`.
- Did not copy FaceNet / YOLO / ByteTrack yet (I01).
