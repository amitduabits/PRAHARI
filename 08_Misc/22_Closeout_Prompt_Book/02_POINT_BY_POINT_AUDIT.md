# Point-by-point audit — official submission vs PRAHARI now

**Re-audited.** 04 September 2026 after C00–C12 and I00–I12.  
**Code.** `02_Code/prahari/` · GitHub default branch `engine-pack` · https://github.com/amitduabits/PRAHARI  
**Sources.** Official text in this conversation (presentation, HLD, two demos, submit methods, scale bullets, eval 01–07 + bonus), live tree, HLD, Beamer slides/notes, deliverables, pytest.

**Status key**

| Status | Meaning |
|---|---|
| DONE | In the running platform or in the submitted-quality PDF/HLD, with tests or an artefact |
| PARTIAL | Exists but a required human artefact or a spoken honesty line is still missing |
| MISSING | Not in the packet the jury will see |
| N/A | Model 4 full-VMS item; answered as DESIGN TARGET text, not faked |

Remaining HUMAN rows: `REMAINING_TO_WIN.md` and `csv/closeout_actions.csv` C13–C14.

---

## 0. Verdict in one page

The platform **is** a working hybrid intelligence plane: registry, GIS (seeded), tokenised HLS, ANPR + operator confirm, CPU objects, godown intrusion, lawful enrolled-gallery FRS on Own cameras only, plate track `GJ01AB1234`, RBAC, integrator laws, GitHub, HLD, 54-frame slides, 15-page notes.

The packet **is not** a complete submission. Two Unlisted YouTube demonstrations, the Drive CSV, incognito checks, and the portal receipt are absent. Those four items eliminate you under eval 01, 04, and 07 regardless of code quality.

Tesseract is often not on PATH. Confirm on `cam04` is honest if you say so. Do not label it ANPR.

Do not upload the old 13-slide `PRAHARI_Solution.pptx` as the presentation. Upload `PRAHARI-Slides.pdf`.

---

## 1. Solution Presentation (PPT/PDF)

Official: model with justification; overview, objectives, innovations; architecture and E2E workflow; AI analytics (detection, recognition, events); watchlist correlation and real-time alerts; stack; scale/interop/security/deployment; operational benefits.

| # | Official sentence | Needed | Now | Pending |
|---|---|---|---|---|
| 1.1 | Model 1–5 / Hybrid / Customised with justification | Hybrid 1+2+thin 3; why not Model 4 statewide | DONE. HLD §2, slides “Chosen model”, README | Keep |
| 1.2 | Overview, objectives, key innovations | Census + viewing + event bus | DONE. Notes §1–§5, slides outcomes | Keep names on title frame |
| 1.3 | High-level architecture and E2E workflow | Diagram + ingest → analyse → match → alert → track | DONE. TikZ `pipeline.tex`, `arch.tex`, `engines.tex` | — |
| 1.4 | AI: detection, recognition, event analytics | Objects/persons/vehicles; plates + faces; alerts/intrusion | DONE in Beamer/notes/HLD §6. Code: blob objects, histogram FRS Own-only, ANPR/confirm, intrusion | Show Analyse still on **own-feed video**. Never FRS on Paldi |
| 1.5 | Watchlist correlation + automated alerts | Stolen/wanted/missing/blacklist; real-time | DONE. Plate + `face_id` + intrusion; WS + poll | Show Alerts tab on camera |
| 1.6 | Technologies, frameworks, tools | Open-source stack | DONE. Stack slide. Optional torch in `requirements-vision.txt`, not default | Do not list Kafka as running |
| 1.7 | Scale, interoperability, security, deployment | 80k DESIGN TARGET, adapters, RBAC, regional GPU | DONE. Slides 80k + MEASURED laptop + cost. Footer DESIGN TARGET | Speak it on video |
| 1.8 | Operational benefits / public safety | Command centre without ripping VMS | DONE. Notes + slides | One spoken line in own-feed |
| 1.9 | PPT/PDF files exist | Official format | DONE for PDF: `04_Documents/PRAHARI-Slides.pdf` (54 frames), `PRAHARI-Notes.pdf` (15 pages). PARTIAL for PPTX: 13-slide file is stale | HUMAN: attach Beamer PDF. Optional: ask Grok to refresh PPTX if the form rejects PDF |
| 1.10 | No lorem, no forbidden claims | Honesty lock | DONE. `audit_gate.py` PASS (K1, K3) | Keep confirm ≠ ANPR on camera |

---

## 2. Technical Proposal — High-Level Design

