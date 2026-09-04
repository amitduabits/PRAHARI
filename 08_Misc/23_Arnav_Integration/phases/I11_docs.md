# I11 — Docs: next engine layer

Prepend `00_MASTER_CONTEXT.md`. AGENT. Depends on I10.

## Goal

HLD and slides describe optional FaceNet/YOLO/ByteTrack. They do not rename the product. Claims lock holds.

## Agent

1. HLD §6: add “Optional vision engines (Arnav pack): FaceNet when FACE_ENGINE=facenet; YOLO when OBJECT_ENGINE/ANPR_ENGINE=yolo; ByteTrack when TRACK_ENGINE=bytetrack. Default remains histogram + blob + Tesseract + IoU. GPU count MEASURED 0 unless a later bench says otherwise.”
2. FRS law paragraph unchanged.
3. Slides: one new frame “Optional vision engines”. Bullets: FaceNet Own-only; YOLO vehicle/person; ByteTrack; predict next camera; never Paldi FRS; no CodeFormer in this PoC.
4. Notes: one short section, same facts. No live-ministry needle. 80k stays DESIGN TARGET.
5. `pdflatex` notes + slides twice. Copy PDFs to `04_Documents/` and `docs/`.
6. `audit_gate.py` PASS.
7. Credit Arnav in notes team line (already on the title). One sentence: workshop code at ArAv-1/PRAHARI-3.0, production tree remains amitduabits/PRAHARI.

## Done when

- PDFs rebuilt. Gate PASS.
- CSV I11-* DONE.

## Do not

Claim AdaFace. Claim 80k laptop throughput. Point the committee at ArAv-1 as the submission repo.
