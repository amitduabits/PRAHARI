# PRAHARI investment audit

**Date.** 03 September 2026  
**Object.** Student PoC for Gujarat Police Innovation Challenge 2026, Category 1.  
**Working tree.** `02_Code/prahari/`  
**GitHub.** https://github.com/amitduabits/PRAHARI  
**This document is an internal investment review.** It is not a certificate from Gujarat Police, Palantir, or any named officer.

Three seats reviewed the same tree, the live Sentinel portal on 03 September 2026, and the pytest run the same day (33 passed, 1 skipped). Each seat writes in that seat's job, not in marketing copy.

Severity used below: **Blocker** (do not submit or host until closed), **High** (close before a public URL), **Medium** (close before the 10–11 September finale), **Low** (backlog).

---

## Committee verdict

Ship the Phase 1 packet if the human video and Drive links exist by 07 September 2026, 12:00 IST. Do not host the box on the public internet until default passwords and `SECRET_KEY` are rotated. Do not tell a DGP this is a statewide VMS. It is a laptop intelligence plane that already onboards the live catalogue, reconstructs `GJ01AB1234`, and writes a detection row for a sandbox camera.

Capital at risk if you treat this as production: operator passwords, Sentinel access cookie, HMAC `SECRET_KEY=change-me`, stream tokens in query strings, no TLS on port 8080, Tesseract absent so OCR is unproven on live frames, and two Unlisted YouTube files that do not yet exist.

---

## Reviewer 1. Director General of Police (operational seat)

Question asked: if a stolen car is on NH-48 tonight, what does a SOC operator actually do, and what fails in court?

### What already works for a duty officer

The product keeps departmental VMS in place. That is the correct political and operational move. Twenty-six AMCs are not ripped out in a student week.

The designated plate `GJ01AB1234` (watchlist `WL-001`, category STOLEN) reconstructs Valsad NH-48 Toll, Surat Adajan Circle, Narol–Naroda, SG Highway, Koba Circle, Gandhinagar Sector 21. A live operator confirm on Sentinel camera `cam04` (Paldi Circle) at 11:40 IST on 03 September 2026 appended. The six seed points remained. That is the evaluation test the Home Department wrote down.

Alerts are priority-coloured. Stolen is CRITICAL. The same plate on the same camera within 120 seconds increments a counter instead of flooding the wall. Ack writes an audit row. `home.viewer` does not see the private-permitted mall camera. Private onboard requires `consent=true`.

Dahod GSRTC is seeded offline on purpose. Food and Civil Supplies cameras are flagged for 7-day retention. A DGP can point at a gap report and ask a department why a pin is red. That is more useful than a fake green grid.

### What a DGP will reject

Face recognition is not the demo. Good. Do not add it for the finale. A student FRS on a public road camera is a rights problem, not a prize feature.

The live catalogue has no lat/lon. Sandbox cameras therefore do not pin on the Gujarat map. The operator must open `cam04` from the Cameras table. Say that sentence in the video. Do not wave at an empty map and call it GIS of the government feed.

Tesseract is not on PATH. The government CSV row is an operator confirm, confidence 1.0, not an OCR read of Paldi Circle. The official page allows analytics output with timestamps. Confirm is a lawful human attestation. It is not ANPR. Install Tesseract before the iHub demo or say “operator confirm” out loud.

No Unlisted YouTube, no Drive Anyone+Viewer, no changed `JUDGE_PASSWORD` means the screening committee cannot replay the duty cycle. That fails evaluation area 7 and, in practice, area 4.

### DGP findings

| ID | Severity | Finding |
|---|---|---|
| D1 | Blocker | Own-feed and gov-feed Unlisted videos, and the Drive CSV link, are missing. Deadline 07 Sep 12:00 IST. |
| D2 | High | Say on camera that `cam04` is confirm, not OCR, until Tesseract is installed. |
| D3 | Medium | Sandbox cameras have no GIS. Table-open is the honest path. |
| D4 | Low | Seeded path Valsad to Gandhinagar is a representative dataset. Live hits must keep appending. Do not reset `prahari.db` on stage. |

---

