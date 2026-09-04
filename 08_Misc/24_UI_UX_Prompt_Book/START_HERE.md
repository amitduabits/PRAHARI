# Start here — PRAHARI duty-desk UI (not another AI dashboard)

**Problem.** The running UI (`app/static/index.html` + `styles.css`) reads as a generic 2024–26 agent skin: navy void, gold accent, tracked uppercase kicker, Segoe UI, identical bordered panels. A Home Department judge will clock that in under five seconds. It does not look like a Gujarat Police duty desk.

**This book.** Client research, a scored audit of the current screens, a locked visual direction, and **measurable pass/fail bars**. It does not invent engines. It restyles and re-labels the seven existing tabs.

## Read in this order

1. `01_CLIENT_RESEARCH.md` (who sits in front of this, what they already use)
2. `02_CURRENT_AUDIT.md` (why it looks generated, with file evidence)
3. `03_DESIGN_DIRECTION.md` (one aesthetic; locked tokens)
4. `04_QUANTIFIED_BAR.md` (numbers an agent or a test can fail)
5. `05_HOW_TO_EXECUTE.md`
6. `csv/ux_actions.csv`
7. Exactly one `phases/U*.md` per conversation

## Hard order

```
U00  freeze: 7 tabs, DESIGN TARGET footer, Analyse this still, FRS copy, no eighth tab
U01  tokens + type in styles.css (kill gold/navy/kicker/Segoe)
U02  shell: header, tabs, login, footer density
U03  Operations: 10-foot map + wall
U04  Alerts: 3-foot queue (CRITICAL first, ack 1 click)
U05  Cameras + Track tables (sticky header, labels not placeholders)
U06  Watchlist + Onboard + Gaps forms (visible labels, no <pre> as primary)
U07  tests: contrast, anti-slop greps, a11y, tabs still 7
U08  HUMAN: 1280px screenshot pack before re-recording C13
```

## Do not

- Install React, Tailwind, shadcn, Lucide, Inter, purple gradients, glass cards.
- Add an eighth top-level tab.
- Delay C13 YouTube past 06 Sep for polish. If both cannot fit, **record first**, restyle second, re-record Operations + Alerts only if time remains.
- Put the Gujarat Police emblem as a stretched hero. A 24×24 mark in the header is enough.
- Use flag saffron/green as chrome.
- Claim this is CCTNS or eGujCop.

## Strengths that must survive

Hybrid 1+2+thin 3. Sentinel `/cameras.json`. RTSP never in the browser. `GJ01AB1234` reconstruct. Confirm `source=operator_confirm`. FRS Own-only. Footer DESIGN TARGET 80,000. Vendored `hls.min.js`.
