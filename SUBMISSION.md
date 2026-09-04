# PRAHARI — submission packet (GPIC 2026)

**Category.** Academic / student (Lead, Arnav, Aria · BITS Pilani)  
**Model.** Hybrid: official Reference Models **1 + 2 + thin 3**. Model 4 (central VMS) is Phase-2, selected cameras only.  
**This GitHub branch.** `gpic-2026-submission`  
**Clone.** https://github.com/amitduabits/PRAHARI/tree/gpic-2026-submission  
**Lock.** 07 September 2026 12:00 IST  
**Form.** https://docs.google.com/forms/d/e/1FAIpQLSeK7bCJ67zyZCF-73iAfRbMUXHtGbYKS5Cz8IgP-ZzQYZLJpw/viewform  

YouTube Unlisted links and the Drive CSV URL are **HUMAN**. Paste them into the table below, then into the portal. Do not wait on more code.

---

## A. Attach these files on the portal

| Official item | File to attach or URL | Status |
|---|---|---|
| 1. Solution presentation (PPT/PDF) | `04_Documents/PRAHARI-Slides.pdf` (54-frame Beamer). Same bytes also at `05_Output/deliverables/PRAHARI_Solution.pdf` | READY |
| Teaching note (extra) | `04_Documents/PRAHARI-Notes.pdf` | READY |
| 2. Technical proposal / HLD | `04_Documents/PRAHARI_HLD.md` | READY |
| 3. Own-feed demonstration | Unlisted YouTube — **you upload** | PENDING |
| 4. Government-feed demonstration | Unlisted YouTube — **you upload** | PENDING |
| Output report (plates + timestamps) | `05_Output/deliverables/gov_feed_plates.csv` + `track_GJ01AB1234.csv`. Upload to Drive **Anyone with the link — Viewer** | FILE READY; Drive URL PENDING |
| Honesty note for gov CSV | `05_Output/deliverables/gov_feed_plates.NOTE.txt` (operator confirm, not ANPR) | READY |
| GitHub | this branch | READY |
| Hosted URL | leave blank unless a tunnel exists after password rotate | SKIP unless asked |
| Onboard log | `05_Output/deliverables/onboard_failures.md` (30 catalogue cameras; cam01/cam04 RTSP-TCP live) | READY |

**Do not attach** `04_Documents/PRAHARI_Solution.pptx` (stale 13-slide file). The Beamer PDF is the presentation.

---

## B. Paste these URLs after you upload video / Drive

| Field | Paste here then on the form |
|---|---|
| Own-feed YouTube (Unlisted) | _HUMAN_ |
| Gov-feed YouTube (Unlisted) | _HUMAN_ |
| Drive/OneDrive (Anyone + Viewer) | _HUMAN_ |
| GitHub | https://github.com/amitduabits/PRAHARI/tree/gpic-2026-submission |
| Team site (slides/notes) | https://amitduabits.github.io/PRAHARI/ |

Demo scripts (what to click on camera):

- `05_Output/deliverables/own_feed_demo_script.md`
- `05_Output/deliverables/gov_feed_demo_script.md`

Gov video: open **cam04 from the Cameras table**. Do **not** run FRS. If OCR is empty, Confirm plate and say it is operator confirm.

---

## C. Official written requirements — where they live

### 1. Solution presentation

Covered in `PRAHARI-Slides.pdf` and `PRAHARI-Notes.pdf`: hybrid justification; overview; architecture + E2E workflow; ANPR / objects / lawful FRS / intrusion; watchlist + alerts; stack; 80k **DESIGN TARGET** scale, interop, security; cost of the intelligence plane (~₹5–6 Cr / yr DESIGN TARGET).

### 2. High-level design

`04_Documents/PRAHARI_HLD.md` sections 1–15: architecture, heterogeneous onboarding, live ingest (RTSP-TCP, PTS), watchlist correlation, AI engines, alerts, 80k math, prerequisites, cost, integrator table, HTTP surface, tests.

### 3–4. Demonstrations

Platform is running (`02_Code/prahari`). Videos are HUMAN. Own-feed file for recording: `03_Data/recordings/own_feed.mp4` (local; mp4 is gitignored — keep it on the demo laptop).

### Scale bullets (participants should explain)

All written in HLD §5, §10, §12 and the slides: central/regional/edge, GPU DESIGN TARGET vs MEASURED 0, bandwidth, hot/warm/cold, health checks, HA/DR, cost.

---

## D. How a judge runs the platform

```
git clone https://github.com/amitduabits/PRAHARI.git
git checkout gpic-2026-submission
cd PRAHARI/02_Code/prahari
copy .env.example .env
.\run.ps1
```

Open http://127.0.0.1:8080 · user `judge` · password `JUDGE_PASSWORD` from `.env` (example default `set-this-before-submit`). Reconstruct plate **GJ01AB1234**.

Do not commit `.env`. Do not paste Sentinel or judge passwords into the portal except in the optional hosted-login box after you rotate them.

---

## E. Evaluation map (A)

| Area | Packet |
|---|---|
| 01 Test case | Catalogue onboard + HLS viewing + `gov_feed_plates.csv`; **needs your gov YouTube** |
| 02 Presentation | `PRAHARI-Slides.pdf` |
| 03 Architecture | `PRAHARI_HLD.md` |
| 04 Working platform | code on this branch + **both YouTubes** |
| 05 Analytics | ANPR/confirm, objects, intrusion, Own-only FRS; timestamps on CSVs |
| 06 Scale | HLD §5/§10 DESIGN TARGET 80,000 cameras |
| 07 Completeness | this file + GitHub; **needs YouTube + Drive + portal receipt** |
