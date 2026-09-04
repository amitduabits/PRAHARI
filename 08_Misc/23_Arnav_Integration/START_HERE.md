# Start here — integrate Arnav’s PRAHARI-3.0 as the next engine layer

**Source fork.** https://github.com/ArAv-1/PRAHARI-3.0 (Arnav Aviral, last code 02–03 Sep 2026)  
**Keep working in.** `D:\1_Projects\Research_Ongoing\PRAHARI` (`02_Code/prahari/`)  
**Do not** switch the GitHub remote to ArAv-1. Do not copy his tree over ours.

P00–P12 built the plate plane. A00–A08 locked secrets and claims. C00–C12 added lawful histogram FRS, blob objects, intrusion, and the experiment harness. **This book does not rebuild those.** It cherry-picks Arnav’s FaceNet, YOLO, ByteTrack, next-camera predict, original-crop flags, and person-enroll UI **behind the existing doors**.

## Read in this order

1. `00_MASTER_CONTEXT.md` (paste at the top of every agent session)
2. `02_WHAT_TO_TAKE.md` (take / adapt / refuse)
3. `03_ENGINE_CONTRACT.md` (env engines, FRS law, honest labels)
4. `04_TEST_CATALOGUE.md`
5. `01_HOW_TO_EXECUTE.md`
6. `csv/integration_actions.csv`
7. Exactly one `phases/I*.md` per conversation

## Hard order

```
I00  preflight: 74 pytest green, audit_gate PASS, GJ01AB1234 still six seeds
I01  vendor layout: copy selected files, import-guard torch/ultralytics
I02  FACE_ENGINE=facenet behind faces.match(); histogram remains default
I03  FRS law still refuses cam04 / ownership=Gov (his ingest ran faces on every camera)
I04  OBJECT_ENGINE=yolo + ANPR_ENGINE=yolo behind detect() / recognize()
I05  ByteTrack for object track_id; scene-cut still resets
I06  original crop + is_ai_reconstructed; never name CodeFormer/ESRGAN/AdaFace unless the model file is loaded
I07  pending_review alerts + person enroll form
I08  GET /api/predict/{plate} next-camera (bonus)
I09  optional /api/query labelled rule-based, not NLP
I10  tests: skip without torch/weights; FRS law + plate track still green
I11  HLD + slides: “next engine layer”, DESIGN TARGET, FRS law
I12  HUMAN: own-feed FaceNet still if torch present; never FRS on gov video
```

## Strengths that must survive every phase

- Hybrid Models 1 + 2 + thin 3. Model 4 not faked.
- Sentinel `/cameras.json`, RTSP-TCP, PTS, HLS fallback, no wget of `/stream/<id>`.
- Seeded plate `GJ01AB1234`, six cameras, live hits append.
- Operator confirm `source=operator_confirm`, never labelled ANPR.
- Path jail, HMAC stream tokens, no RTSP in the browser, vendored `hls.min.js`.
- `audit_gate.py` PASS (no live-ministry claims; 80k near DESIGN TARGET).
- FRS never on government CCTV of unknown people.

## What this book is not

- Not a merge of `ArAv-1/PRAHARI-3.0` as the new root.
- Not 3D face reconstruction. His “reconstruction” is same-camera tracklets plus optional upscaled crops for a human.
- Not AdaFace, CodeFormer, or Real-ESRGAN until those weight files exist and load.
- Not wild FRS on Paldi Circle.
