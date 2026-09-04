# PRAHARI

Statewide CCTV intelligence plane for the Gujarat Police Innovation Challenge 2026. Hybrid Models 1 (registry + GIS) + 2 (unified viewing + ANPR) + thin 3 (event bus). Model 4 central VMS is Phase-2, not this PoC.

PRAHARI **consumes live streams** (RTSP-TCP, HLS, WHEP) from the Sentinel catalogue `GET /cameras.json` (session cookie). It does **not** download sandbox footage. `/stream/<id>` range-requests are not a dataset.

## Judge guide (10 lines)

1. `cd 02_Code/prahari` then `.\run.ps1`
2. Open http://127.0.0.1:8080
3. Sign in as `judge` / `JUDGE_PASSWORD` from `.env` (default in `.env.example` is `set-this-before-submit`; change before submit)
4. Operations: Gujarat map, coloured health pins
5. Vehicle Track: plate `GJ01AB1234` → Reconstruct → Download CSV
6. Alerts: CRITICAL stolen queue, Ack
7. Onboard: ANPR this still, Analyse this still (objects / own-feed faces), or Operator confirm
8. Analytics & Gaps: Dahod offline, short retention
9. Do not expect raw `rtsp://` in the browser; tiles are tokenised
10. `SENTINEL_HOST` empty is valid: sample cameras still run

## Run

```powershell
cd D:\1_Projects\Research_Ongoing\PRAHARI\02_Code\prahari
.\run.ps1
```

Copy `.env.example` to `.env` and set `JUDGE_PASSWORD`. Set `SENTINEL_HOST`, `SENTINEL_PASSWORD`, and `SENTINEL_RTSP_HOST` after the live portal login. The app still boots on sample cameras if those are empty.

Tesseract OCR (optional; confirm path covers the demo): `choco install tesseract` or the UB Mannheim installer, then ensure `tesseract` is on PATH.

## Sentinel ingest

Force TCP when you open a sandbox camera yourself:

```
ffplay -rtsp_transport tcp rtsp://103.250.160.189:8554/stream/cam04
ffplay https://cctv.corp8.cloud/cam04/index.m3u8
```

HLS on the TLS host needs the access cookie and a browser User-Agent. If 8554 is blocked, use HLS.

| Official checklist | Code |
|---|---|
| RTSP over TCP | `app/services/capture.py`, `scripts/grab_frame.py` |
| No CAP_PROP_FPS timing | `app/services/sampler.py`, `capture.py` |
| Gaps are not disconnects | `StreamSession.read` |
| Backoff 2–30 s | `backoff_sleep` |
| Decode warnings non-fatal | logged in `capture.py` |
| Catalogue `/cameras.json` | `app/services/catalogue.py` |
| Mixed codecs/resolutions | per-camera fields |
| Scene cut at loop | `detect_scene_cut` |

WHEP preview is a P1 link-out, not a full WebRTC stack in this PoC.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts\run_experiments.py --suite smoke
```

Logs: `../../05_Output/experiments/`. Government suite SKIPPED if `SENTINEL_HOST` is empty.

Integrator guide: https://sentinel.gujarat.gov.in/resource
