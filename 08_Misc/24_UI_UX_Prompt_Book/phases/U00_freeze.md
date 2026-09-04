# U00 — Freeze demo strings

AGENT. No visual restyle yet.

## Goal

Restyle cannot break the 3-minute scripts or honesty tests.

## Agent

1. Confirm `GET /` contains: Analyse this still, DESIGN TARGET, 80,000, Enroll, Reconstruct, Confirm plate, seven `data-tab` values.
2. Add `tests/test_ux_freeze.py` that asserts those strings (duplicate of honesty/tabs is fine; this file is the UX contract).
3. List current `.kicker`, gold, Segoe in a 10-line comment at the top of the new test so U01 knows what to kill.
4. Tick U00-001.

## Done when

pytest includes the freeze test and it passes on the **current** UI (before restyle).

## Do not

Change CSS yet.
