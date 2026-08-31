# PRAHARI one-page brief

**Challenge.** Home Department, Government of Gujarat. CCTV Integration Hackathon 2026. Prize pool ₹51 lakh. Student category. Submission 07 Sep 2026.

**The deployed problem.** 26 departments run independent CCTV estates (analog and IP, cloud and local NVR, 7-day vs 15-day retention) across ~1,000 km. Watchlists already exist (VAHAN, SARTHI, eGujCop, AFIS, NAFIS) and are unused by the cameras that could match them. There is no statewide camera census.

**Chosen model.** Hybrid. Model 1 (registry + GIS) now. Model 2 (direct RTSP / HLS / WHEP / ONVIF viewing + ANPR) now. Thin Model 3 (detection-event bus, watchlist match, cross-camera track) now. Model 4 (central VMS recording) only for selected cameras in Phase-2.

**The evaluation test.** Onboard the ~50 Sentinel sandbox cameras published at https://sentinel.gujarat.gov.in/resource. Identify a designated vehicle registration number across the grid. Reconstruct route, timestamps, locations. Continuously match live detections to a representative watchlist and raise automated alerts.

**The Sentinel contract.** Every camera is a live RTP/RTSP stream. Catalogue `GET /api/ingest` is the source of truth. RTSP `rtsp://<host>:8554/stream/<id>` for inference. WHEP for low-latency preview. HLS for dashboards. TCP transport is mandatory. Timing is PTS. Feeds loop; expect a hard scene cut. There is no file download.

**PoC claim we will demonstrate.** Registry of government + private-permitted cameras; unified viewing; ANPR with Indian-plate normaliser; watchlist hit on `GJ01AB1234` (seeded STOLEN, live hits append); GIS route + CSV; health and gap report; open adapter so a new VMS is one connector.

**Cost honesty.** Intelligence plane ~₹5–6 Cr / year statewide (5 regional GPU sites, crops not 25 fps video, 1 fps analytics). Not the cost of replacing 26 VMS contracts.
