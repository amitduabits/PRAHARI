# PRAHARI closeout prompt book

**Challenge.** Gujarat Police Innovation Challenge 2026  
**Lock.** 07 September 2026 12:00 IST  
**Version.** 1.0 · 2026-09-04

This book is the remaining work. P00–P12 and A00–A08 are finished. Do not rebuild them.

## How a session is started

```
[paste 00_MASTER_CONTEXT.md]

Then:

[paste phases/C0N_....md]
```

One conversation per phase. Tick `csv/closeout_actions.csv`.

Human rows are labelled HUMAN in the phase files. The agent lists them at the end and stops.

## Phase index

| Phase | File | Day | Hours | Builds |
|---|---|---|---|---|
| C00 | `phases/C00_preflight.md` | 04 Sep | 0.5 | pytest + audit_gate baseline |
| C01 | `phases/C01_event_schema.md` | 04 Sep | 1.5 | additive detection/alert/watchlist columns |
| C02 | `phases/C02_object_detection.md` | 04 Sep | 3 | objects.py + tests + CSV |
| C03 | `phases/C03_frs_lawful.md` | 04 Sep | 3 | faces.py + gallery + gov refuse |
| C04 | `phases/C04_intrusion.md` | 04 Sep | 1.5 | person-in-ROI on CAM-FCS-001 |
| C05 | `phases/C05_watchlist_entities.md` | 04 Sep | 1.5 | matcher plate OR face_id |
| C06 | `phases/C06_anpr_hardening.md` | 05 Sep | 2 | Tesseract path, negatives, honesty |
| C07 | `phases/C07_analytics_ui.md` | 05 Sep | 2 | Analyse still, alerts for persons, reports |
| C08 | `phases/C08_experiment_harness.md` | 05 Sep | 2 | run_experiments.py + log |
| C09 | `phases/C09_live_experiments.md` | 05–06 Sep | 2 | own-feed + gov-feed MEASURED |
| C10 | `phases/C10_scale_bench.md` | 06 Sep | 1.5 | MEASURED laptop vs DESIGN TARGET 80k |
| C11 | `phases/C11_security_privacy.md` | 06 Sep | 1 | FRS law tests, RBAC for enroll |
| C12 | `phases/C12_docs.md` | 06 Sep | 2 | HLD §6, slides, spoken scripts |
| C13 | `phases/C13_demos.md` | 05–06 Sep | human | YouTube + Drive |
| C14 | `phases/C14_submit.md` | 07 Sep | human | incognito, portal, freeze |

## Atomic catalogue (IDs match the CSV)

Priority: P0 must-do for first prize or eval 05. P1 should. P2 skip if videos are still missing.

### C00 Preflight

| ID | Pri | Who | Task | Done when |
|---|---|---|---|---|
| C00-001 | P0 | grok | Run pytest -q; record skip list | suite green or only documented skips |
| C00-002 | P0 | grok | Run audit_gate.py | PASS |
| C00-003 | P0 | grok | Confirm no edits under nested PRAHARI/PRAHARI/ | only 02_Code/prahari |
| C00-004 | P0 | grok | Create 05_Output/experiments/ and EXPERIMENT_LOG.md header | folder exists |

### C01 Event schema

| ID | Pri | Who | Task | Done when |
|---|---|---|---|---|
| C01-001 | P0 | grok | ALTER detections/alerts/watchlist additive columns | test_event_schema.py |
| C01-002 | P0 | grok | models.DETECTION_COLUMNS extended; old inserts still work | test_track.py still green |
| C01-003 | P0 | grok | analyse.py stub dispatching to engines from env | importable |

### C02 Object detection

| ID | Pri | Who | Task | Done when |
|---|---|---|---|---|
| C02-001 | P0 | grok | objects.detect() CPU; fixture person PNG | test_objects.py T-O01 |
| C02-002 | P0 | grok | POST /api/ingest/analyse | T-O04 |
| C02-003 | P0 | grok | GET /api/objects/report.csv | T-O05 |
| C02-004 | P0 | grok | scene-cut resets object track_ids | T-V05 |
| C02-005 | P1 | grok | optional YOLO import-guard | T-O06 |

### C03 FRS lawful gallery

| ID | Pri | Who | Task | Done when |
|---|---|---|---|---|
| C03-001 | P0 | grok | faces.match + synthetic gallery fixtures | T-F01 |
| C03-002 | P0 | grok | enroll API + confirm-face | T-F02, T-F06 |
| C03-003 | P0 | grok | refuse faces on cam\d+ and ownership=Gov | T-F04, T-F05 |
| C03-004 | P0 | grok | gallery JSON has no embeddings | T-F07 |
| C03-005 | P0 | aria | HUMAN: 2 consented adult photos | files in 03_Data/samples/faces/ |

### C04 Intrusion

| ID | Pri | Who | Task | Done when |
|---|---|---|---|---|
| C04-001 | P0 | grok | ROI on CAM-FCS-001 extra_json | T-I01 |
| C04-002 | P0 | grok | negative + missing ROI | T-I02, T-I03 |

### C05 Watchlist entities

