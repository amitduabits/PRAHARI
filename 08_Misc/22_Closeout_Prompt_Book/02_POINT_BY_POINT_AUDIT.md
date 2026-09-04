# Point-by-point audit — official submission vs PRAHARI now

**Audited.** 04 September 2026.  
**Sources.** `06_References/SENTINEL_Problems_Page.md` (verbatim official page), live code under `02_Code/prahari/`, HLD, slides, deliverables, pytest tree, `08_Misc/20_Prompts/csv/execution_status.csv`, `08_Misc/21_Audit_Remediation/csv/audit_actions.csv`.

**Status key**

| Status | Meaning |
|---|---|
| DONE | Implemented, evidenced, tests exist or artefact exists |
| PARTIAL | Code or doc exists but missing a required piece, a test, or a human artefact |
| MISSING | Not in the running platform |
| BLOCKED | Waiting on a human or an external host |
| N/A | Official item is a Model 4 full-VMS deliverable; hybrid PoC answers it as DESIGN TARGET text, not as a fake product |

Every pending item has closeout IDs (`Cxx-nnn`) in `csv/closeout_actions.csv`.

---

## 0. Verdict in one page

The platform is a **working hybrid intelligence plane for plates**: registry, GIS (seeded cameras), tokenised HLS viewer, ANPR interface, operator confirm, watchlist, WebSocket alerts, six-point track, RBAC, integrator laws, GitHub, HLD, slides.

It is **not yet a complete submission**. Two screen-recorded demonstrations, the Drive CSV link, incognito check, and portal receipt are absent. Official evaluation area 05 and the HLD bullet on AI analytics also name **FRS, object detection, person/vehicle detection, and intrusion**. Those engines are not in `app/services/`. Watchlist row `WL-004` is a person with no plate; the matcher ignores it.

If we submit as-is after only recording videos, we can pass the **mandatory ANPR test case** (with operator confirm, which must be labelled as such). We will score weakly on analytics quality and leave bonus “additional reliable analytics” on the table. This book exists to close both the submission blockers and the analytics gap without breaking honesty or the FRS law.

---

## 1. Solution Presentation (PPT/PDF)

Official: “Proposed solution model … with justification. Overview, objectives, key innovations. High-level architecture and end-to-end workflow. AI-powered video analytics (detection, recognition, event analytics). Watchlist correlation and automated real-time alerts. Stack. Scalability, interoperability, security, deployment. Operational benefits.”

| # | Official sentence | Needed | Done | Pending | Close |
|---|---|---|---|---|---|
| 1.1 | Model (1–5, Hybrid, or Customised) with justification | Hybrid 1+2+thin 3, why not Model 4 statewide | DONE. BRIEF, HLD §2, slides, README | Keep. Do not switch models. | — |
| 1.2 | Overview, objectives, key innovations | One-page story: census + viewing + event bus | DONE. Slides + notes + BRIEF | Confirm names + institute on slide 1 (W05-001 marked DONE) | C12-001 |
| 1.3 | High-level architecture and E2E workflow | Diagram + ingest → analyse → match → alert → track | PARTIAL. TikZ arch in `04_Documents/bits-tex/figures/arch.tex`. Pipeline is plate-only | Redraw worker box as ANPR + objects + lawful FRS after C02/C03 | C12-002 |
| 1.4 | AI analytics: detection, recognition, event analytics | Detection (objects/persons/vehicles), recognition (plates + faces), events (alerts/intrusion) | PARTIAL. Recognition = ANPR + confirm. No detection engine. No FRS | Implement C02–C04 then patch slides. Do not screenshot FRS on Paldi Circle | C02, C03, C12-003 |
| 1.5 | Watchlist correlation + automated alerts | Stolen/wanted/missing/blacklist; real-time | PARTIAL. Plate matcher + WS alerts. Person row never matches. Missing-person path absent | C05 matcher for face_id / entity_id | C05-001 |
| 1.6 | Technologies, frameworks, tools | Open source stack named | DONE. FastAPI, SQLite, Leaflet, OpenCV, Tesseract, FFmpeg | Add OpenCV DNN / LBPH after they exist. Do not list Kafka as running | C12-004 |
| 1.7 | Scale, interoperability, security, deployment | 80k, adapters, RBAC, regional GPU | PARTIAL. HLD §5/§9/§10. PPT cost slide matches ~₹5–6 Cr DESIGN TARGET | Spoken 80k line already in footer. Keep DESIGN TARGET label | C12-005 |
| 1.8 | Operational benefits / public safety | Command-centre value without ripping VMS | DONE in notes/slides | One sentence on godown intrusion after C04 | C12-006 |
| 1.9 | PPT/PDF files exist and export | Official format | DONE. `04_Documents/PRAHARI_Solution.pptx`, `05_Output/deliverables/PRAHARI_Solution.pdf`, Beamer `PRAHARI-Slides.pdf` | Punch list: working-tree paths on old PPT slide 13 | C12-007 |
| 1.10 | No lorem, no forbidden claims | Honesty lock | DONE for A08 greps | After FRS lands, replace “face recognition / not in this PoC” with the FRS law sentence, not a NAFIS claim | C12-008 |

