# Start here — PRAHARI closeout (04–07 Sep 2026)

**Today.** 04 September 2026.  
**Phase 1 lock.** 07 September 2026 12:00 IST.  
**Official page.** https://sentinel.gujarat.gov.in/problems  
**This book.** Remaining work to make every official submission point, every evaluation area, and every experiment honest, tested, and demoable.

P00–P12 built the ANPR platform. A00–A08 locked secrets, path jail, HLS origin, HMAC, claims. **This book does not rebuild those.** It closes gaps the earlier books deferred: Facial Recognition (lawful gallery), object detection, person/vehicle analytics, intrusion, thorough experiments, and the human submission packet.

## Read in this order

1. `00_MASTER_CONTEXT.md` (paste at the top of every agent session)
2. `02_POINT_BY_POINT_AUDIT.md` (needed / done / pending for every official sentence)
3. `04_ANALYTICS_CONTRACT.md` (event JSON, FRS law, matcher rules)
4. `03_TEST_AND_EXPERIMENT_CATALOGUE.md` (every test and soak)
5. `01_HOW_TO_EXECUTE.md` (day map, gates, parallel tracks)
6. `csv/closeout_actions.csv` (tick list)
7. Exactly one `phases/C*.md` per conversation

## Hard order (do not skip gates)

```
C00  preflight: pytest green, audit_gate PASS, freeze hybrid + GJ01AB1234
C01  event schema: entity_type / face_id / object_class without breaking plate fields
C02  object detection: person, vehicle, bicycle, motorcycle, bus, truck
C03  FRS lawful gallery: enrolled consented adults OR synthetic fixtures; never on gov CCTV
C04  intrusion: person-in-ROI on CAM-FCS-001
C05  watchlist matcher: plate OR face_id OR entity_id; person row WL-004 actually fires
C06  ANPR hardening: Tesseract on PATH, synthetic + own-feed stills, no confirm-only claim
C07  analytics UI: Analytics tab shows plates, faces, objects, intrusion; reports CSV
C08  experiment harness: scripts/run_experiments.py writes MEASURED logs
C09  own-feed + gov-feed experiments (live consume; no wget of /stream)
C10  scale bench: 1 fps, MAX_OPEN_CAPTURES, labelled DESIGN TARGET vs MEASURED
C11  security + privacy tests (FRS never on unknown public faces)
C12  HLD + slides + notes patched to match implemented analytics
C13  HUMAN: own-feed video, gov-feed video, Drive CSV
C14  HUMAN: incognito, portal, freeze
```

C13 videos are **submission blockers**. C02–C07 may run in parallel with C13 rehearsal, but a video of a mock UI is a disqualification. Record against a running backend with rows in `prahari.db`.

## What this book is not

- Not a rebuild of FastAPI, Leaflet, catalogue, HLS proxy, RBAC, or the seeded GJ01AB1234 track.
- Not a Model 4 central VMS.
- Not a live VAHAN / eGujCop / AFIS / NAFIS pipe.
- Not wild-surveillance FRS on Paldi Circle or any government camera of unknown people.
