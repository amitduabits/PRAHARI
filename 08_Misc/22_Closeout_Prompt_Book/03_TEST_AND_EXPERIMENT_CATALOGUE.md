# Test and experiment catalogue

Every official requirement maps to at least one **automated test** and, where the sandbox or a clip is involved, one **MEASURED experiment**. Labels: MEASURED, DESIGN TARGET, CONJECTURED.

Run from `02_Code/prahari`:

```
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts\run_experiments.py --suite smoke
.\.venv\Scripts\python.exe scripts\audit_gate.py
```

Experiment logs land in `05_Output/experiments/` as Markdown + JSON. Never commit secrets.

---

## A. Automated pytest (must stay green)

Existing tests keep their names. New files are listed as NEW.

### A1. Health, boot, seed

| ID | File | Asserts | Official map |
|---|---|---|---|
| T-H01 | `test_health.py` | `/api/health` 200, cameras ≥ 11 | Platform |
| T-H02 | existing seed | watchlist ≥ 5, detections ≥ 6 | Test case |
| T-H03 NEW | `test_event_schema.py` | detections table has entity_type, face_id, object_class; old plate columns still present | HLD 2.5 |

### A2. Registry, GIS, onboarding

| ID | File | Asserts | Official map |
|---|---|---|---|
| T-C01 | `test_cameras.py` | CSV import, Dahod offline, FCS short retention | Model 1 |
| T-C02 | `test_cameras.py` | Private-Permitted without consent → 400 | Security |
| T-C03 | `test_cameras.py` | sync-catalogue without host → 400 naming SENTINEL_HOST | Gov feed |
| T-C04 | `test_catalogue.py` | fixture JSON maps to camera dicts | Integrator |
| T-C05 | `test_tabs_smoke.py` | `/` and list APIs as judge | Presentation |

### A3. Viewer and capture laws

| ID | File | Asserts | Official map |
|---|---|---|---|
| T-V01 | `test_no_rtsp_leak.py` | no `rtsp://` in browser JSON / static | Security |
| T-V02 | `test_path_jail.py` | crop/stream paths cannot escape data dir | Security |
| T-V03 | `test_integrator_laws.py` | TCP flag, no CAP_PROP_FPS, backoff, no publish | Integrator §4 |
| T-V04 | `test_scene_cut.py` | PTS rewind calls on_scene_cut | Integrator |
| T-V05 NEW | `test_scene_cut.py` | on_scene_cut clears object and face track_ids | Eval 05 tracking |
| T-V06 | `test_security.py` | expired HLS token 401 | Security |

### A4. ANPR (mandatory)

| ID | File | Asserts | Official map |
|---|---|---|---|
| T-A01 | `test_plate_normaliser.py` | `GJ 01 AB 1234` → `GJ01AB1234`; reject junk | ANPR |
| T-A02 | `test_anpr_synthetic.py` | recognize fixture or skip if no Tesseract | ANPR |
| T-A03 | `test_anpr_synthetic.py` | confirm inserts detection, plate normalised | Demo safety |
| T-A04 NEW | `test_anpr_synthetic.py` | confirm is audited; confidence 1.0; matcher fires CRITICAL for GJ01AB1234 | Alerts |
| T-A05 NEW | `test_anpr_negative.py` | below ANPR_MIN_CONFIDENCE → inserted False | Quality |
| T-A06 NEW | `test_anpr_negative.py` | empty image 400; unknown camera 404 | Robustness |
| T-A07 NEW | `test_anpr_variants.py` | hyphenated, lowercase, extra spaces still normalise | Indian plates |

### A5. Object detection (eval 05)

| ID | File | Asserts | Official map |
|---|---|---|---|
| T-O01 NEW | `test_objects.py` | fixture PNG with a large “person-coloured” rectangle returns class person **or** documented fallback | Person detection |
| T-O02 NEW | `test_objects.py` | empty / noise image returns [] not crash | Robustness |
| T-O03 NEW | `test_objects.py` | classes mapped to {person,car,motorcycle,bus,truck,bicycle}; others dropped | Object detection |
| T-O04 NEW | `test_objects.py` | `POST /api/ingest/analyse` inserts entity_type=object rows | API |
| T-O05 NEW | `test_objects.py` | `GET /api/objects/report.csv` has camera_id, ts, object_class, confidence | Output report |
| T-O06 NEW | `test_objects.py` | OBJECT_ENGINE=yolo without weights does not crash; falls back | Swap |

