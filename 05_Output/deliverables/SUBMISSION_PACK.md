# Submission pack

Form (after profile OTP): https://docs.google.com/forms/d/e/1FAIpQLSeK7bCJ67zyZCF-73iAfRbMUXHtGbYKS5Cz8IgP-ZzQYZLJpw/viewform

Category: Academic, Research and DPIIT Recognised Startup / Individual Participant (student).

| Item | Path or URL | Notes |
|---|---|---|
| GitHub | https://github.com/amitduabits/PRAHARI | live |
| Solution PPT | `04_Documents/PRAHARI_Solution.pptx` | slide 1: student, BITS Pilani, Lead + Arnav + Aria |
| Solution PDF | `05_Output/deliverables/PRAHARI_Solution.pdf` | exported |
| HLD | `04_Documents/PRAHARI_HLD.md` | |
| Investment audit | `04_Documents/PRAHARI_Investment_Audit.md` | DGP / security / Palantir seats; internal |
| Track CSV | `05_Output/deliverables/track_GJ01AB1234.csv` | seeded path; live hits append |
| Own-feed file | `03_Data/recordings/own_feed.mp4` | 130 s plate stand-in; replace with Aria road clip if filmed |
| Own-feed YouTube | pending screen record | Backend ready. Script: `own_feed_demo_script.md`. Own tile 200 (mp4). |
| Gov-feed YouTube | pending screen record | Catalogue sync 200 (30 live). `cam04` HLS playlist 200. Script: `gov_feed_demo_script.md`. Record now before cooldown returns. |
| Gov CSV | `gov_feed_plates.csv` | 2 confirm rows `GJ01AB1234` on `cam04`. Tesseract not on PATH. Upload Drive Anyone+Viewer. |
| Hosted URL | http://127.0.0.1:8080 (local; no public tunnel) | `admin` / `admin` or `judge` / `JUDGE_PASSWORD`. Do not put this on the public internet. |
| Onboard log | `onboard_failures.md` | 30 cameras from `/cameras.json`; cam01 and cam04 RTSP-TCP live |

Do not commit `.env`. Web host: `cctv.corp8.cloud`. RTSP: `103.250.160.189:8554`. Access password lives only in `.env` as `SENTINEL_PASSWORD`.