---

## 2. Technical Proposal — High-Level Design

| # | Official sentence | Needed | Done | Pending | Close |
|---|---|---|---|---|---|
| 2.1 | Overall architecture + diagrams + component interactions | Hybrid diagram, adapters, bus, SOC | DONE. HLD §3. PoC = SQLite + in-process WS, contract = future Kafka | After analytics, name `analyse()` as the worker | C12-009 |
| 2.2 | Heterogeneous cameras, NVRs, VMS into one platform | CSV, form, REST, catalogue, RTSP/HLS/WHEP/ONVIF | PARTIAL. CSV, form, REST, catalogue, RTSP, HLS. WHEP is a documented link-out. ONVIF not implemented | Document ONVIF as adapter stub (one connector), do not fake a device manager | C12-010 |
| 2.3 | Ingest, process, manage live streams from dispersed sites | TCP capture, PTS, backoff, HLS fallback, session cap | DONE. `capture.py`, `sampler.py`, `sessions.py`, integrator tests | Live soak experiment C09 still required | C09-001 |
| 2.4 | Watchlist integration (stolen vehicles, wanted persons, missing persons, blacklisted vehicles, suspects) + continuous correlation + real-time alerts | Multi-entity watchlist, match on every detection | PARTIAL. Vehicles: STOLEN, BLACKLIST, OBSERVE. Person row `WL-004` Ramesh K has empty plate so matcher skips it. No missing-person gallery | C05 + C03. Representative data only. No live VAHAN | C05-002 |
| 2.5 | AI: ANPR, FRS, object detection, person and vehicle tracking, other analytics | Working approach in HLD **and** in code | PARTIAL. HLD §6: Phase-1 ANPR, Phase-1.5 count/intrusion if GPU, Phase-2 FRS. Code: ANPR + confirm only. YOLO class raises RuntimeError. Vehicle “tracking” is plate sightings, not a multi-object tracker | Implement CPU engines. Rewrite HLD §6 to match. Person/vehicle **track ids** on own-feed; plate track remains the evaluation test | C02, C03, C04, C12-011 |
| 2.6 | Alert workflow: prioritisation, visualisation, user interaction | CRITICAL/HIGH/LOW, UI queue, ack, WS | DONE for plates | Person/intrusion cards must not render a blank plate | C07-001 |
| 2.7 | Scale, interoperability, security, performance to ~80,000 cameras | Regional 1 fps math, HA, DR, RBAC | PARTIAL. HLD §5/§10 DESIGN TARGET. No MEASURED load test beyond 4 tiles | C10 bench. Label every number | C10-001 |
| 2.8 | Prerequisites, assumptions, info from departments | Inventory, protocol, ONVIF, AMC, consent, watchlist sample | DONE. HLD §11 | Unchanged | — |

HLD extra (not in the eight bullets but required by Step 6 scale and Step 3 cover list):

