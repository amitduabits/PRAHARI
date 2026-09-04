# I05 — ByteTrack

Prepend `00_MASTER_CONTEXT.md`. AGENT. Depends on I04 (can run after I01 if objects still IoU).

## Goal

Object `track_id` can come from ByteTrack. Scene cut still resets.

## Agent

1. `objects.detect` after boxes: if `TRACK_ENGINE=bytetrack`, call `bytetrack_backend.update(camera_id, dets)` and write `track_id`. Else existing IoU.
2. `objects.reset` also calls `bytetrack_backend.reset`.
3. Capture scene-cut already calls `objects.reset`. Confirm with T-V06 and existing `test_scene_cut.py`.
4. His `tracker.get_tracklet` may be ported as `GET /api/tracklet/{event_id}` P1. Skip if time is short; GIS plate track remains the evaluation test.

## Done when

- IoU path default green.
- CSV I05-* DONE.

## Do not

Replace `GET /api/track/{plate}` with ByteTrack. That API is the designated-vehicle test.
