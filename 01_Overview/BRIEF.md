# PRAHARI one-page brief

**Product.** Statewide CCTV intelligence plane. Yushu Excellence Technologies Pvt. Ltd. Collaborator: Amit Dua.

**The deployed problem.** 26 departments run independent CCTV estates (analog and IP, cloud and local NVR, 7-day vs 15-day retention) across ~1,000 km. Watchlists already exist (VAHAN, SARTHI, eGujCop, AFIS, NAFIS) and are unused by the cameras that could match them. There is no statewide camera census.

**Chosen architecture.** Hybrid. Registry + GIS now. Direct RTSP / HLS / WHEP / ONVIF viewing + ANPR now. Thin event bus (detection events, watchlist match, cross-camera track) now. Central VMS recording only for selected cameras on the roadmap.

**What operators demonstrate.** Onboard heterogeneous cameras from a live catalogue. Identify a designated vehicle registration number across the grid. Reconstruct route, timestamps, locations. Continuously match live detections to a representative watchlist and raise automated alerts.

**The ingest contract.** Every camera is a live RTP/RTSP stream. Catalogue `GET /cameras.json` (session cookie) is the source of truth. RTSP for inference. HLS for dashboards. TCP transport is mandatory. Timing is PTS. Feeds loop; expect a hard scene cut. There is no file download.

**PoC claim.** Registry of government + private-permitted cameras; unified viewing; ANPR with Indian-plate normaliser; watchlist hit on `GJ01AB1234` (seeded STOLEN, live hits append); GIS route + CSV; health and gap report; open adapter so a new VMS is one connector. Lawful face matching on Own cameras only.

**Cost honesty.** Intelligence plane ~₹5–6 Cr / year statewide (5 regional GPU sites, crops not 25 fps video, 1 fps analytics). Not the cost of replacing 26 VMS contracts.
