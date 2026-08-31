# PRAHARI

Student entry, Gujarat Police Innovation Challenge 2026. Submission lock: 07 September 2026 12:00 IST.

PRAHARI is a hybrid statewide CCTV intelligence plane: Model 1 registry and GIS, Model 2 unified viewing and ANPR, thin Model 3 event bus. It consumes the Sentinel sandbox camera grid. It does not replace departmental VMS.

## Start here

| Need | Open |
|---|---|
| GitHub README (clone and run) | `README.md` |
| One-page brief | `01_Overview/BRIEF.md` |
| Architecture | `04_Documents/PRAHARI_HLD.md` |
| Deck | `04_Documents/PRAHARI_Solution.pptx` |
| Official integrator guide (archived) | `06_References/SENTINEL_Integrator_Guide.md` |
| Working tree | `02_Code/prahari/` |

## Folder map

- `01_Overview/` brief
- `02_Code/prahari/` source
- `03_Data/` sample cameras, watchlist, catalogue fixture
- `04_Documents/` HLD, solution PPT
- `05_Output/` track CSV and submission notes
- `06_References/` official problem, evaluation, integrator guide, prizes
- `07_Communications/` official contacts

## Integrator rules

Force RTSP over TCP. Time every event from PTS, never from arrival time or declared frame rate. Reconnect with backoff. Treat decoder warnings at join as non-fatal. Read cameras from `/api/ingest`. Consume only. Never publish to the gateway. Do not treat `/stream/<id>` as a file download.

## Team

Lead, Arnav, Aria. Student category. Seeded evaluation plate: `GJ01AB1234`.