### A6. FRS lawful gallery (HLD 2.5, bonus)

| ID | File | Asserts | Official map |
|---|---|---|---|
| T-F01 NEW | `test_faces.py` | two synthetic gallery fixtures: same id matches, other id rejects | Recognition |
| T-F02 NEW | `test_faces.py` | enroll via API creates files under data/faces/ | Watchlist persons |
| T-F03 NEW | `test_faces.py` | match on CAM-OWN-001 inserts entity_type=person, face_id=WL-004, alert HIGH | WL-004 |
| T-F04 NEW | `test_faces.py` | analyse with faces engine on camera_id=`cam04` returns zero face events | FRS law |
| T-F05 NEW | `test_faces.py` | analyse on ownership=Gov returns zero face events even if engine listed | FRS law |
| T-F06 NEW | `test_faces.py` | confirm-face audited, confidence 1.0 | Demo safety |
| T-F07 NEW | `test_faces.py` | GET /api/faces/gallery does not include embedding bytes | Privacy |
| T-F08 NEW | `test_faces.py` | unknown face → detection with face_id empty, no alert | Negative |

### A7. Intrusion (eval 05)

| ID | File | Asserts | Official map |
|---|---|---|---|
| T-I01 NEW | `test_intrusion.py` | person bbox overlapping CAM-FCS-001 ROI → entity_type=intrusion, CRITICAL | Godown |
| T-I02 NEW | `test_intrusion.py` | person outside ROI → no intrusion | Negative |
| T-I03 NEW | `test_intrusion.py` | missing ROI → no crash, no event | Robustness |
| T-I04 NEW | `test_intrusion.py` | 120 s dedupe on same camera | Alerts |

### A8. Watchlist, alerts, track

| ID | File | Asserts | Official map |
|---|---|---|---|
| T-W01 | `test_matcher.py` | stolen CRITICAL, 120 s dedupe, unknown plate none | Alerts |
| T-W02 NEW | `test_matcher.py` | person face_id match; empty plate does not block | Wanted/missing |
| T-W03 NEW | `test_matcher.py` | BLACKLIST GJ05CD5678 is HIGH | Watchlist |
| T-W04 | `test_track.py` | six seed cameras in order; CSV ≥ 7 lines | Test case |
| T-W05 | `test_track.py` | extra insert does not drop seed-1 | Live append |
| T-W06 NEW | `test_track.py` | confirm of a new Indian plate creates a one-point track | Finale designated plate |
| T-W07 NEW | `test_alerts_ws.py` | WS receives CRITICAL payload (TestClient websocket) | Real-time |

### A9. Security, RBAC, privacy

| ID | File | Asserts | Official map |
|---|---|---|---|
| T-S01 | `test_security.py` | unauthenticated /api/cameras 401; health public | Security |
| T-S02 | `test_security.py` | home.viewer hides mall | RBAC |
| T-S03 | `test_security.py` | auditor cannot POST watchlist | RBAC |
| T-S04 NEW | `test_security.py` | dept_viewer cannot enroll faces | Privacy |
| T-S05 NEW | `test_security.py` | auditor cannot confirm-face | RBAC |
| T-S06 | `test_path_jail.py` | unchanged | S2 |
| T-S07 NEW | `test_privacy_frs.py` | grep services: no face engine call when camera_id matches `^cam\d+` | FRS law |

### A10. Claims and honesty

| ID | File | Asserts | Official map |
|---|---|---|---|
| T-K01 | `scripts/audit_gate.py` | PASS | A08 |
| T-K02 NEW | `test_honesty.py` | confirm events cannot be labelled source=anpr | Eval 05 |
| T-K03 NEW | `test_honesty.py` | 80k string in static footer still contains DESIGN TARGET | Scale |

---