| # | Official sentence | Needed | Now | Pending |
|---|---|---|---|---|
| 2.1 | Overall architecture + diagrams + interactions | Hybrid diagram, adapters, bus, SOC | DONE. HLD §3 ASCII + TeX figures. PoC = SQLite + in-process WS | — |
| 2.2 | Heterogeneous cameras, NVRs, VMS | CSV, form, REST, catalogue, RTSP/HLS/WHEP/ONVIF | DONE for CSV/form/REST/catalogue/RTSP/HLS. WHEP documented link-out. ONVIF named as later adapter | Do not fake a device manager |
| 2.3 | Ingest, process, manage live streams from dispersed sites | TCP, PTS, backoff, HLS fallback, session cap | DONE. `capture.py`, `sampler.py`, `sessions.py`, integrator tests | Re-probe cam04 on recording day |
| 2.4 | Watchlist (stolen, wanted, missing, blacklist, suspects) + continuous correlation + real-time alerts | Multi-entity match on every detection | DONE. Vehicles STOLEN/BLACKLIST/OBSERVE. Person `WL-004` matches `face_id`. Representative only | No live VAHAN. Say so |
| 2.5 | AI: ANPR, FRS, object detection, person/vehicle tracking, other | Approach in HLD **and** in code | DONE. HLD §6 + 6.1–6.4. Code: Tesseract/confirm, blob objects, Own-only histogram FRS, IoU `track_id`, plate GIS track. Optional FaceNet/YOLO/ByteTrack | GPU count MEASURED 0. Plate track is the eval test, not ByteTrack |
| 2.6 | Alert workflow: priority, visualisation, interaction | CRITICAL/HIGH/LOW, queue, ack, WS | DONE. Person cards show name/gallery. `pending_review` shown | Show Ack on video |
| 2.7 | Scale/interop/security/performance to ~80,000 cameras | Regional 1 fps, HA, DR, RBAC | DONE as DESIGN TARGET HLD §5/§10/§12. MEASURED: 4 captures, 41 KB crop, GPU 0 | Speak DESIGN TARGET |
| 2.8 | Prerequisites from departments | Inventory, protocol, ONVIF, AMC, consent, watchlist sample | DONE. HLD §11 | — |
| 2.9 | Cybersecurity | RBAC, tokens, path jail, HMAC, no RTSP in browser | DONE in PoC tests. TLS/mTLS/VLAN DESIGN TARGET | — |
| 2.10 | Deployment / sizing / cost | Regional GPU, ~₹5–6 Cr intelligence plane | DONE. HLD §10/§12 | Not a vendor quote |
| 2.11 | Central/regional/edge, GPU, bandwidth, hot/warm/cold, LB, HA/DR, cost | Official “participants should explain” list | DONE in HLD §5, §10, §12, notes scale section, slides | Must be in the PDF the jury opens (it is) |

---

## 3. Demonstration on participant's own feed

Official: max 2–3 minutes, screen-recorded, fully functional backend. Onboard/process; AI (ANPR, FRS, **or** other); watchlist correlation; automatic alerts.

| # | Official sentence | Needed | Now | Pending |
|---|---|---|---|---|
| 3.1 | Own CCTV or footage of choice | File camera `CAM-OWN-001` | DONE. `03_Data/recordings/own_feed.mp4` | If no readable plate, confirm and say so |
| 3.2 | Onboarding and processing | File tile + ingest | PARTIAL. Product can. **No screen record** | HUMAN H5 |
| 3.3 | AI detection/analytics | At least one engine on the clip | PARTIAL. Analyse still + objects + optional Own FRS in product | Must appear in the video |
| 3.4 | Correlation with representative watchlist | Stolen/wanted/missing/blacklist | DONE in product (`GJ01AB1234`, `WL-004`) | Must appear in the video |
| 3.5 | Automatic real-time alerts | WS + Alerts tab | DONE in product | Must appear in the video |
| 3.6 | Fully functional, not a mock | SQLite row after POST | DONE | Video must show Alerts after a real POST |
| 3.7 | ≤ 3 min Unlisted YouTube | Artefact | **MISSING** | HUMAN H5 |
| 3.8 | Spoken honesty | Confirm vs OCR, DESIGN TARGET 80k, representative watchlist | Script ready | Read MUST lines |

---

## 4. Live demonstration on government-provided CCTV feed

Official: onboard gov feed(s); live or recorded viewing; analytics output; screen-recorded video **plus** output report of detected vehicles or plates with timestamps.