| # | Topic | Status | Close |
|---|---|---|---|
| 2.9 | Cybersecurity architecture | PARTIAL. RBAC, tokens, path jail, HMAC, no RTSP in browser. TLS/mTLS/VLAN are DESIGN TARGET text | C11 |
| 2.10 | Deployment architecture | PARTIAL. Laptop PoC. Regional GPU described | C10, C12 |
| 2.11 | Infrastructure sizing | DESIGN TARGET in §5/§12 | C10 |
| 2.12 | Cost-benefit | DONE. ~₹5–6 Cr intelligence plane, not VMS replacement | — |
| 2.13 | Future roadmap | PARTIAL. Model 4 selected cameras, FRS Phase-2 | Move FRS lawful-gallery into Phase-1.5 implemented; keep AFIS/NAFIS Phase-2 | C12-011 |

---

## 3. Demonstration on participant's own feed

Official: max 2–3 minutes, screen-recorded, fully functional backend (no mock-ups). Must show onboard/process, AI detection/analytics (ANPR, FRS, **or** other), watchlist correlation, automatic real-time alerts.

| # | Official sentence | Needed | Done | Pending | Close |
|---|---|---|---|---|---|
| 3.1 | Own CCTV or footage of our choice | File camera `CAM-OWN-001` | DONE. `03_Data/recordings/own_feed.mp4` exists (W02-001 DONE) | If clip has no readable plate, use confirm **and** say so. Prefer a still that Tesseract can read | C06-003, C13-001 |
| 3.2 | Onboarding and processing live or recorded feeds | File protocol tile + ingest | PARTIAL. Tile path implemented. Screen record missing | Record it | C13-002 |
| 3.3 | AI detection and analytics (ANPR, FRS, or other) | At least one working engine on the clip | PARTIAL. ANPR interface + confirm. Tesseract often absent. No FRS, no objects | C06 Tesseract. C02 objects on the clip. C03 FRS on enrolled stills in the same video if time | C06, C02, C03, C13-003 |
| 3.4 | Correlation with representative watchlist | Stolen/wanted/missing/blacklist | PARTIAL. `GJ01AB1234` STOLEN works. Person watchlist does not | C05 | C05, C13-004 |
| 3.5 | Automatic real-time alerts and visualisation | WS + Alerts tab, no refresh | DONE in product | Must appear in the video | C13-005 |
| 3.6 | Fully functional, not a mock | Detection **row in SQLite** | DONE for confirm path | Video must show the Alerts card after a real POST | C13-006 |
| 3.7 | ≤ 3 minutes, Unlisted YouTube | Artefact | MISSING. `own_feed_demo.mp4` and YouTube URL pending | HUMAN | C13-007 |
| 3.8 | Spoken honesty | Confirm vs OCR, DESIGN TARGET 80k, representative watchlist | Script exists (`own_feed_demo_script.md`) | Update script after C07 so objects/FRS appear without claiming NAFIS | C12-012 |

---

## 4. Live demonstration on government-provided CCTV feed

Official: onboard government feed(s); live or recorded viewing; analytics output; screen-recorded video **plus** output report of detected vehicles or number plates with timestamps.

| # | Official sentence | Needed | Done | Pending | Close |
|---|---|---|---|---|---|
| 4.1 | Onboard government-provided feeds | Catalogue sync of sandbox cameras | DONE. 30 cameras from `/cameras.json`. `onboard_failures.md` exists. cam01 and cam04 RTSP-TCP live (pack notes) | Re-probe on recording day; ids change | C09-002 |
| 4.2 | Successful onboarding and live or recorded viewing | HLS tile via tokenised proxy | PARTIAL. Product can. Video missing. GIS pins cannot be used: live catalogue has no coordinates | Open `cam04` from Cameras table, not the map | C13-008 |
| 4.3 | Available video-analytics output on the provided feed | ANPR and/or objects on Paldi Circle (cam04) | PARTIAL. Two **operator confirm** rows, confidence 1.0. Tesseract was not on PATH. No object detections | Install Tesseract. Run analyse on a grabbed frame. If OCR fails, confirm **and** still run object detector on the same frame | C06-004, C09-003 |
| 4.4 | Screen-recorded video | ≤3 min, Unlisted YouTube | MISSING | HUMAN. FRS **off** on this feed | C13-009 |
| 4.5 | Output report: detected vehicles or plates + timestamps | CSV | PARTIAL. `gov_feed_plates.csv` has 2 confirm rows on cam04 | After C06/C09, regenerate. If still confirm, keep the NOTE.txt honesty line. Add `gov_feed_objects.csv` if objects fire | C09-004, C13-010 |
| 4.6 | Drive/OneDrive Anyone+Viewer | Official submit method | MISSING | HUMAN | C13-011 |
| 4.7 | Do not wget `/stream/<id>` | Integrator law | DONE in code/docs | Spoken script already forbids it | — |