## B. Experiment protocols (MEASURED)

`scripts/run_experiments.py` implements these. Each run writes `05_Output/experiments/{id}_{utc}.json` and appends `EXPERIMENT_LOG.md`.

### B1. ANPR quality

| Exp | Input | Procedure | Pass | Label |
|---|---|---|---|---|
| E-A1 | `tests/fixtures/plate_gj01ab1234.png` | recognize() | plate == GJ01AB1234 **or** skip+confirm path documented | MEASURED |
| E-A2 | 8 stills from `own_feed.mp4` at t=0,10,20,… | sampler + recognize | log plates, confidences, crop paths | MEASURED |
| E-A3 | `grab_frame.py --camera-id cam04` | recognize on live frame | log plate or none honestly | MEASURED |
| E-A4 | blur / downsample / invert of fixture | recognize | expected drop; no crash | MEASURED |
| E-A5 | confirm GJ01AB1234 on cam04 | POST confirm | row in detections + CRITICAL alert | MEASURED |

### B2. Objects

| Exp | Input | Procedure | Pass | Label |
|---|---|---|---|---|
| E-O1 | fixture person PNG | detect | ≥1 person | MEASURED |
| E-O2 | own_feed frame | detect | log classes; 0 is allowed if clip has no COCO objects | MEASURED |
| E-O3 | cam04 frame | detect | log classes; FRS not invoked | MEASURED |
| E-O4 | 30 s own_feed at 1 fps | count unique object_class | CSV written | MEASURED |

### B3. FRS (own-feed / fixtures only)

| Exp | Input | Procedure | Pass | Label |
|---|---|---|---|---|
| E-F1 | synthetic gallery | match same vs other | TPR/FPR on fixtures | MEASURED |
| E-F2 | consented team photo vs enrolled | match | hit or confirm-face | MEASURED |
| E-F3 | cam04 frame with faces engine forced | analyse | **zero** face events | MEASURED |
| E-F4 | lighting/shift of synthetic | match confidence drop, no crash | MEASURED |

### B4. Intrusion

| Exp | Input | Procedure | Pass | Label |
|---|---|---|---|---|
| E-I1 | FCS fixture person-in-ROI | check | CRITICAL intrusion | MEASURED |
| E-I2 | FCS fixture person-out | check | no intrusion | MEASURED |

### B5. Watchlist / track / alerts

| Exp | Input | Procedure | Pass | Label |
|---|---|---|---|---|
| E-W1 | GET /api/track/GJ01AB1234 | count ≥ 6, order | MEASURED |
| E-W2 | confirm new plate GJ27XY0001 | OBSERVE alert or none per watchlist | MEASURED |
| E-W3 | two confirms 10 s apart same cam | counter increments, one alert id | MEASURED |
| E-W4 | WS client while confirm | toast payload | MEASURED |

### B6. Government feed soak (integrator)

| Exp | Input | Procedure | Pass | Label |
|---|---|---|---|---|
| E-G1 | GET cameras.json | n cameras, ids logged | MEASURED |
| E-G2 | POST sync-catalogue | upsert count, onboard_failures.md | MEASURED |
| E-G3 | HLS cam04 playlist | HTTP 200, tokenised proxy plays | MEASURED |
| E-G4 | RTSP-TCP grab cam04 | JPEG on disk, pts_ms > 0 | MEASURED |
| E-G5 | second camera different codec if present | grab does not crash | MEASURED |
| E-G6 | 60 s sampler on cam04 | frames kept at ~1 Hz by PTS, not sleep | MEASURED |
| E-G7 | fifth concurrent session | rejected | MEASURED |

If SENTINEL_HOST is empty, E-G* write SKIPPED with that reason. Do not invent ids.

### B7. Scale bench (laptop = MEASURED, 80k = DESIGN TARGET)

