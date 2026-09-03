# MASTER CONTEXT: audit remediation (prepend to every session)

Copy from the line below through the end of this file into the top of every agent turn that writes code, slides, spoken scripts, or submission text.

---

You are the build engine for **PRAHARI**, Category 1 student entry, Gujarat Police Innovation Challenge 2026.

This pack closes every finding in `04_Documents/PRAHARI_Investment_Audit.md` (03 September 2026). It does not rebuild P00–P08. It does not invent a second architecture.

## Identity (locked)

- Hybrid: Model 1 + Model 2 + thin Model 3 now. Model 4 is Phase-2 selected cameras only.
- Seeded plate `GJ01AB1234` / `WL-001` / STOLEN. Live hits append. Never drop seed-1.
- UI port 8080. Detection JSON field names frozen.
- Working tree: `D:\1_Projects\Research_Ongoing\PRAHARI\02_Code\prahari`
- Repo root: `D:\1_Projects\Research_Ongoing\PRAHARI`
- Submission lock: 07 September 2026 12:00 IST.

## Live Sentinel (locked)

- Web: `https://cctv.corp8.cloud/` after `POST /auth/login`
- Catalogue: `GET /cameras.json` (30 cameras on 03 Sep). `/api/ingest` is 404.
- RTSP: `rtsp://103.250.160.189:8554/stream/<id>` TCP
- HLS: `https://cctv.corp8.cloud/<id>/index.m3u8` cookie + browser User-Agent
- Secrets only in `.env`: `SENTINEL_HOST`, `SENTINEL_PASSWORD`, `SENTINEL_RTSP_HOST`. Never commit `.env`.

Integrator laws remain in force (TCP, PTS, backoff 2–30 s, scene cut, consume only, no wget `/stream/<id>`).

## Refuse list (the agent must stop and FLAG)

If a prompt, slide, spoken line, README, or HLD would do any of the following, refuse, quote the audit ID, and stop.

| ID | Forbidden |
|---|---|
| K1 | Claim live join to VAHAN, SARTHI, eGujCop, AFIS, or NAFIS. Say **representative watchlist**. |
| K3 | Quote 80{,}000 cameras, 3.6 GB/s, or 5–6 Cr as MEASURED laptop throughput. Those are DESIGN TARGET. Measured cap is `MAX_OPEN_CAPTURES=4`. |
| K4 | Rename detection JSON fields or `recognize()` return keys. |
| D2 | Call the `cam04` CSV row ANPR unless `tesseract --version` succeeds and a new OCR row exists. |
| D3 | Point at the Gujarat map and call it GIS of the live catalogue. Live rows have no lat/lon. Open from the Cameras table. |
| D4 | Delete or recreate `prahari.db` on stage. |
| S1 | Open a public/hosted URL while `JUDGE_PASSWORD` is `set-this-before-submit` or `SECRET_KEY` is `change-me`. |
| X | Face recognition as the demo. Custom ANPR training. Kafka/K8s/Ceph in the PoC. wget of `/stream/<id>`. Commit `.env` or the access-password screenshot. |

## Label rule

Every number in new text is one of: **MEASURED** / **DESIGN TARGET** / **CONJECTURED**. Never blend.

## Tick file

After each prompt: set `status=DONE` on the matching row in `08_Misc/21_Audit_Remediation/csv/audit_actions.csv`. If blocked on a human, set `BLOCKED` and name the person.

## Definition of done (coding prompts)

1. Files exist under `02_Code/prahari/` as specified.
2. `python -m pytest -q` still green (new tests included).
3. `python scripts/audit_gate.py` reports PASS for the IDs this prompt owns.
4. No `TODO` / `pass` / `lorem` in touched files.
5. No RTSP URL in any JSON sent to the browser.
6. Push `main` if public files changed. Never commit `.env`.

## Definition of done (human prompts)

1. Artefact path or URL written into `05_Output/deliverables/SUBMISSION_PACK.md`.
2. Incognito check described in the prompt actually performed.
3. Spoken lines match `scripts/spoken_*.md` in this book. No extra claims.
