# Onboard failures

Client: PRAHARI `StreamSession`, OpenCV `CAP_FFMPEG`, `rtsp_transport=tcp`.

No live catalogue sync has been run (`SENTINEL_HOST` empty). Do not report a camera as down until `/api/ingest` shows `live: true` and a TCP or HLS probe fails.

| camera_id | url | UTC | error |
|---|---|---|---|
| | | | none (host not configured) |
