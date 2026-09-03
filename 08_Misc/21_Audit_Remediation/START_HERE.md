# Start here (audit remediation)

Date: 03 September 2026. Phase 1 lock: **07 September 2026 12:00 IST**.

The platform is on GitHub. The investment audit is in `04_Documents/PRAHARI_Investment_Audit.md`. This book is the only remaining execution pack. Do not re-run P00–P08 or W01 catalogue work unless a test is red.

## Read in this order

1. `00_MASTER_CONTEXT.md` (refuse list)
2. `02_CONSTRAINT_REGISTER.md` (every audit ID)
3. `01_HOW_TO_EXECUTE.md` (04–11 Sep, gates)
4. `csv/audit_actions.csv` (tick list)
5. One `phases/A*.md` per session

## Hard order (do not skip gates)

```
A00  preflight + install audit_gate.py
A01  HUMAN: rotate JUDGE_PASSWORD, ADMIN_PASSWORD, SECRET_KEY   (S1)
A02  AGENT: jail file paths                                      (S2)
A03  AGENT: pin HLS origin to SENTINEL_HOST                      (S3)
A04  AGENT: full HMAC + compare_digest passwords                 (S4)
A05  AGENT: vendor hls.min.js, delete jsDelivr                   (S5)
     ----- audit_gate.py must print PASS -----
A06  Tesseract on PATH or lock spoken "operator confirm"         (D2, K2)
A07  AGENT: GIS honesty in UI for lat=0 cameras                  (D3)
A08  AGENT: claims lock in scripts, HLD, slides, notes           (K1, K3)
A09  HUMAN: own-feed Unlisted YouTube                            (D1)
A10  HUMAN: gov-feed Unlisted YouTube                            (D1)
A11  HUMAN: Drive Anyone+Viewer for gov_feed_plates.csv          (D1)
A12  preserve prahari.db; finale runcard                         (D4)
A13  hosted URL only if A01–A05 PASS                             (S1, S6)
A14  incognito dry-run of every URL
A15  portal submit then freeze
```

A09–A11 are blockers for first prize. A02–A05 are blockers for any public tunnel. A01 is human and does not wait on code.

## How to run an agent session

1. New conversation in this repo.
2. Paste `00_MASTER_CONTEXT.md`.
3. Paste exactly one `phases/A0N_*.md`.
4. Tick `csv/audit_actions.csv`.
5. Run `python scripts/audit_gate.py` from `02_Code/prahari`.
6. Push `main` if public files changed. Never commit `.env`.
