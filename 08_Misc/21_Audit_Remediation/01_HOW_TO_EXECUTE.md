# How to execute (04 Sep – 11 Sep 2026)

Build engine: one agent session = `00_MASTER_CONTEXT.md` + one `phases/A*.md`.  
Humans: secrets, Tesseract, videos, Drive, portal.

## Daily loop

1. Open `csv/audit_actions.csv`. Filter `status!=DONE` and lowest `priority`.
2. If `assignee=agent`, new conversation: master context, then that phase file.
3. If `assignee=lead|arnav|aria`, that person does it the same day. Do not queue it behind coding.
4. Run `python scripts/audit_gate.py` from `02_Code/prahari` after every coding phase.
5. Tick the CSV. Push `main` if public files changed. Never commit `.env`.

## Gates (machine)

`audit_gate.py` exit 0 is required before A13 (hosted URL). Exit 0 is required before A14 (incognito) for the code IDs S2 S3 S4 S5 D3 K1 K3.

If the gate fails, do not record videos that depend on the failed claim (K1/K3/D2). Fix the code or the script first.

## Day map

| Day | Date | Must finish | Forbidden that day |
|---|---|---|---|
| D4 | 04 Sep | A00–A05 code. A01 password rotate. A06 Tesseract or confirm lock. A07 GIS banner. A08 claims lock. | Hosted URL. FRS. |
| D5 | 05 Sep | A09 own-feed video. A10 gov-feed video. Rehearse once. | Bonus analytics (W04-002). |
| D6 | 06 Sep | A11 Drive. A13 hosted URL only if gate PASS. A14 incognito all links. | New features. |
| D7 | 07 Sep before 12:00 IST | A15 portal upload. Receipt. Freeze. | CSS. New ANPR engine. |
| D8–D9 | 08–09 Sep | A12 bag: two laptops, `prahari.db`, `own_feed.mp4`, dongle, printed architecture. | db wipe. |
| D10–D11 | 10–11 Sep | iHub. HLS-first if 8554 blocked. Speak hybrid + 1 fps DESIGN TARGET. | wget `/stream/<id>`. |

## Parallel tracks

- **Track S (agent):** A02 A03 A04 A05 A07 A08. Serial inside the track (HMAC tests depend on A04).
- **Track H (lead):** A01 secrets. A09 A10 A11 videos and Drive. A13 A14 A15.
- **Track T (aria/lead):** A06 Tesseract install. If skipped, Track H must use confirm scripts.

Track H videos wait on A08 (spoken words) and A07 (table-open path). They do not wait on A13.

## Do not start

Custom ANPR training. Face recognition. Kafka, Kubernetes, Ceph. Downloading `/stream/<id>`. Rebuilding P00–P08. Polishing CSS after the portal receipt. Opening a tunnel before A01 and `audit_gate.py` PASS.
