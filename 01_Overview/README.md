# PRAHARI overview

Unified CCTV intelligence grid from Yushu Excellence Technologies Pvt. Ltd.

## What this product does

A working platform that:

1. Onboards heterogeneous cameras (lab catalogue plus own-feed).
2. Shows them on a GIS map with health and gap reports.
3. Opens live RTSP-TCP / HLS / WHEP tiles in one operations view.
4. Runs ANPR on sampled frames, normalises Indian plates, writes detection events.
5. Matches detections against a representative watchlist and raises real-time alerts.
6. Reconstructs a designated vehicle path (`GET /api/track/{plate}`) and exports CSV.

Statewide design target is ~80,000 cameras. This tree runs the seeded registry plus live catalogue sync. Central recording of every frame is a roadmap item, not a claim of this PoC.

## What this product is not

- A rip-and-replace of 26 departmental VMS estates.
- Custom ANPR training from scratch.
- Kafka + Kubernetes + Ceph in the laptop PoC.
- Face recognition on government CCTV of unknown people.
- A 15-day central video archive.
- A mock UI with no detection rows in the database.

## Stack

FastAPI · Leaflet + vanilla JS command centre · SQLite now / Postgres+PostGIS later · FFmpeg · OpenCV · Tesseract · WebSocket now / Redis-Kafka later.

## Where the work lives

- Product design: `04_Documents/PRAHARI_HLD.md`
- Build tree: `02_Code/prahari/`
- Clone and run: repository root `README.md`