---

## 5. How to submit

| # | Official method | Status | Close |
|---|---|---|---|
| 5.1 | Unlisted YouTube | MISSING both videos | C13-007, C13-009 |
| 5.2 | Drive/OneDrive Anyone+Viewer | MISSING | C13-011 |
| 5.3 | Optional hosted URL + test login | SKIPPED for public tunnel (A13). Local `:8080` only. A02–A05 are PASS so a tunnel is allowed **after** password rotate | C14-001 optional |
| 5.4 | Optional GitHub/GitLab | DONE. https://github.com/amitduabits/PRAHARI | C14-002 push after analytics |
| 5.5 | Portal form before 07 Sep 12:00 IST | MISSING | C14-003 |
| 5.6 | Incognito of every submitted link | BLOCKED on videos | C14-004 |

---

## 6. Plan for scale (participants should explain)

| # | Official item | Needed | Done | Pending | Close |
|---|---|---|---|---|---|
| 6.1 | Central, regional, and edge-compute | 2 central API + 5 regional GPU + edge 1 fps | DONE as DESIGN TARGET in HLD §10 | C10 MEASURED: this laptop, 4 captures, 1 fps sampler | C10-002 |
| 6.2 | GPU or accelerator for video analytics | L40S-class regional; PoC is CPU | PARTIAL. HLD names 8×L40S. PoC YOLO raises RuntimeError | C02 CPU DNN. HLD: GPU is statewide, CPU is PoC. Never claim a GPU we do not have | C10-003, C12-013 |
| 6.3 | Network bandwidth and low-bandwidth strategies | 3.6 GB/s naive vs 720 MB/s per region; crops not 25 fps; HLS if 8554 blocked | DONE as DESIGN TARGET in HLD §5 | C10 MEASURED bytes of one 1 fps crop stream | C10-004 |
| 6.4 | Hot / warm / cold storage vs retention | 7 / 8–30 / 31–90 days, Phase-2 selected cameras | DONE as DESIGN TARGET. PoC stores crops + metadata | Experiment: crop file size × 45k × 7 days labelled DESIGN TARGET | C10-005 |
| 6.5 | Load balancing, horizontal scaling, monitoring, logging, health checks | Regional worker = scale unit; Prometheus statewide | PARTIAL. `/api/health`, gap report, MAX_OPEN_CAPTURES. No Prometheus in PoC | C10 health-check soak. Do not install K8s | C10-006 |
| 6.6 | HA, backup, DR, cybersecurity | active-active, RPO 15 min, RTO 1 h, RBAC, audit | PARTIAL. Security controls MEASURED in tests. HA/DR DESIGN TARGET | C11 tests stay green. HLD already states PoC HA = none | C11 |
| 6.7 | Estimated implementation and operational costs | ~₹5–6 Cr / yr intelligence plane | DONE. HLD §12 | Do not present as a quote | — |

---

## 7. Evaluation framework A — common areas

