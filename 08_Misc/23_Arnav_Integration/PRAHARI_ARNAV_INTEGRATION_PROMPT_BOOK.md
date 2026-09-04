# PRAHARI Arnav engine-pack prompt book

**Fork.** https://github.com/ArAv-1/PRAHARI-3.0  
**Stay on.** https://github.com/amitduabits/PRAHARI  
**Version.** 1.0 · 2026-09-04

C00–C12 stay finished. This book is I00–I12.

## How a session is started

```
[paste 00_MASTER_CONTEXT.md]

Then:

[paste phases/I0N_....md]
```

One conversation per phase. Tick `csv/integration_actions.csv`.

## Phase index

| Phase | File | Builds |
|---|---|---|
| I00 | `phases/I00_preflight.md` | Baseline green |
| I01 | `phases/I01_vendor_layout.md` | `_upstream` copy, `engines/` package, `requirements-vision.txt` |
| I02 | `phases/I02_facenet.md` | FACE_ENGINE=facenet |
| I03 | `phases/I03_frs_law.md` | No FaceAnalyzer on Gov |
| I04 | `phases/I04_yolo.md` | YOLO object + plate crop |
| I05 | `phases/I05_bytetrack.md` | TRACK_ENGINE=bytetrack |
| I06 | `phases/I06_crops_honesty.md` | original/enhanced flags |
| I07 | `phases/I07_enroll_review.md` | Person form, pending_review |
| I08 | `phases/I08_predict.md` | Next-camera API |
| I09 | `phases/I09_query_optional.md` | Keyword filter or skip |
| I10 | `phases/I10_tests.md` | T-V01–V11 |
| I11 | `phases/I11_docs.md` | HLD/slides optional-engine frame |
| I12 | `phases/I12_human.md` | Own-feed FaceNet still |

## Atomic catalogue

See `csv/integration_actions.csv`. IDs `Ixx-nnn`.
