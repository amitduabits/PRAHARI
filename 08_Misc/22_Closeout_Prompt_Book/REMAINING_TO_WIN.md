# Remaining to compete — HUMAN runbook

**Audited.** 04 September 2026 against the official submission text (presentation, HLD, two demos, how-to-submit, scale bullets, eval 01–07 + bonus).  
**Lock.** 07 September 2026 **12:00 IST**.  
**Code tree.** `02_Code/prahari/` on GitHub branch **`engine-pack`** (repo default).  
**This file is for Lead / Arnav / Aria.** Grok Build cannot record YouTube, cannot click Google Drive, cannot fill the portal, cannot sit in front of a camera.

C00–C12 and I00–I12 are **done in code and PDFs**. Do not ask the agent to rebuild engines. Do these HUMAN rows. A green pytest with no videos is a losing packet.

---

## 0. Verdict

| Layer | Status |
|---|---|
| Working platform | DONE. Hybrid 1+2+thin 3. ANPR + confirm, objects, godown intrusion, lawful FRS on Own cameras, plate track `GJ01AB1234`, RBAC, Sentinel `/cameras.json` |
| Solution presentation PDF | DONE. Beamer `04_Documents/PRAHARI-Slides.pdf` (54 frames) + notes 15 pages |
| HLD | DONE. `04_Documents/PRAHARI_HLD.md` covers architecture, ingest, watchlist, ANPR/FRS/objects, alerts, 80k DESIGN TARGET, cost, prerequisites |
| GitHub | DONE. https://github.com/amitduabits/PRAHARI default branch `engine-pack` |
| Own-feed YouTube ≤ 3 min | **MISSING. Submission blocker.** |
| Gov-feed YouTube ≤ 3 min | **MISSING. Submission blocker.** |
| Drive CSV Anyone+Viewer | **MISSING. Submission blocker.** |
| Portal receipt before noon | **MISSING. Submission blocker.** |
| Incognito of every submitted URL | **MISSING.** |
| Tesseract on PATH | **MISSING.** Demo still works via operator confirm if you say so. |
| Consented adult face photos | **MISSING.** Own-feed FRS uses synthetic gallery unless you add two adult photos. |
| Stale 13-slide PPT | Do **not** upload `PRAHARI_Solution.pptx` as the presentation. Upload the Beamer PDF. Ask Grok later if the form refuses PDF. |

If you record nothing else this week: two Unlisted videos + Drive CSV + portal. That is the contest.

---

## 1. What Grok Build already finished (do not redo)

- Hybrid model, Sentinel catalogue, RTSP-TCP, PTS, HLS tiles, path jail, HMAC, vendored `hls.min.js`
- `analyse()`: ANPR, objects, intrusion, Own-only faces; `frs_refused` on Gov / `cam04`
- Matcher: plate, `face_id` / `WL-004`, intrusion; 120 s dedupe; `pending_review` for reconstructed faces
- Optional FaceNet / YOLO / ByteTrack behind env; default needs no GPU
- pytest **88 passed, 4 skipped**; `audit_gate.py` **PASS**
- HLD §5–§15, Beamer slides, notes, GitHub Pages PDFs under `docs/`

---

## 2. Evaluation risk if you submit today

| Area | If you stop now | If you finish this runbook |
|---|---|---|
| 01 Test case | Fail. No gov video, no viewing proof | Pass: cam04 HLS + confirm CSV |
| 02 Presentation | Pass if you attach Beamer PDF + notes, **fail if you attach the old 13-slide PPT** | Pass |
| 03 Architecture | Pass (HLD + diagrams) | Pass |
| 04 Working platform | Fail. Jury never sees the backend | Pass |
| 05 Analytics | Weak. Confirm CSV exists; objects/FRS not on camera | Stronger: Analyse still + object CSV + Own-only face; gov still no FRS |
| 06 Scale 80k | Pass as DESIGN TARGET in HLD/slides | Speak the footer line in both videos |
| 07 Completeness | Fail. Blank YouTube, Drive, portal | Pass after incognito |
| Bonus | Hybrid + track + RBAC in code, not on camera | Show Reconstruct, Alerts, Analyse, no Paldi FRS |

