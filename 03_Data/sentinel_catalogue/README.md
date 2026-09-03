# Sentinel catalogue cache

Live portal (2026-09-03): `https://cctv.corp8.cloud/` with the team access password in `.env` as `SENTINEL_PASSWORD`.

```
# after POST /auth/login (cookie `sentinel`)
curl -s https://cctv.corp8.cloud/cameras.json -o catalogue.last.json
```

The live manifest is a JSON array of `{id, name}`. HLS is `https://cctv.corp8.cloud/<id>/index.m3u8` and requires a browser User-Agent. RTSP is on the public IP from the live `/resource` page (`SENTINEL_RTSP_HOST`), not on the TLS hostname. `/api/ingest` is 404 on this host.

Keep `catalogue.last.json` out of git. Camera ids still come from the JSON; do not invent them.