| Area | Official bar | PRAHARI now | Risk | Close |
|---|---|---|---|---|
| 01 Successful test case | Onboard gov feed, live/recorded viewing, required analytics output | 30 cameras onboarded. HLS viewing works. Analytics output is confirm-not-OCR. Videos missing | Eliminates if video or viewing fails | C09, C13 |
| 02 Solution presentation | Clarity and completeness of PPT/PDF | Beamer + PPT + PDF exist. Hybrid justified. AI slide is ANPR-only | Medium: incomplete AI story | C12 |
| 03 Solution architecture | Sound, feasible, secure, interoperable HLD + diagrams | HLD matches live APIs. FRS/object described as later | Medium until §6 rewritten to match new engines | C12 |
| 04 Working platform and demonstration | Maturity on own feed **and** gov feed | Platform mature for plates. Both videos missing | Eliminates | C13 |
| 05 Video analytics output | ANPR, vehicle or person detection, intrusion, object detection, timestamps, reports | ANPR weak (Tesseract often absent). No person/vehicle/object/intrusion engines. Timestamps exist on confirm CSV | High for scoring; not an instant DQ if ANPR/confirm + timestamps exist | C02–C07, C09 |
| 06 Scalability and PoC readiness | 80k story + on-site PoC preparedness | HLD math + finale runcard. No MEASURED bench. Finale bag not packed | Tie-break | C10, C14-005 |
| 07 Submission completeness | Docs, videos, reports, links, credentials consistent and reachable | GitHub live. Videos, Drive, portal, incognito missing | Eliminates if a link 403s | C14 |

---

## 8. Evaluation framework B — bonus (does not rescue a failed mandatory)

| Bonus | Official | PRAHARI now | After this book |
|---|---|---|---|
| Hybrid architecture with operational value | Must be visible | Built and in PPT | Keep. Show in both videos |
| Advanced cross-camera vehicle tracking | Multi-camera correlation | `GET /api/track/GJ01AB1234` six seeds + live append + teleport flag | Keep. Show Reconstruct + CSV |
| Additional reliable analytics beyond ANPR | Must be **demonstrated**, not described | MISSING | C02 objects, C03 FRS (own-feed only), C04 intrusion |
| Edge / bandwidth / low-connectivity | 1 fps, HLS fallback | Designed. HLS fallback coded | Show HLS on gov video. Speak 1 fps |
| Cybersecurity, privacy, audit, RBAC | Enhanced | RBAC, audit, consent, tokenised HLS, path jail, HMAC | C11. FRS privacy is a bonus if we refuse gov-camera faces |
| Dashboards, automated alerts, health, APIs | Operational | Map, alerts WS, gap report, REST | Show footer health + WS toast |

---

## 9. Technical evaluation / test case (Step 4)

| # | Official | Status | Close |
|---|---|---|---|
| 9.1 | Onboard ~50 heterogeneous cameras | 30 from live catalogue (count is MEASURED, catalogue can change) | Re-sync on demo day |
| 9.2 | Centralised monitoring + AI analytics | Viewer + ANPR/confirm. AI incomplete | C02–C06 |
| 9.3 | Designated vehicle registration number, identify, trace, present movement | Seeded GJ01AB1234 Valsad→GNR. Live confirm on cam04 appended | At finale, designated plate may differ: confirm path must accept any Indian plate |
| 9.4 | Complete route: timestamped, location-wise | JSON + CSV. Live catalogue cameras have no lat/lon so cam04 will not sit on the Gujarat map | Honesty in script. Seeded path is the GIS story |
| 9.5 | Working watchlist + continuous cross-reference + automated alerts | Plate path yes. Person path no | C05 |
| 9.6 | Evidence of integration, analytics, interoperability, scalability, E2E | Code + HLD. Videos are the evidence the jury actually watches | C13 |

---

## 10. Integrator pre-submission checklist (official §4)

Encoded in `tests/test_integrator_laws.py`. Status: **DONE as static tests**. Pending: **live soak**.

| Law | Code | Test | Live experiment |
|---|---|---|---|
| RTSP over TCP | `capture.py` sets env before `import cv2` | DONE | C09 grab cam04 |
| No CAP_PROP_FPS / arrival-time | services grepped | DONE | C09 log pts_ms |
| Inter-frame gaps not fatal | StreamSession continues | PARTIAL unit | C09 |
| Backoff 2..30 | constants | DONE | C09 optional restart |
| Decoder warnings non-fatal | logged | PARTIAL | C09 |
| Catalogue `/cameras.json` | `catalogue.py` | DONE `test_catalogue.py` | C09 sync |
| Mixed codec/resolution | per-camera fields | PARTIAL | C09 two cameras |
| Scene discontinuity resets tracker | `test_scene_cut.py` | DONE for callback | C02/C03 must hook the same callback for object/face track ids |