| ID | Pri | Who | Task | Done when |
|---|---|---|---|---|
| C05-001 | P0 | grok | matcher hits face_id / entity_id | T-W02 |
| C05-002 | P0 | grok | WL-004 fires without a plate | alert row |
| C05-003 | P0 | grok | BLACKLIST plate HIGH | T-W03 |
| C05-004 | P1 | grok | WS test for CRITICAL | T-W07 |

### C06 ANPR hardening

| ID | Pri | Who | Task | Done when |
|---|---|---|---|---|
| C06-001 | P0 | aria | HUMAN: Tesseract on PATH | tesseract --version |
| C06-002 | P0 | grok | negative + variant tests | T-A05–A07 |
| C06-003 | P0 | grok | honesty: confirm cannot be source=anpr | T-K02 |
| C06-004 | P0 | grok | grab own_feed still + analyse | E-A2 logged |

### C07 Analytics UI

| ID | Pri | Who | Task | Done when |
|---|---|---|---|---|
| C07-001 | P0 | grok | Analyse this still on Onboard | UI shows plate/objects/faces |
| C07-002 | P0 | grok | Alerts render name for person hits | no blank plate |
| C07-003 | P0 | grok | Analytics tab object counts + CSV link | clickable |
| C07-004 | P0 | grok | tabs smoke still green | test_tabs_smoke.py |

### C08 Experiment harness

| ID | Pri | Who | Task | Done when |
|---|---|---|---|---|
| C08-001 | P0 | grok | scripts/run_experiments.py --suite smoke | JSON files |
| C08-002 | P0 | grok | EXPERIMENT_LOG.md appended | file |

### C09 Live experiments

| ID | Pri | Who | Task | Done when |
|---|---|---|---|---|
| C09-001 | P0 | grok | E-A* E-O* on own_feed | log |
| C09-002 | P0 | grok | E-G1–G4 if SENTINEL_HOST set else SKIPPED | log |
| C09-003 | P0 | grok | E-F3 refuse faces on cam04 | log |
| C09-004 | P0 | grok | regenerate gov_feed_plates.csv + optional objects CSV | deliverables |

### C10 Scale bench

| ID | Pri | Who | Task | Done when |
|---|---|---|---|---|
| C10-001 | P0 | grok | E-S1–S6 | SCALE_BENCH.md |
| C10-002 | P0 | grok | HLD §5 crop size updated if MEASURED differs >2× | HLD note |

### C11 Security privacy

| ID | Pri | Who | Task | Done when |
|---|---|---|---|---|
| C11-001 | P0 | grok | T-S04 T-S05 T-S07 T-K02 | pytest |
| C11-002 | P0 | grok | audit_gate still PASS | PASS |

### C12 Docs

| ID | Pri | Who | Task | Done when |
|---|---|---|---|---|
| C12-001 | P0 | grok | HLD §6 rewritten: ANPR + objects + lawful FRS | no “FRS not in PoC” |
| C12-002 | P0 | grok | slides/notes AI frames updated; FRS law spoken | pdflatex |
| C12-003 | P0 | grok | own/gov demo scripts updated | files |
| C12-004 | P0 | grok | forbidden_claims.md allows lawful FRS sentence | A08 still PASS |
| C12-005 | P1 | lead | HUMAN: PPT export if Beamer is the submitted deck | PDF copy |

### C13 Demos (HUMAN)

| ID | Pri | Who | Task | Done when |
|---|---|---|---|---|
| C13-001 | P0 | lead | preflight_demo.ps1 PASS | PASS |
| C13-002 | P0 | lead | own-feed ≤3 min Unlisted YT | URL |
| C13-003 | P0 | lead | gov-feed ≤3 min Unlisted YT | URL |
| C13-004 | P0 | lead | Drive Anyone+Viewer CSV | URL |
| C13-005 | P0 | grok | DEMO_ACCEPTANCE.md ticked from script | file |

### C14 Submit (HUMAN)

| ID | Pri | Who | Task | Done when |
|---|---|---|---|---|
| C14-001 | P1 | lead | hosted URL only if audit_gate PASS and passwords rotated | optional |
| C14-002 | P0 | arnav | push main | GitHub |
| C14-003 | P0 | lead | portal before 12:00 IST | receipt png |
| C14-004 | P0 | lead | incognito all links | checklist |
| C14-005 | P0 | all | finale bag after shortlisting | bag |

## Already finished (do not rebuild)

Working tree `02_Code/prahari/`. GitHub live. Seeded track. Hybrid HLD. Integrator static tests. Catalogue sync of 30 cameras. Operator confirm on cam04. RBAC. Path jail. HMAC. Claims lock for live VAHAN. Registration.

## First-prize non-negotiables (unchanged)

1. Own-feed video is a running UI with a detection row in the database.
2. Gov-feed video shows a Sentinel camera from the live catalogue, not a wget of `/stream/<id>`.
3. RTSP over TCP; HLS if 8554 blocked.
4. Event time is PTS.
5. `GJ01AB1234` reconstructs Valsad to Gandhinagar.
6. Links work logged-out.
7. Submit before 12:00 IST on 07 Sep.

Plus this book:

8. FRS never runs on government CCTV of unknown people.
9. Confirm rows are never labelled as ANPR.
10. Eval 05 engines (objects, intrusion, lawful FRS) have pytest + a MEASURED log, or the docs do not claim them.