## Reviewer 2. Independent security reviewer (application and ingest)

Question asked: who can see a camera, who can mint a token, and where do secrets live if this box is tunnelled to the committee.

### Controls that are present and tested

`GET /api/cameras` without login returns 401. Auditor cannot POST a watchlist row (403). `home.viewer` does not receive `CAM-MALL-001`. Stream JSON to the browser contains no `rtsp://` (`tests/test_no_rtsp_leak.py`). Stream tokens are HMAC-SHA256 truncated, bound to `camera_id`, and expire (`STREAM_TOKEN_TTL_S=60`). Compare on the signature uses `hmac.compare_digest`. Sentinel origin cookie stays in the server `httpx` session. The HLS playlist is rewritten to `/api/stream/{id}/hls/{name}?token=`. Segment names must match `^[\w.\-]+$`. Consume-only: no publish helper in capture or catalogue. SQL uses named parameters.

Integrator laws are encoded: RTSP TCP env flag before `import cv2`, PTS not `CAP_PROP_FPS`, backoff 2–30 s, scene cut on PTS rewind or gap above 5 s.

### Failures that matter if the host leaves 127.0.0.1

Passwords in `config.users()` are compared with `==`, not `compare_digest`. Default `JUDGE_PASSWORD=set-this-before-submit`, `ADMIN_PASSWORD=admin`, `SECRET_KEY=change-me`. Session cookie is `httponly` and `samesite=lax`, and is not `Secure`, because the bind is HTTP on 8080. HTTP Basic is offered as a fallback (`WWW-Authenticate: Basic`). A reverse-proxy without TLS ships passwords in clear text.

Stream tokens travel in the query string. They will land in access logs, browser history, and any Referer if a future asset is off-origin. `hls.min.js` is loaded from `cdn.jsdelivr.net`. That is a supply-chain and offline-hall risk. Vendor the file.

`resolve_media_path` joins a camera `url` onto the app root and `.resolve()`s it. A write-role user who onboards `protocol=file` with `url=../../somewhere` can point `FileResponse` at any readable path the process can open. Bound the resolve inside `03_Data/` or `data/`.

`origin_get` follows the camera’s `hls` URL with the Sentinel cookie attached. If an operator pastes a non-Sentinel HLS URL into a camera row, the process will fetch it (SSRF with the team cookie on requests that happen to hit `cctv.corp8.cloud`). Restrict origin host to `SENTINEL_HOST`.

HMAC digest is sliced to 32 hex characters (128 bits of hex, 16 bytes). Use the full hex digest.

Process-wide Sentinel session is never rotated on a timer. A stolen process memory dump holds the live grid cookie.

`.env` is gitignored. Confirm `git check-ignore -v .env` before every push. The access password screenshot must stay out of git (`07_Communications/*.png`, `/Screenshot*.png`).

### Security findings

| ID | Severity | Finding |
|---|---|---|
| S1 | High | Rotate `JUDGE_PASSWORD`, `ADMIN_PASSWORD`, `SECRET_KEY` before any hosted URL. Bind TLS or keep the tunnel authenticated and short-lived. |
| S2 | High | File-protocol path is not jailed. A write user can read arbitrary files via `/api/stream`. |
| S3 | Medium | HLS origin fetch is not pinned to `SENTINEL_HOST`. |
| S4 | Medium | Stream token in query string; HMAC truncated; password `==` compare. |
| S5 | Medium | `hls.min.js` from jsDelivr. Copy it into `app/static/`. |
| S6 | Low | Cookie lacks `Secure`. Fine on localhost. Wrong on a public name. |

---

## Reviewer 3. Alexander Karp, Chief Executive Officer, Palantir Technologies

Question asked: is this a data product that fuses sensors and watchlists, or a video-storage company wearing a hackathon badge.

### What is the actual object

The object is an ontology with four types: Camera (sensor + department + consent), Plate (normalised identifier), Detection (observation with PTS), Alert (watchlist join). The JSON field names are frozen. That is the right grain. Kafka later is a transport swap, not a redesign. Model 4 central recording of 80{,}000 GOP streams is a storage business. This team correctly refused to fake it.

