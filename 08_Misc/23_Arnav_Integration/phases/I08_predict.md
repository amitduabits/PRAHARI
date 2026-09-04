# I08 — Next-camera predict

Prepend `00_MASTER_CONTEXT.md`. AGENT.

## Goal

Bonus: given GJ01AB1234, name likely next cameras from historical transitions, else GIS neighbours.

## Agent

1. Port the **logic** of his `predictive.py` into `app/services/predict.py` (not a raw router copy if it mixed concerns). Use our `store.list_detections` / `haversine_km`.
2. Router `GET /api/predict/{plate}` auth required.
3. Track tab: button “Next cameras” showing the JSON list.
4. Test T-V08: seeded six-point path produces a list or honest empty; never 500.

## Done when

- Predict does not drop seed track tests.
- CSV I08-* DONE.

## Do not

Call this Kalman or Re-ID. It is frequency + distance.