| Exp | Procedure | What to record | Label |
|---|---|---|---|
| E-S1 | 1 / 2 / 4 open captures for 60 s | CPU%, RSS, frames, drops | MEASURED |
| E-S2 | mean crop JPEG bytes | bytes | MEASURED |
| E-S3 | `45_000 * crop_bytes * 1 fps` | GB/s | DESIGN TARGET from MEASURED crop size |
| E-S4 | `crop_bytes * 45_000 * 86400 * 7` | storage for 7-day crops | DESIGN TARGET |
| E-S5 | `/api/health` p99 over 100 calls | ms | MEASURED |
| E-S6 | GPU count | 0 on this box | MEASURED; regional GPU remains DESIGN TARGET |

### B8. Security / privacy soak

| Exp | Procedure | Pass | Label |
|---|---|---|---|
| E-X1 | incognito GET /api/cameras | 401 | MEASURED |
| E-X2 | home.viewer cameras | no CAM-MALL-001 | MEASURED |
| E-X3 | grep response of GET /api/cameras/cam04 | no rtsp:// | MEASURED |
| E-X4 | analyse cam04 with ANALYTICS_ENGINES=anpr,objects,faces | face count 0 | MEASURED |

---

## C. Demo acceptance tests (human + agent)

A video is accepted only if all of these are true. Agent writes `05_Output/experiments/DEMO_ACCEPTANCE.md` after watching the file or after the human ticks.

### Own-feed video (≤ 180 s)

- [ ] Running UI at :8080, not Figma
- [ ] Login as judge; no `.env` on screen
- [ ] Operations map + Dahod offline called out
- [ ] Track GJ01AB1234 Reconstruct + CSV
- [ ] Watchlist + CRITICAL alert visible
- [ ] Onboard still: ANPR **or** confirm, labelled honestly
- [ ] If C07 green: objects list and/or enrolled face match on **own** camera
- [ ] Footer 80k DESIGN TARGET spoken
- [ ] A detections row exists in SQLite after the still

### Gov-feed video (≤ 180 s)

- [ ] Cameras table shows catalogue ids (`cam04` etc.)
- [ ] Tile plays HLS; spoken: no coordinates in live JSON
- [ ] No RTSP URL on screen
- [ ] Analytics: plate confirm and/or object CSV; **no FRS**
- [ ] Download CSV with timestamps
- [ ] Alert for GJ01AB1234 if that plate was confirmed
- [ ] Spoken: representative watchlist, not live VAHAN

---

## D. Traceability matrix (requirement → tests → experiments)

| Official atom | Tests | Experiments |
|---|---|---|
| PPT completeness | T-K03, human C12 | — |
| HLD architecture | T-H03, T-V03 | — |
| Heterogeneous onboard | T-C01–C04 | E-G1, E-G2 |
| Live ingest | T-V03, T-V04 | E-G3–G6 |
| Watchlist correlation | T-W01–W03 | E-W1–W4 |
| ANPR | T-A01–A07 | E-A1–A5 |
| FRS | T-F01–F08 | E-F1–F4 |
| Object detection | T-O01–O06 | E-O1–O4 |
| Person/vehicle tracking | T-V05, T-W04–W06 | E-O4, E-W1 |
| Intrusion | T-I01–I04 | E-I1–I2 |
| Alerts workflow | T-W01, T-W07 | E-W3, E-W4 |
| 80k scale | T-K03 | E-S1–S6 |
| Security | T-S01–S07, T-V01–V02 | E-X1–X4 |
| Own-feed demo | demo acceptance | C13 |
| Gov-feed demo + report | T-A03, T-O05 | E-G*, C13 |
| FRS not on gov cameras | T-F04, T-F05, T-S07 | E-F3, E-X4 |
| Integrator §4 | T-V03, T-V04 | E-G4–G6 |

---

## E. How an agent reports an experiment

JSON schema for each run:

```json
{
  "id": "E-A1",
  "utc": "2026-09-04T12:00:00Z",
  "label": "MEASURED",
  "command": "...",
  "input": "tests/fixtures/plate_gj01ab1234.png",
  "ok": true,
  "skipped": false,
  "skip_reason": "",
  "metrics": {"plate": "GJ01AB1234", "confidence": 0.71},
  "notes": ""
}
```

If Tesseract is missing, `ok=false`, `skipped=true`, `skip_reason="tesseract binary absent"`, and E-A5 must still be MEASURED via confirm.
