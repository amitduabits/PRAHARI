# C12 — HLD, slides, spoken scripts

Prepend `00_MASTER_CONTEXT.md`. AGENT. Depends on C02–C05 actually existing in code. If a capability is not merged, do **not** claim it.

## Goal

Documents match the running platform. Official HLD bullet on ANPR/FRS/object/person tracking is answered. Claims stay honest.

## Agent

1. Rewrite `04_Documents/PRAHARI_HLD.md` §6:
   - Phase-1 implemented: ANPR (Tesseract + confirm), object detection (CPU DNN or fixture fallback), intrusion on CAM-FCS-001, lawful FRS enrolled gallery on Own cameras.
   - FRS law paragraph (never on government CCTV of unknown people; not AFIS/NAFIS).
   - Production swap: YOLO/PaddleOCR, regional GPU 1 fps, dedicated FRS cameras Phase-2, AFIS/NAFIS API Phase-2.
   - Vehicle tracking in the PoC = plate sightings + optional object track_id on a single camera. Cross-camera remains plate-based (evaluation test).

2. Architecture ASCII in §3: change `ANPR / object worker` to `analyse(): ANPR + objects + lawful FRS`.

3. §13 evaluation table: add rows for objects CSV, intrusion, FRS own-feed.

4. `04_Documents/bits-tex/slides.tex` ANPR frame: add one frame “Detection and recognition” with three bullets: plates, objects/intrusion, enrolled-gallery FRS (own-feed). Keep DESIGN TARGET on 80k. Rebuild: `pdflatex slides.tex` twice, copy PDF to `04_Documents/PRAHARI-Slides.pdf` and `docs/`.

5. `notes.tex`: replace “Face recognition is not the demo” with “Face recognition in this PoC is an enrolled gallery on own cameras, never on government CCTV of unknown people.” Rebuild notes similarly.

6. Update `05_Output/deliverables/own_feed_demo_script.md` with a 15 s slot for Analyse still (objects + optional face) **without** cutting the GJ01AB1234 reconstruct. Keep ≤3 min: shorten Gaps if needed.

7. Gov script: add “object boxes or object CSV” if E-O3 produced classes. Explicit MUST: we do not run FRS on this feed.

8. Patch `08_Misc/21_Audit_Remediation/scripts/forbidden_claims.md`:
   - Forbidden remains: live VAHAN, downloaded mp4, 80k as laptop fact, ANPR on cam04 unless OCR.
   - Replace “face recognition | not in this PoC” with “face recognition on government CCTV | enrolled gallery on own-feed only, never Paldi Circle”.
   - Allowed sentence: the notes FRS-law sentence.

9. Run audit_gate.py. Must PASS.

10. HLD_CHANGELOG.md one paragraph for this cycle.

## Done when

- HLD §6 names implemented engines.
- Slides/notes PDFs rebuilt if tex changed.
- Spoken scripts mention objects; gov script forbids FRS.
- CSV C12-001..004 DONE.

## Do not

Add FRS screenshots from cam04. Soften “representative watchlist”. List Kafka as a running component.
