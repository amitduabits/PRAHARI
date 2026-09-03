# Finale runcard (10–11 Sep, 3 minutes)

Wi-Fi may die. HLS-first. Consume only.

## Setup (before walking on stage)

1. `cd 02_Code\prahari`
2. `.env` has `SENTINEL_HOST=cctv.corp8.cloud`, `SENTINEL_RTSP_HOST=103.250.160.189`, a set `SENTINEL_PASSWORD`, and a non-default `JUDGE_PASSWORD`. Do not commit `.env`.
3. `.\run.ps1`
4. Login `judge`
5. If `/api/cameras/sync-catalogue` is 503, skip gov tiles and use own-feed + seeded track

## Spoken 3 minutes

| Sec | Click | Say |
|---|---|---|
| 0:00 | Operations map | PRAHARI is an intelligence plane. Departments keep their VMS. |
| 0:20 | Two pins | Model 1 census: health and gaps. Dahod is offline on purpose. |
| 0:40 | Vehicle Track GJ01AB1234 Reconstruct | Designated vehicle, Valsad to Gandhinagar. CSV is the evaluator artefact. |
| 1:10 | Alerts | Watchlist match is automatic. Stolen is CRITICAL. Same plate on the same camera stacks. |
| 1:30 | Live tile or own-feed | RTSP over TCP. If 8554 is blocked we use HLS. Timing is PTS. |
| 2:00 | Onboard confirm if needed | A readable plate cannot fail the demo. |
| 2:20 | Gaps + footer | At 80,000 cameras we sample 1 fps at five regions. About 5–6 Cr a year for the intelligence plane, not a second VMS bill. |
| 2:45 | Alerts | Working backend. Source is on GitHub. |

## If hall network blocks 8554

Use the HLS URL from the catalogue. If the catalogue is 502, play `CAM-OWN-001` from disk and reconstruct the seeded plate.

## Bag

- 2 laptops, chargers, HDMI
- `data/prahari.db`
- `03_Data/recordings/own_feed.mp4`
- Phone hotspot
- Printed architecture one-pager
- Judge password on paper, not on a slide
