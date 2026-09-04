# PRAHARI

Statewide CCTV intelligence plane from Yushu Excellence Technologies Pvt. Ltd.

PRAHARI is a hybrid intelligence plane: camera registry and GIS, unified viewing and ANPR, and a thin event bus for watchlist match and cross-camera tracks. It consumes live camera catalogues. It does not replace departmental VMS.

## Start here

| Need | Open |
|---|---|
| Clone and run | `README.md` |
| One-page brief | `01_Overview/BRIEF.md` |
| Architecture | `04_Documents/PRAHARI_HLD.md` |
| Stakeholder slides | `04_Documents/PRAHARI-Slides.pdf` |
| Technical notes | `04_Documents/PRAHARI-Notes.pdf` |
| Working tree | `02_Code/prahari/` |

## Folder map

- `01_Overview/` brief
- `02_Code/prahari/` source
- `03_Data/` sample cameras, watchlist, catalogue fixture
- `04_Documents/` HLD, slides, notes
- `05_Output/` track CSV and experiment logs
- `docs/` GitHub Pages index

## Ingest rules

Force RTSP over TCP. Time every event from PTS, never from arrival time or declared frame rate. Reconnect with backoff. Treat decoder warnings at join as non-fatal. Read cameras from `/cameras.json`. Consume only. Never publish to the gateway. Do not treat `/stream/<id>` as a file download.

## Contact

Amit Dua, Yushu Excellence Technologies Pvt. Ltd. Seeded demonstration plate: `GJ01AB1234`.
