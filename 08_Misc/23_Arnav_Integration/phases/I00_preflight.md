# I00 — Preflight

Prepend `00_MASTER_CONTEXT.md`. AGENT.

## Goal

Prove C00–C12 still hold before any Arnav file is copied.

## Agent

1. `cd D:\1_Projects\Research_Ongoing\PRAHARI\02_Code\prahari`
2. `.\.venv\Scripts\python.exe -m pytest -q`
3. `.\.venv\Scripts\python.exe scripts\audit_gate.py`
4. Write `05_Output/experiments/I00_PREFLIGHT.md` with pass counts and SKIP list.
5. Confirm `GET` track GJ01AB1234 is still in tests.
6. Do not copy Arnav files yet.

## Done when

- pytest green (skips only documented).
- audit_gate PASS.
- CSV I00-001 DONE.

## Do not

Clone into `02_Code/prahari`. Change `origin`.
