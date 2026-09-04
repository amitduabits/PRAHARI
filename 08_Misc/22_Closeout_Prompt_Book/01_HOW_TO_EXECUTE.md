# How to execute this book (04–11 Sep 2026)

Build engine: one agent conversation = `00_MASTER_CONTEXT.md` + exactly one `phases/C*.md`.  
Humans: Tesseract, consented face photos, screen records, YouTube, Drive, portal.

## Daily loop

1. Open `csv/closeout_actions.csv`. Filter `priority=P0` and `status!=DONE`.
2. If `assignee=agent`, new conversation: master context then the matching phase file.
3. If `assignee=lead|arnav|aria`, that person does it the same day. Do not queue it behind coding.
4. After each phase: `cd 02_Code/prahari` then `python -m pytest -q` and `python scripts/audit_gate.py`.
5. Tick the CSV. Push `main` if public files changed. Never commit `.env`, `prahari.db` with secrets, or `catalogue.last.json` if it contains a session cookie.

## Critical path (first prize dies if any one fails)

| Gate | Why | Owner | Date |
|---|---|---|---|
| Own-feed Unlisted YouTube ≤3 min, real backend | Official demo 3 | Lead | 05 Sep |
| Gov-feed Unlisted YouTube ≤3 min + CSV | Official demo 4 | Lead | 05 Sep |
| Drive Anyone+Viewer for `gov_feed_plates.csv` | Official how-to-submit | Lead | 05 Sep |
| Incognito every URL | Eval 07 | Lead | 06 Sep |
| Portal upload before 12:00 IST 07 Sep | Hard lock | Lead | 07 Sep morning |

Analytics expansion (C01–C08) **raises eval 05 and bonus**. It does not replace the videos. If a phase overruns, record the videos on the current ANPR/confirm backend and keep coding analytics in parallel for a possible re-shoot on 06 Sep.

## Day map

| Day | Date | Agent | Human |
|---|---|---|---|
| D4 | **04 Sep (today)** | C00, C01, C02, C03, C04, C05 | Install Tesseract. Two consented adult face photos into `03_Data/samples/faces/`. |
| D5 | 05 Sep | C06, C07, C08, start C09 | Own-feed video. Gov-feed video. Drive CSV. |
| D6 | 06 Sep | C09 remaining, C10, C11, C12 | Re-shoot if new analytics are green. Incognito. |
| D7 | **07 Sep before noon** | C14 support only | Portal. Receipt. Freeze. |
| D8–D11 | 08–11 Sep | Finale runcard | Bag, rehearsal, iHub. |

## Parallel tracks (do not serialise)

- **Track A (agent):** C01–C08 analytics + tests + experiments.
- **Track B (Lead + Aria):** own-feed video from `own_feed_demo_script.md` (update after C07).
- **Track C (Lead + Arnav):** gov-feed video from `gov_feed_demo_script.md`. FRS is **off** on gov cameras.
- **Track D (Lead):** PPT/HLD after C12. Portal.

## Gates between phases

```
C00 pytest green and audit_gate PASS
     │
     ├─ C01 schema  ── tests/test_event_schema.py
     │
     ├─ C02 objects ── tests/test_objects.py     ─┐
     ├─ C03 FRS     ── tests/test_faces.py        ├─ C05 matcher ── C07 UI ── C08 harness
     └─ C04 intrusion── tests/test_intrusion.py  ─┘
                                                      │
                                            C06 ANPR ─┤
                                                      ▼
                                            C09 live experiments
                                            C10 scale bench
                                            C11 privacy
                                            C12 docs
                                            C13 videos (human)
                                            C14 submit (human)
```

## Do not start

- Training a detector from scratch.
- Enrolling faces cropped from `cctv.corp8.cloud`.
- Kafka / Kubernetes / Ceph.
- Rebuilding catalogue/HLS/RBAC.
- Polishing CSS after the portal receipt.