1 fps crops, not 25 fps video to the SOC, is the only bandwidth story that survives contact with SWAN. The 5–6 Cr yearly figure is labelled DESIGN TARGET. Keep saying that. A laptop is not a regional GPU site.

Live catalogue sync of 30 cameras on 03 September 2026 is a real adapter: login cookie, `/cameras.json`, RTSP on `103.250.160.189:8554`, HLS on `cctv.corp8.cloud` with a browser User-Agent. The old `/api/ingest` contract is 404. The code follows the live page. That is how you treat a vendor portal.

### Where the company would fire the demo

A confirm click is not a model. It is a human in the loop, which Palantir would keep, but you still need a detector behind `recognize()`. Tesseract missing means the ANPR interface is unexercised on Paldi Circle. The fixture plate image in tests is not the government feed.

Watchlist rows are a CSV the team typed. There is no VAHAN or eGujCop pipe. Say “representative watchlist”. The official page allows that. Do not say “integrated with VAHAN”.

Scale numbers in the HLD (3.6 GB/s naive, 720 MB/s per region) are arithmetic on assumptions, not a load test of 80{,}000 sessions. `MAX_OPEN_CAPTURES=4` is the measured cap. Speak 4 open tiles and 1 fps as the PoC law. Speak 80k only as the design target.

GitHub is optional on the form and already live. Source is the only durable asset. Videos expire. Keep `main` green.

### Karp findings

| ID | Severity | Finding |
|---|---|---|
| K1 | High | Do not claim VAHAN/eGujCop live join. The table is representative. |
| K2 | High | Put Tesseract on PATH or keep confirm as the spoken method. |
| K3 | Medium | Never quote 80k as measured throughput. The measured cap is 4 captures. |
| K4 | Low | Detection JSON and `recognize()` are the products. Keep them stable. |

---

## Working evidence (shared)

| Claim | State | Label |
|---|---|---|
| pytest | 33 passed, 1 skipped (Tesseract binary) | MEASURED 03 Sep 2026 |
| Catalogue | 30 cameras from `GET /cameras.json` | MEASURED |
| RTSP-TCP | `cam04` 1920×1080, PTS 1080 ms; `cam01` live | MEASURED |
| Track `GJ01AB1234` | 8 cameras, seeds kept | MEASURED |
| Gov CSV | 1 row, confirm, `cam04`, STOLEN | MEASURED |
| Own-feed file | `own_feed.mp4` on disk | MEASURED |
| Own-feed YouTube | missing | BLOCKER for submit |
| Gov-feed YouTube | missing | BLOCKER for submit |
| Drive Anyone+Viewer | missing | BLOCKER for submit |
| Hosted URL | 127.0.0.1:8080 only | optional on the form |
| Tesseract | not on PATH | skip in pytest |
| FFmpeg | not on PATH | HLS proxy used instead of remux |
| Default passwords | still example values in `.env` | High if tunnelled |

UDP SETUP 461 then TCP success is not a down camera. Do not mail SCRB.

---

## Actions before submit (ordered)

1. Record own-feed ≤ 3 min from `own_feed_demo_script.md`. Unlisted YouTube. Incognito play.
2. Record gov-feed ≤ 3 min: sync, Cameras table Open tile `cam04`, confirm or OCR, CSV. Unlisted YouTube.
3. Upload `gov_feed_plates.csv` to Drive, Anyone with the link, Viewer.
4. Change `JUDGE_PASSWORD` and `SECRET_KEY`. Do not commit `.env`.
5. Install Tesseract if you want OCR on camera. Otherwise say confirm.
6. Jail `resolve_media_path` and pin HLS origin before a public tunnel.
7. Vendor `hls.min.js`. Stop calling jsDelivr from the SOC page.
8. After portal receipt, freeze product edits.

---

## What this review is not

It is not a Palantir diligence memo on letterhead. It is not a Gujarat Police sanction. Alexander Karp did not sign it. No Director General signed it. The three seats are the questions a buyer, a CISO, and a DGP would ask. The answers are taken from this repository and from the live portal on 03 September 2026.