| # | Official sentence | Needed | Now | Pending |
|---|---|---|---|---|
| 4.1 | Onboard government feeds | Catalogue sync | DONE. 30 cameras from `/cameras.json` | Re-sync on record day |
| 4.2 | Onboarding and live/recorded viewing | HLS tile via tokenised proxy | PARTIAL. Product can. **No video**. Live catalogue has no coordinates | Open cam04 from the **table** |
| 4.3 | Analytics output on the provided feed | ANPR and/or objects on Paldi | PARTIAL. Two operator-confirm rows, confidence 1.0. Tesseract often absent. Objects available via Analyse | Confirm honesty. **No FRS** |
| 4.4 | Screen-recorded video Unlisted | ≤3 min | **MISSING** | HUMAN H6 |
| 4.5 | Output report: vehicles or plates + timestamps | CSV | PARTIAL. `gov_feed_plates.csv` + NOTE.txt | Upload Drive. Optional objects CSV |
| 4.6 | Drive/OneDrive Anyone+Viewer | Official method | **MISSING** | HUMAN H7 |
| 4.7 | Do not wget `/stream/<id>` | Integrator law | DONE in code/docs | Spoken forbid |

---

## 5. How to submit

| # | Official method | Status | Who |
|---|---|---|---|
| 5.1 | Unlisted YouTube | MISSING both | Lead H5 H6 |
| 5.2 | Drive/OneDrive Anyone+Viewer | MISSING | Lead H7 |
| 5.3 | Optional hosted URL + test login | SKIPPED (local `:8080`). Tunnel only after password rotate | Lead H10 optional |
| 5.4 | GitHub/GitLab | DONE. https://github.com/amitduabits/PRAHARI default `engine-pack` | Paste that URL |
| 5.5 | Portal before 07 Sep 12:00 IST | MISSING | Lead H9 |
| 5.6 | Incognito of every submitted link | BLOCKED on videos | Lead H8 |

---

## 6. Plan for scale (participants should explain)

All of these are **written** in HLD + slides + notes. The jury also needs to **hear** 80k as DESIGN TARGET on video.

| # | Official item | In docs | MEASURED vs DESIGN TARGET |
|---|---|---|---|
| 6.1 | Central, regional, edge | HLD §10: 2 API + 5 GPU regions + edge 1 fps | Laptop PoC. 4 captures MEASURED |
| 6.2 | GPU / accelerators | Regional L40S-class DESIGN TARGET. PoC CPU | GPU count MEASURED 0 |
| 6.3 | Bandwidth + low-bandwidth | HLD §5: 3.6 GB/s naive, 720 MB/s/region; HLS if 8554 blocked | Mean crop 41 KB MEASURED; 80 KB DESIGN TARGET |
| 6.4 | Hot / warm / cold | Phase-2 selected cameras. PoC = crops + metadata | Arithmetic in SCALE_BENCH |
| 6.5 | LB, scale-out, monitoring, health | Regional worker = scale unit. `/api/health`, gap report, session cap | Health p99 ~9 ms MEASURED. No K8s in PoC |
| 6.6 | HA, backup, DR, cyber | HLD: PoC HA = none. RBAC/audit/HMAC MEASURED | Do not claim active-active on a laptop |
| 6.7 | Implementation + ops cost | ~₹5–6 Cr / yr intelligence plane DESIGN TARGET | Not a VMS-replacement quote |

---

## 7. Evaluation framework A

| Area | Official bar | PRAHARI now | Risk | Close |
|---|---|---|---|---|
| 01 Successful test case | Gov feed onboard, viewing, analytics output | 30 cameras, HLS works, confirm CSV. **No video** | Eliminates | H6 H7 |
| 02 Solution presentation | Clarity of PPT/PDF | Beamer 54 frames + notes 15 pages. Old PPT stale | Medium if wrong file attached | Attach Beamer PDF |
| 03 Solution architecture | Sound HLD + diagrams | HLD matches APIs. FRS law explicit | Low | — |
| 04 Working platform | Own **and** gov demos | Platform mature. **Both videos missing** | Eliminates | H5 H6 |
| 05 Video analytics | ANPR, person/vehicle, intrusion, objects, timestamps, reports | Engines in code. Confirm CSV exists. Objects/FRS not on camera yet | Score, not instant DQ if ANPR/confirm + timestamps exist | Show Analyse + object CSV on own-feed |
| 06 Scalability / PoC ready | 80k story + on-site PoC | HLD math + runcard. Finale bag empty | Tie-break | Speak DESIGN TARGET. Pack bag after shortlist |
| 07 Completeness | Docs, videos, reports, links reachable | GitHub live. Videos, Drive, portal missing | Eliminates | H8 H9 |

---

## 8. Evaluation framework B — bonus (does not rescue a failed mandatory)

