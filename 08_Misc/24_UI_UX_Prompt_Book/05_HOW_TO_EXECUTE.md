# How to execute

## Agent

One phase per conversation. Prepend the FRS / hybrid / DESIGN TARGET laws from `08_Misc/22_Closeout_Prompt_Book/00_MASTER_CONTEXT.md` if that file is in context; otherwise keep: no Paldi FRS, no live-ministry claims, 80k only next to DESIGN TARGET.

Work only in `02_Code/prahari/app/static/` plus new tests under `tests/`. Do not restyle GitHub Pages `docs/index.html` unless asked.

After U01–U07:

```
cd 02_Code/prahari
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts\audit_gate.py
```

Both must pass. Then fill `csv/ux_actions.csv`.

## HUMAN

U08: 1280×720 window, `judge` login, screenshot Operations, Alerts, Track, Cameras, Onboard. Save under `05_Output/experiments/ux/`. Then decide: re-record C13 or keep the old video if time is gone.

## Parallelism

Do **not** run U01–U06 in parallel. Tokens first, then shell, then panels. Parallel restyles fight.

C13 videos outrank this book if the calendar is 06–07 Sep. See `REMAINING_TO_WIN.md`.
