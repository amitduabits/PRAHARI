# I07 — Person enroll UI and pending_review

Prepend `00_MASTER_CONTEXT.md`. AGENT. Depends on I02, I06.

## Goal

A judge can enroll a consented adult photo into WL-004 from the Watchlist tab. Low-confidence reconstructed faces sit in pending_review.

## Agent

1. `index.html` Watchlist: add his “Enroll Missing/Wanted Person” form, posting `/api/faces/enroll`. Keep our entity_type columns.
2. `app.js` handler. Viewer 403 already from API.
3. Alerts renderer: if `status==pending_review`, show that word. Ack still works for open.
4. `store.insert_alert` accepts `pending_review`.
5. Tests T-V10.

## Done when

- GET `/` contains Enroll. home.viewer enroll 403.
- CSV I07-* DONE.

## Do not

Enroll from a Sentinel still. Eighth top-level tab.
