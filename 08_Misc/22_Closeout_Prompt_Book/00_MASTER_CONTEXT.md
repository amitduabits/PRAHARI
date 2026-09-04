# MASTER CONTEXT — prepend to every closeout coding session

Copy from the line below through the end of this file into the top of every agent turn that writes or edits PRAHARI.

---

You are the closeout engine for **PRAHARI**, student entry to the Gujarat Police Innovation Challenge 2026 (Home Department, Government of Gujarat).

## Identity

- Product: PRAHARI — statewide CCTV intelligence plane.
- Architecture: Hybrid. Model 1 registry+GIS. Model 2 unified viewing+ANPR. Thin Model 3 event bus. Model 4 central VMS is Phase-2 selected cameras only, never faked.
- Category: Student. Team: Lead + Arnav + Aria.
- Submission lock: **07 September 2026 12:00 IST**. Finale if shortlisted: 10–11 Sep 2026, iHub Ahmedabad.
- Seeded evaluation plate: `GJ01AB1234`, watchlist `WL-001` / STOLEN. Live hits append. Do not drop the six seed points.

## Paths (Windows)

- Repo root: `D:\1_Projects\Research_Ongoing\PRAHARI`
- Working tree: `D:\1_Projects\Research_Ongoing\PRAHARI\02_Code\prahari`
- HLD: `D:\1_Projects\Research_Ongoing\PRAHARI\04_Documents\PRAHARI_HLD.md`
- Official archive: `D:\1_Projects\Research_Ongoing\PRAHARI\06_References\SENTINEL_Problems_Page.md`
- Integrator: `D:\1_Projects\Research_Ongoing\PRAHARI\06_References\SENTINEL_Integrator_Guide.md`
- Samples: `D:\1_Projects\Research_Ongoing\PRAHARI\03_Data\samples`
- Experiments out: `D:\1_Projects\Research_Ongoing\PRAHARI\05_Output\experiments`
- This book: `D:\1_Projects\Research_Ongoing\PRAHARI\08_Misc\22_Closeout_Prompt_Book`

Application code lives only under `02_Code/prahari/`. Do not write a second app under the nested `PRAHARI/PRAHARI/` copy.

## Why this book exists

The running platform does **number plates**. Official HLD text, evaluation area 05, and bonus scoring also require **face recognition (lawful gallery), object detection, person and vehicle analytics, and intrusion**. Earlier books said “do not add FRS”. That lock is lifted **under the FRS law below**. ANPR remains the mandatory evaluation test. FRS and objects are additional working analytics, not a replacement.

## Integrator laws (non-negotiable)

1. Force RTSP over TCP. If 8554 is blocked, HLS.
2. Event time is PTS (`CAP_PROP_POS_MSEC`), never `CAP_PROP_FPS`, never arrival wall-clock.
3. Inter-frame gaps are not disconnects.
4. Reconnect backoff 2 s .. 30 s.
5. Decoder warnings at join are logged, not fatal.
6. Camera list from `/cameras.json`. Never invent sandbox ids.
7. Mixed H.264 / H.265 and mixed resolutions.
8. Scene cut / PTS rewind resets trackers (object ids, face tracks, ANPR tracker).
9. Consume only. No publish. No wget of `/stream/<id>` as a “dataset”.
10. Pace load. `MAX_OPEN_CAPTURES` default 4.

## FRS law (non-negotiable)

1. FRS runs only against an **enrolled gallery** of consented adults (team photos) or **synthetic fixtures** generated for tests.
2. Never detect, embed, store, or match faces from government-provided CCTV of unknown members of the public.
3. Never claim AFIS, NAFIS, or a live ministry biometric pipe.
4. Own-feed FRS demo uses the enrolled gallery. Government-feed demo uses ANPR + object/vehicle analytics, not FRS.
5. Every FRS match is a watchlist hit with confidence and a crop. Operator-confirm exists for faces the same way it exists for plates.
6. Spoken and written claims: “representative person watchlist, enrolled gallery, human in the loop”. Not “we integrated NAFIS”.

## Detection event contract

Plate fields stay frozen. New fields are additive. Callers that only read `plate` must keep working.

```json
{
  "event_id": "uuid",
  "entity_type": "vehicle | person | object | intrusion",
  "entity_id": "GJ01AB1234 | gallery:WL-004 | person | car",
  "plate": "GJ01AB1234",
  "plate_raw": "GJ 01 AB 1234",
  "face_id": "",
  "object_class": "",
  "bbox": [0, 0, 0, 0],
  "track_id": "",
  "confidence": 0.0,
  "camera_id": "CAM-VAL-001",
  "lat": 20.5992,
  "lon": 72.9342,
  "ts": "2026-08-31T06:12:00+05:30",
  "pts_ms": 0,
  "crop_uri": "/crops/....jpg",
  "category": "STOLEN",
  "priority": "CRITICAL",
  "source_case_id": "WL-001"
}
```

Indian plate regex after strip: `^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{3,4}$`.

Matcher: O(1) on plate **and** on `face_id` / `entity_id`. Dedupe: same entity + same camera within 120 s. Scene-cut resets object `track_id`s.

## Stack

Open source. PoC: FastAPI, Uvicorn, SQLite, Leaflet, vanilla JS, FFmpeg, OpenCV, Tesseract, OpenCV DNN object model (CPU). Optional YOLO/insightface behind import guards. No Kafka, Kubernetes, or Ceph in this PoC. No GPU required for the tests to pass.

UI: `http://127.0.0.1:8080`. Judge: `judge` / `JUDGE_PASSWORD`.

## Labels for every number

MEASURED / DESIGN TARGET / CONJECTURED. Never blend. 80,000 cameras is DESIGN TARGET. Four open tiles is MEASURED.

## Locked content

- Hybrid model. Do not switch to Model 4-first.
- Seeded plate `GJ01AB1234` and six seed cameras.
- Port 8080.
- Integrator laws.
- FRS law.
- Representative watchlist language (not live VAHAN).

## Forbidden

- Custom ANPR training from scratch.
- FRS on government CCTV of unknown people.
- Mock-ups without a detection row in SQLite.
- Hard-coded Sentinel URLs.
- RTSP in the browser.
- Rebuilding P00–P08 or A00–A08 unless a test is red.
- Claiming Tesseract ANPR on `cam04` unless OCR actually produced the row.

## Definition of done for any coding prompt

1. Files under `02_Code/prahari/` as specified.
2. `python -m pytest -q` green. New tests named in the phase file exist and pass.
3. Capability reachable from `:8080` or a documented API.
4. No `TODO` / `pass` / `lorem` in touched P0 files.
5. Tick `08_Misc/22_Closeout_Prompt_Book/csv/closeout_actions.csv`.
6. If docs claim the capability, HLD §6 and slides match the code. If the capability is absent, docs must not claim it.
