# Constraint register

Source: `04_Documents/PRAHARI_Investment_Audit.md` dated 03 September 2026.  
Every row must reach DONE before the gate in the last column. No row is optional.

| ID | Severity | Constraint | Prompt | Done when | Gate |
|---|---|---|---|---|---|
| D1 | Blocker | Own-feed YouTube, gov-feed YouTube, Drive CSV missing | A09 A10 A11 | Three URLs in `SUBMISSION_PACK.md`; incognito play | Human |
| D2 | High | `cam04` row is confirm, not OCR, unless Tesseract exists | A06 | `tesseract --version` **or** spoken scripts say "operator confirm" | `audit_gate.py D2` |
| D3 | Medium | Live catalogue has no lat/lon; map is not gov GIS | A07 | Cameras table remains the open path; UI states the gap | `audit_gate.py D3` |
| D4 | Low | Do not reset `prahari.db` on stage | A12 | Finale runcard forbids db wipe; seed count stays ≥6 | Human |
| S1 | High | Default passwords / `SECRET_KEY=change-me` on a tunnel | A01 A13 | `.env` rotated, not committed; gate fails if example values | Human + gate |
| S2 | High | `protocol=file` path not jailed | A02 | Resolve confined under app `data/` or `03_Data/`; test 403/400 | `audit_gate.py S2` |
| S3 | Medium | HLS fetch not pinned to `SENTINEL_HOST` | A03 | Off-host HLS URL does not carry the Sentinel cookie | `audit_gate.py S3` |
| S4 | Medium | Token in query; HMAC `[:32]`; password `==` | A04 | Full hex HMAC; `compare_digest` on passwords; tests green | `audit_gate.py S4` |
| S5 | Medium | `hls.min.js` from jsDelivr | A05 | File in `app/static/hls.min.js`; index has no jsdelivr | `audit_gate.py S5` |
| S6 | Low | Cookie `Secure` missing | A13 | `COOKIE_SECURE=1` when public HTTPS; default off on localhost | A13 |
| K1 | High | Must not claim live VAHAN/eGujCop | A08 | Spoken scripts + HLD + slides use "representative watchlist" | `audit_gate.py K1` |
| K2 | High | Tesseract missing; ANPR unproven on Paldi | A06 | Same as D2 | `audit_gate.py D2` |
| K3 | Medium | 80k / 5–6 Cr are DESIGN TARGET | A08 | Those strings sit next to DESIGN TARGET in HLD, notes, slides, scripts | `audit_gate.py K3` |
| K4 | Low | Detection JSON and `recognize()` frozen | locked | Any prompt that renames fields is rejected | Master context |

Committee extras (not numbered in the table, still gated):

- Face recognition stays out of the demo.
- `MAX_OPEN_CAPTURES=4` is the MEASURED capture cap.
- UDP SETUP 461 then TCP success is not a down camera. No SCRB mail.
- After portal receipt: freeze CSS and product edits (A15).
