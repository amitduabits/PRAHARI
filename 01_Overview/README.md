# PRAHARI overview

Unified CCTV intelligence grid for the Gujarat Police Innovation Challenge 2026.

## What we are building

A working platform that:

1. Onboards heterogeneous cameras (Sentinel sandbox ~50 feeds plus own-feed) from the catalogue at `/api/ingest`.
2. Shows them on a GIS map with health and gap reports (Model 1).
3. Opens live RTSP-TCP / HLS / WHEP tiles in one operations view (Model 2).
4. Runs ANPR on sampled frames, normalises Indian plates, writes detection events.
5. Matches detections against a representative watchlist and raises real-time alerts (thin Model 3).
6. Reconstructs the designated vehicle path (`GET /api/track/{plate}`) and exports CSV.

Statewide design target is ~80,000 cameras. PoC target is the Sentinel sandbox plus own-feed. Model 4 central recording is a Phase-2 roadmap item, not a 7-day deliverable.

## What we are not building

- A rip-and-replace of 26 departmental VMS estates.
- Custom ANPR training from scratch.
- Kafka + Kubernetes + Ceph in the laptop PoC.
- Face recognition as the evaluation demo.
- A 15-day central video archive.
- A mock UI with no detection rows in the database.

## Stack (open source, as required)

FastAPI · Leaflet + vanilla JS command centre · SQLite now / Postgres+PostGIS later · FFmpeg · OpenCV · Tesseract · WebSocket now / Redis-Kafka later.

## Where the work lives

- Product design: `04_Documents/PRAHARI_HLD.md`
- Build tree: `02_Code/prahari/`
- Sentinel contract: `06_References/SENTINEL_Integrator_Guide.md`
- Clone and run: repository root `README.md`