---

## 11. Working platform inventory (code)

### Present (do not rebuild)

- FastAPI `:8080`, SQLite seed, seven UI tabs
- Camera CRUD, CSV import/export, catalogue sync, gap report
- Tokenised HLS/file proxy, 2×2 wall, max 4 sessions
- ANPR `recognize()`, Indian normaliser, still upload, operator confirm
- Plate matcher, 120 s dedupe, WS alerts, ack audit
- Track API + CSV for GJ01AB1234
- RBAC: superadmin, soc_operator, dept_viewer, auditor
- Tests: health, cameras, catalogue, integrator laws, matcher, no RTSP leak, path jail, plate normaliser, scene cut, security, tabs smoke, track, ANPR synthetic (skip without Tesseract)

### Absent (this book)

- `app/services/objects.py`
- `app/services/faces.py`
- `app/services/intrusion.py`
- `app/services/analyse.py`
- Person matcher for `WL-004`
- Object/face CSV reports
- Experiment harness and MEASURED logs
- UI for objects/faces/intrusion
- Tesseract on PATH (HUMAN)
- Demo videos and Drive link (HUMAN)
- Docker Compose (P00-007 P1, skip unless time)

### Present but inert

- `YoloEngine.recognize` raises `RuntimeError`
- Watchlist `WL-004` person with empty plate
- HLD sentence “Phase-2: FRS” which this book upgrades to a lawful gallery in the PoC

---

## 12. Documents vs code drift

| Claim | Reality | Action |
|---|---|---|
| HLD §6 Phase-1 is ANPR only | True today | Rewrite after C02–C04 |
| Slides: “Face recognition is not the demo” | Policy, not a capability | Replace with FRS law: enrolled gallery on own-feed; never on gov CCTV |
| PPT punch list: do not add FRS screenshots | Still correct for **gov** video | Own-feed may show enrolled-gallery match |
| `gov_feed_plates.csv` looks like ANPR | It is operator confirm | Keep NOTE.txt. Do not retitle as OCR |
| Footer 80k DESIGN TARGET | Correct | Keep |
| Nested `PRAHARI/PRAHARI/` tree | Duplicate copy | Do not edit it. Do not submit it as the repo root |

---

## 13. Human / external blockers

| Item | Who | Status |
|---|---|---|
| Tesseract on PATH | Aria / Lead | NOT_STARTED (W02-002) |
| Consented adult face photos (2) | Lead + Arnav | NOT_STARTED |
| Own-feed screen record + Unlisted YT | Lead | NOT_STARTED |
| Gov-feed screen record + Unlisted YT | Lead | NOT_STARTED |
| Drive Anyone+Viewer | Lead | NOT_STARTED |
| JUDGE_PASSWORD rotate if hosting | Lead | A01 marked DONE; re-check before tunnel |
| Portal receipt | Lead | NOT_STARTED |
| Finale bag | All | NOT_STARTED |

---

## 14. What “best researcher, thorough testing” means here

Every engine gets:

1. **Synthetic fixture unit tests** that do not need the sandbox or a GPU.
2. **API integration tests** that insert a real SQLite row.
3. **Negative tests** (unknown plate, unknown face, gov-camera FRS refuse, private camera without consent, fifth session rejected).
4. **A MEASURED experiment log** with command, input hash, output, timestamp.
5. **An honesty label** if the path was operator-confirm rather than a model.

If a test needs weights that are not in the tree, it skips with an explicit reason **and** a fallback fixture test still passes.

Deadline discipline: videos and links outrank a third object class. A green object+face suite with no YouTube is a losing submission. A YouTube of a running backend with only ANPR/confirm is a complete mandatory packet and a weaker eval-05 score. This book aims for both.
