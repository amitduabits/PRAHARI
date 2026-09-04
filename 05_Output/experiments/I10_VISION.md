# I10 vision test pass

**When.** 04 September 2026  
**Cwd.** `02_Code/prahari` with `.\.venv\Scripts\python.exe`  
**Torch.** Not installed (on purpose). Default engines must stay green.

## pytest

```
88 passed, 4 skipped in 7.16s
```

Skipped (named):

| File | Reason |
|---|---|
| `test_anpr_synthetic.py` | Tesseract binary not installed |
| `test_bytetrack_optional.py` (T-V06) | ultralytics ByteTrack missing |
| `test_facenet_optional.py` (T-V03) | torch+facenet-pytorch not installed |
| `test_yolo_optional.py` (T-V05) | ultralytics or yolov8n.pt missing |

T-V01, T-V02, T-V04, T-V07, T-V08, T-V09, T-V10, T-V11 passed on the default path.

## audit_gate.py

PASS (S2–S5, K1, K3, D3, D2).

## smoke + E-V

`scripts/run_experiments.py --suite smoke`

| id | ok | skipped |
|---|---|---|
| E-A1 | true | true (Tesseract) |
| E-O1 | true | false |
| E-F1 | true | false |
| E-I1 | true | false |
| E-W1 | true | false |
| E-V1 | true | false (histogram WL-004) |
| E-V2 | true | true (no torch) |
| E-V3 | true | true (no ultralytics) |
| E-V4 | true | false (cam04 FACE_ENGINE=facenet still refuses faces) |
| E-V5 | true | false (predict list) |

GJ01AB1234 track and FRS-on-Gov refuse remain green.
