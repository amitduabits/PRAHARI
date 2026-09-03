# A07. GIS honesty (D3)

Prepend `00_MASTER_CONTEXT.md`. AGENT.

## Goal

Operators must not think the Gujarat map is the live Sentinel grid. Live rows have lat=0 lon=0.

## Agent

1. `app/static/app.js` `loadCameras`:
   - Keep skipping map pins when `lat === 0 && lon === 0`.
   - Banner or table caption: `Live catalogue cameras have no coordinates. Open them from this table.`
   - Keep the Open tile button on those rows (already added).
2. Health banner: if `sentinel_host_configured`, do not say “on the map” for sandbox cameras.
3. Optional: `GET /api/gap-report` already lists `missing_coords`. Leave that.
4. Do not invent lat/lon for Paldi Circle or any sandbox id. That would be CONJECTURED GIS.
5. `python scripts/audit_gate.py` prints `PASS D3` (detects the table Open button and a “no coordinates” string in `app.js`).

## Done when

- UI states the gap.
- CSV A07-001 DONE.

## Do not

Geocode from Wikipedia and drop pins. That is a lie on camera.