Bonus does not rescue a missing video.

---

## 3. HUMAN actions — do in this order

Tick the CSV column in `csv/closeout_actions.csv`. Times are wall-clock for one person.

### Day 0 (today): machine ready

**H1. Install Tesseract (20 min). Owner: Aria or Lead. C06-001**

1. Install UB Mannheim Tesseract **or** `choco install tesseract`.
2. Open a **new** PowerShell. Run `tesseract --version`. You need a version line, not “not recognized”.
3. If it fails, the demo still uses **Operator confirm**. Do not delay YouTube for OCR.

**H2. Two consented adult photos (15 min). Owner: Lead + Arnav. C03-005**

1. Only adults who agreed in writing. Never a minor. Never a Paldi crop.
2. Save two JPEGs as `03_Data/samples/faces/WL-004/a.jpg` and `b.jpg` (create folders).
3. Optional: Watchlist tab → Enroll Missing/Wanted Person → `WL-004` → those files.
4. If you skip this, own-feed still shows **synthetic** gallery match or **Confirm face**. Say “representative person watchlist, not NAFIS”.

**H3. Passwords (5 min). Owner: Lead**

1. Open `02_Code/prahari/.env`. Confirm `JUDGE_PASSWORD` is not a public default if you will host.
2. Do **not** commit `.env`. Do **not** show it on camera.

### Day 1: record (the contest)

**H4. Boot and preflight (10 min). Owner: Lead. C13-001**

```
cd D:\1_Projects\Research_Ongoing\PRAHARI\02_Code\prahari
.\run.ps1
```

Second window:

```
.\scripts\preflight_demo.ps1
```

Need `PASS`. Browser: http://127.0.0.1:8080 login `judge` / `JUDGE_PASSWORD`. Window ≥ 1280 px. Close Slack, mail, `.env`, RTSP URLs.

**H5. Own-feed video ≤ 3:00 Unlisted YouTube (40 min). Owner: Lead. C13-002**

Follow `05_Output/deliverables/own_feed_demo_script.md` **exactly**.

Must show, in order:

1. Operations map (hybrid one-liner).
2. Vehicle Track `GJ01AB1234` → Reconstruct → CSV download starts.
3. Alerts CRITICAL for stolen.
4. Onboard: **Analyse this still** on `CAM-OWN-001` (objects; optional face if Own). If OCR empty: **Confirm plate** and say it is operator confirm, not ANPR.
5. Footer: 80,000 is a **DESIGN TARGET**. MEASURED cap is four tiles.

Save `05_Output/deliverables/own_feed_demo.mp4`. YouTube → Unlisted. Paste URL into `05_Output/deliverables/SUBMISSION_LINKS.md`.

Do not show FaceNet unless torch is installed. Histogram / confirm-face is enough.

**H6. Gov-feed video ≤ 3:00 Unlisted YouTube (40 min). Owner: Lead. C13-003**

Follow `gov_feed_demo_script.md`.

Must show:

1. Cameras **table**, not the map. Open **cam04** (Paldi Circle).
2. HLS tile playing.
3. Confirm `GJ01AB1234` on cam04 **or** a real ANPR row. If confirm: say “confidence 1.0, source operator confirm, not ANPR”.
4. Analyse this still on cam04 for **objects only**.
5. **MUST: we do not run FRS on this feed.**
6. Track Reconstruct: live point appended, six seeds remain.
7. Download `track` or plates CSV.

Save `gov_feed_demo.mp4`. YouTube Unlisted. Paste URL.

Never wget `/stream/cam04`. Never paste `rtsp://` on screen.

**H7. Drive CSV (15 min). Owner: Lead. C13-004**

1. File: `05_Output/deliverables/gov_feed_plates.csv` (two confirm rows today). Keep `gov_feed_plates.NOTE.txt` (“OCR empty, confirm used”).
2. Also upload `track_GJ01AB1234.csv` if Drive allows two files.
3. Google Drive or OneDrive: **Anyone with the link — Viewer**.
4. Open that link in **Incognito** before you paste it.
5. Paste URL into `SUBMISSION_LINKS.md`.

