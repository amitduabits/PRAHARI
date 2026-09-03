# A05. Vendor hls.min.js (S5)

Prepend `00_MASTER_CONTEXT.md`. AGENT.

## Goal

The SOC page must not load JavaScript from jsDelivr. The iHub hall may be offline. Supply-chain risk.

## Agent

1. Download hls.js 1.5.17 min build into `02_Code/prahari/app/static/hls.min.js` (same version currently cited).
2. `app/static/index.html`: replace the cdn.jsdelivr.net script tag with `<script src="/hls.min.js"></script>`.
3. Confirm `app.js` still uses `window.Hls`.
4. Grep the working tree `app/static` for `jsdelivr` and `cdn.jsdelivr`. Zero hits.
5. `python scripts/audit_gate.py` prints `PASS S5`.
6. `pytest -q tests/test_tabs_smoke.py` green.

## Done when

- Local `hls.min.js` exists and is referenced.
- CSV A05-001 DONE.

## Do not

Bump to an untested hls.js major. Do not load from unpkg either.
