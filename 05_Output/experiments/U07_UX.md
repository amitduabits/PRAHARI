# U07 duty-desk restyle

**When.** 04 September 2026  
**Files.** `app/static/{index.html,styles.css,app.js}`  
**Tests.** 100 passed, 4 skipped. `audit_gate.py` PASS.

## Score (re-run of `02_CURRENT_AUDIT.md`)

| Block | Before | After |
|---|---|---|
| A Visual | 4 / 16 | **16 / 16** |
| B IA | 8 / 10 | **8 / 10** (plate shortcut still Track-tab; alerts stay own tab) |
| C Forms | 5 / 10 | **10 / 10** |
| D A11y | 4 / 8 | **8 / 8** |
| E Tasks | 6 / 8 | **8 / 8** |
| **Total** | **27 / 52** | **50 / 52** (bar was written as 48; row max is 52). Pass ≥ 40. |

V1–V8 pass: olive-black `--field`, khaki rank stripe, IBM Plex before Segoe, tracking 0, no kicker, 13 px / 34 px rows, square corners, 12 colour tokens (`#d4a017` only as `--high`).

## Contrast (computed)

`--ink` on `--field` and `--panel` ≥ 7:1. `--muted` on `--field` ≥ 4.5:1. `--khaki` on `--field` ≥ 3:1. Log in (`--ink` on `--navy`) ≥ 4.5:1.

## Not done (U08 HUMAN)

1280 px screenshot pack. Re-record C13 on this skin if noon allows.