### Day 2: links and portal

**H8. Incognito every URL (20 min). Owner: Lead. C14-004**

Logged-out Chrome:

- Own-feed YouTube plays
- Gov-feed YouTube plays
- Drive CSV downloads
- https://github.com/amitduabits/PRAHARI README clone-and-run
- https://github.com/amitduabits/PRAHARI/blob/engine-pack/04_Documents/PRAHARI-Slides.pdf
- https://github.com/amitduabits/PRAHARI/blob/engine-pack/04_Documents/PRAHARI_HLD.md
- https://amitduabits.github.io/PRAHARI/ if Pages is live

If any 404/403, fix before the portal.

**H9. Portal (30 min). Owner: Lead. Morning of 07 Sep at latest. C14-003**

Form: https://docs.google.com/forms/d/e/1FAIpQLSeK7bCJ67zyZCF-73iAfRbMUXHtGbYKS5Cz8IgP-ZzQYZLJpw/viewform  
Login first: https://sentinel.gujarat.gov.in/login

Paste:

| Field | Value |
|---|---|
| Category | Academic / student |
| Solution PPT/PDF | `04_Documents/PRAHARI-Slides.pdf` (not the old 13-slide PPTX) |
| HLD | `04_Documents/PRAHARI_HLD.md` or export to PDF if the form wants a file |
| Notes (if extra slot) | `04_Documents/PRAHARI-Notes.pdf` |
| Own-feed | Unlisted YouTube from H5 |
| Gov-feed | Unlisted YouTube from H6 |
| Output report | Drive Anyone+Viewer from H7 |
| GitHub | https://github.com/amitduabits/PRAHARI (branch `engine-pack`) |
| Hosted URL | leave blank unless you opened a tunnel after password rotate |
| Login | only if hosted: `judge` / the rotated password |

Screenshot receipt → `07_Communications/submission_receipt.png`. Stop product edits.

**H10. Optional hosted URL (40 min). Owner: Lead. C14-001. Skip unless asked**

Only after `audit_gate.py` PASS and rotated `JUDGE_PASSWORD` / `SECRET_KEY`. No public RTSP. Email the committee if you change the password after sending it.

**H11. Finale bag (after shortlisting). C14-005**

Two laptops, chargers, HDMI, `data/prahari.db`, `own_feed.mp4`, hotspot, printed architecture, `FINALE_RUNCARD.md`, judge password on paper. Do not delete the db.

---

## 4. Spoken MUST lines (read on camera)

Own-feed:

1. PRAHARI is a hybrid intelligence plane. Departments keep their VMS.
2. Representative watchlist, not a live ministry pipe.
3. If you confirm: operator confirm writes a real row, confidence 1.0, not ANPR.
4. Enrolled gallery on Own cameras only. Never Paldi Circle.
5. At 80,000 cameras that number is a DESIGN TARGET. We sample 1 fps at the region. MEASURED cap on this box is four open tiles.

Gov-feed:

1. Catalogue is `/cameras.json`. Thirty cameras. No coordinates in that JSON.
2. We open Paldi Circle from the table, not from a map pin.
3. We do not run FRS on this feed.
4. Live confirm appended. The six seed points are still there.

---

## 5. What Grok Build can still do if you ask (not blockers)

- Refresh `PRAHARI_Solution.pptx` to match the 54-frame Beamer deck (only if the portal rejects PDF).
- Merge `engine-pack` into `main`.
- Tick `DEMO_ACCEPTANCE.md` after the two mp4 files exist.
- Install-side YOLO weights script (optional; do not delay video).

Do not ask Grok to “make the demo look nicer” after the receipt.

---

## 6. Do not

- Upload the stale 13-slide PPT as the official presentation.
- Show FRS on cam04 / Paldi / any `ownership=Gov`.
- wget `/stream/<id>` and call it the government feed.
- Label confirm rows as ANPR.
- Say live VAHAN / live eGujCop / NAFIS join.
- Quote 80,000 as laptop throughput.
- Commit `.env`.
- Miss 12:00 IST.