| Bonus | Official | In product | On camera yet |
|---|---|---|---|
| Hybrid with operational value | Visible | Yes | Own-feed map line |
| Cross-camera vehicle tracking | Multi-camera correlation | `GET /api/track/GJ01AB1234` six seeds + live append | Reconstruct + CSV |
| Additional analytics beyond ANPR | Demonstrated | Objects, intrusion, Own-only FRS | Analyse still + godown line. No Paldi FRS |
| Edge / bandwidth / low-connectivity | 1 fps, HLS | HLS fallback coded | HLS on gov video. Speak 1 fps |
| Cybersecurity, privacy, audit, RBAC | Enhanced | RBAC, audit, consent, HMAC, path jail, FRS refuse | Optional: mention no FRS on public CCTV |
| Dashboards, alerts, health, APIs | Operational | Map, WS alerts, gap report, REST | Footer health + Alerts |

---

## 9. Official test case (designated vehicle)

| # | Official | Status |
|---|---|---|
| 9.1 | Onboard ~50 heterogeneous cameras | 30 from live catalogue (MEASURED; count can change) |
| 9.2 | Centralised monitoring + AI analytics | Viewer + ANPR/confirm + objects + Own FRS + intrusion |
| 9.3 | Identify designated registration across grid | Seeded `GJ01AB1234` Valsad→GNR. Live confirm on cam04 appended |
| 9.4 | Complete route timestamped, location-wise | JSON + CSV. Live catalogue has no lat/lon so cam04 is not a map pin |
| 9.5 | Watchlist + continuous cross-reference + alerts | Plate and person paths in code |
| 9.6 | Evidence | Code + HLD. **Videos are what the jury watches** |

Finale designated plate may differ: confirm path accepts any Indian plate.

---

## 10. Integrator laws

Static tests DONE (`test_integrator_laws.py`, `test_scene_cut.py`). Live soak: re-open cam04 on record day.

| Law | Code | Tests |
|---|---|---|
| RTSP over TCP | env before `import cv2` | DONE |
| No CAP_PROP_FPS timing | PTS only | DONE |
| Gaps not disconnects | StreamSession continues | DONE |
| Backoff 2–30 s | constants | DONE |
| Decoder warnings non-fatal | logged | DONE |
| Catalogue `/cameras.json` | `catalogue.py` | DONE |
| Scene cut resets trackers | objects + faces reset | DONE |
| Consume only | no publish / no wget dataset | DONE |

---

## 11. Working platform inventory

### Present (do not rebuild)

FastAPI `:8080`, seven tabs, catalogue sync, tokenised HLS, ANPR `recognize()`, operator confirm, `analyse()`, objects, intrusion, Own-only faces, matcher plate/face/intrusion, track CSV, predict, keyword query, RBAC, experiment harness, 88 pytest, audit_gate PASS.

### Absent (HUMAN only)

- Unlisted own-feed YouTube
- Unlisted gov-feed YouTube
- Drive Anyone+Viewer
- Portal receipt
- Tesseract on PATH (optional if confirm is spoken)
- Two consented adult photos (optional if synthetic gallery is spoken)
- Finale bag

### Do not submit as the presentation

- Stale 13-slide `04_Documents/PRAHARI_Solution.pptx` (paths and FRS story outdated)
- Nested `PRAHARI/` copy
- Arnav workshop `ArAv-1/PRAHARI-3.0` as the submission repo

---

## 12. Documents vs code (drift closed)

| Claim | Reality |
|---|---|
| HLD §6 | Histogram FRS + blob objects + Tesseract/confirm + optional FaceNet/YOLO |
| Slides FRS | Law: Own gallery only; never Paldi |
| `gov_feed_plates.csv` | Operator confirm, confidence 1.0. NOTE.txt says so |
| Footer 80k | DESIGN TARGET. MEASURED four tiles |
| GitHub | `engine-pack` is default. `main` is older closeout |

---

## 13. Human blockers (the contest)

See `REMAINING_TO_WIN.md` H1–H11.

| Item | Who | Status |
|---|---|---|
| Tesseract on PATH | Aria / Lead | NOT_STARTED |
| Two consented adult photos | Lead + Arnav | NOT_STARTED |
| Own-feed Unlisted YT | Lead | NOT_STARTED |
| Gov-feed Unlisted YT | Lead | NOT_STARTED |
| Drive Anyone+Viewer | Lead | NOT_STARTED |
| Incognito | Lead | NOT_STARTED |
| Portal receipt | Lead | NOT_STARTED |
| Optional tunnel | Lead | SKIP unless asked |
| Finale bag | All | After shortlist |
