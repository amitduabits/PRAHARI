# PRAHARI High-Level Design
**Gujarat Police Innovation Challenge 2026 · CCTV Integration**
Team: student team (Lead + Arnav + Aria)  
Architecture class: **Hybrid (Reference Models 1 + 2 + thin 3)**  
PoC target: ~50 Sentinel sandbox cameras  
DESIGN TARGET: ~80,000 statewide cameras. MEASURED PoC is the seeded registry plus live catalogue sync.

Working tree: `02_Code/prahari/` · Integrator guide: `06_References/SENTINEL_Integrator_Guide.md` (source https://sentinel.gujarat.gov.in/resource)

---

## 1. Problem reading (what we are not building)

Departments already own VMS, AMC contracts, NVRs and storage. Replacing them in 7 days, or even in Phase-1, is neither feasible nor cost-effective. Model 4 (central VMS ingesting every frame for 15 days) would require statewide dark fibre, petabytes of hot storage and a GPU farm that a student PoC cannot honestly claim.

PRAHARI therefore **does not rip and replace**. It adds a statewide intelligence plane on top of what already exists.

## 2. Chosen model and justification

| Layer | Source model | Why |
|---|---|---|
| Camera census, GIS, health, gap analysis | Model 1 | Zero disturbance to departmental VMS. Unlocks planning immediately. |
| Unified viewing + ANPR on accessible streams | Model 2 | Direct RTSP / ONVIF / HLS / WHEP. Satisfies the evaluation test case. |
| Event / metadata bus, correlation, alerts | Thin Model 3 | Watchlist matching and cross-camera tracks without a federation SDK zoo. |
| Central recording + full VMS | Model 4 (Phase-2 only) | Selected cameras, not all 80k (DESIGN TARGET). Written as a roadmap, not faked in the PoC. |

This is vendor-neutral: adapters speak open protocols. A new VMS is one connector, not a redesign.

## 3. Logical architecture

```
Dept VMS / NVR / raw camera / private-permitted RTSP
        │  RTSP-TCP · HLS · WHEP · ONVIF · vendor API
        ▼
┌───────────────────────────────────────────┐
│  Ingest adapters + stream session control │  Model 2
└─────────────────────┬─────────────────────┘
                      │ 1 fps sampled frame (not 25 fps video)
                      ▼
┌───────────────┐    ┌─────────────────────┐
│ Registry+GIS  │    │ ANPR / object worker│
│ PostGIS later │    │ edge or regional GPU│
└───────┬───────┘    └──────────┬──────────┘
        │                       │ detection event
        │                       ▼
        │            ┌─────────────────────┐
        └────────────┤ Event bus (Redis/   │  Model 3
                     │ Kafka statewide)    │
                     └──────────┬──────────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
        Watchlist           Vehicle path      Alert / SOC
        matcher             store             dashboard
        VAHAN/SARTHI        GIS replay        RBAC + audit
        eGujCop/AFIS
```

PoC implementation uses SQLite + in-process WebSocket instead of Kafka. The contract (detection event JSON) is the same object that would go on Kafka later.

## 4. Heterogeneous onboarding

Each camera record carries: id, department, owner (Gov / private-permitted), lat/lon, protocol, URL, retention, type, health.

Onboarding paths:
1. Bulk CSV / Excel (Model 1 deliverable).
2. Manual form for a single node.
3. REST API for departmental inventory systems.
4. Sentinel sandbox endpoints published as RTSP / WHEP / HLS.

If RTSP/UDP dies across NAT (official Integrator Guide), the adapter retries with `rtsp_transport=tcp`, then HLS. Health probe flips the pin red after 3 failures.

Private society / mall cameras are first-class rows with `ownership=Private-Permitted` and a legal-consent flag. They never land in a public viewer role.

## 5. Video path and bandwidth math (80k DESIGN TARGET)

Full-HD 25 fps everywhere is the wrong design.

Numbers in this section are **DESIGN TARGET** (statewide intelligence plane), not MEASURED PoC throughput. The laptop PoC camera count is MEASURED from the seeded registry (11 rows) plus any catalogue sync.

Assumption used in cost model (DESIGN TARGET):
- 80,000 cameras
- Only **public-domain + checkpoint** cameras (assume 45,000) run analytics
- Analytics uses **1 frame per second**, 720p JPEG crop ~80 KB
- Metadata event ~500 bytes

Edge / regional worker traffic for analytics:

`45,000 × 80 KB × 1 fps ≈ 3.6 GB/s peak` if naively centralised.

With regional aggregation (5 regions: Ahmedabad, Surat, Rajkot, Vadodara, Bhuj):

`3.6 GB/s / 5 ≈ 720 MB/s per regional GPU site`. Feasible on existing SWAN / GSWAN plus leased wavelengths.

Control-room operators do **not** pull 45k live streams. They pull:
- a video wall of 16–64 selected cameras via HLS/WebRTC
- metadata + crops for everything else

Low-bandwidth sites (Dahod, border outposts): on-camera or on-NVR sampling; only events go upstream.

Hot / warm / cold storage (Phase-2, selected cameras only):
- Hot: 7 days, object store local to region
- Warm: 8–30 days, erasure-coded Ceph / S3
- Cold: 31–90 days, Glacier-class, legal hold only

PoC stores crops + metadata, not full GOP archives.

## 6. AI / analytics

Phase-1 (this submission): ANPR.
Pipeline: sampled frame → plate localisation → OCR → Indian-plate normaliser (`^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{3,4}$`) → event.

PoC engine: OpenCV morphology + Tesseract. Production swap: YOLOv8 / YOLO11 plate detector + PaddleOCR or a commercial ANPR SDK behind the same `recognize()` interface.

Phase-1.5 (bonus if GPU arrives): vehicle make-model, person/vehicle count, intrusion on godown cameras.

Phase-2: FRS only against a lawful watchlist, on dedicated cameras, with a human-in-the-loop confirm. FRS is **not** the evaluation test and is not demo-critical.

## 7. Watchlist correlation and alerts

Watchlist tables (PoC: local Postgres/SQLite; production: read-replicas / APIs):

| Source | Entity |
|---|---|
| VAHAN | stolen / flagged vehicles |
| SARTHI | suspect licence linkage |
| eGujCop / CCTNS | wanted, missing, unidentified dead |
| AFIS / NAFIS | biometric cases (Phase-2) |

Every detection event is matched in O(1) against an in-memory plate set, refreshed from the source APIs every 60 seconds.

Alert object:

```
plate, camera_id, lat, lon, ts, crop_uri, category, priority, source_case_id
```

Priority: CRITICAL (stolen / wanted) → audible + red queue; HIGH → amber; LOW → log only.

Operator ack is audited. Duplicate suppression: same plate + same camera within 120 seconds collapses to one alert with a counter.

## 8. Multi-camera vehicle track (evaluation test)

`GET /api/track/{plate}` returns chronological sightings joined to camera GIS.

Route reconstruction is a time-ordered polyline. No Kalman filter in PoC; Phase-2 adds:
- camera graph (adjacency by road network)
- travel-time sanity window so a plate cannot “teleport”
- interpolation on the road network, not as-the-crow-flies

CSV / PDF report is the evaluators’ artefact.

## 9. Security

- RBAC: `superadmin`, `soc_operator`, `dept_viewer`, `auditor`. Dept viewers see only their cameras.
- Stream URLs never shipped to the browser without a short-lived token.
- TLS on UI and APIs. mTLS between regional workers and the bus.
- Network segmentation: analytics VLAN ≠ enterprise VLAN ≠ camera VLAN.
- Audit table for onboard, watchlist edit, alert ack, report download.
- Privacy: raw video stays in the department that owns it. Centre stores events + crops for watchlist hits. Crops older than retention are purged.
- No public internet exposure of RTSP.

## 10. Scale, HA, operations

| Concern | PoC | Statewide |
|---|---|---|
| Compute | 1 laptop / 1 VM | 5 regional GPU nodes (8×L40S or equivalent) + 2 central API |
| Bus | WebSocket | Kafka 3-az |
| DB | SQLite | PostgreSQL + PostGIS + Redis |
| HA | none | active-active API, regional isolated failure domains |
| DR | git + DB file | daily object-store backup, RPO 15 min metadata, RTO 1 h |
| Observability | `/api/health` | Prometheus, camera-health SLO 99%, alert lag p95 < 5 s |

Horizontal scale unit = regional worker. Adding cameras is a registry row + worker subscription, not a platform rewrite.

## 11. Prerequisites from departments (need this on Day 1 of a real PoC)

- Camera inventory export (CSV) with lat/lon
- Protocol + reachable URL or jump-host
- Whether ONVIF profile S is enabled
- AMC vendor contact for firewall holes
- Retention policy and legal owner
- Written consent for private-permitted feeds
- Watchlist API contract / sample dump from SCRB

## 12. Cost sketch (order-of-magnitude, INR / year, statewide intelligence plane only)

| Item | Assumption | INR |
|---|---|---|
| 5 regional GPU inferencing nodes | capex amortised 3 yr | 1.8–2.4 Cr / yr |
| Object storage for crops + selected video | 2 PB usable | 0.8–1.2 Cr / yr |
| SWAN / leased bandwidth top-up | regional | 0.6–1.0 Cr / yr |
| Integration + SOC software ops | 12 engineers | 1.5 Cr / yr |
| **Total intelligence plane** | | **~5–6 Cr / yr** |

This is *not* the cost of replacing 26 departmental VMS estates. That is the point of the hybrid model.

## 12a. Sentinel integrator compliance

Gated by `02_Code/prahari/tests/test_integrator_laws.py` plus live soak when `SENTINEL_HOST` is set.

| Official checklist | Implementation |
|---|---|
| RTSP over TCP | `OPENCV_FFMPEG_CAPTURE_OPTIONS=rtsp_transport;tcp` before `import cv2`; FFmpeg `-rtsp_transport tcp` |
| No CAP_PROP_FPS / arrival-time metrics | Event time = `CAP_PROP_POS_MSEC`; sampler uses PTS deltas |
| Inter-frame gaps are not disconnects | `StreamSession.read` continues; scene-cut callback on PTS jump |
| Reconnect backoff 2–30 s | `backoff_sleep` |
| Decoder warnings at join are non-fatal | logged, not raised |
| Catalogue is `/cameras.json` | `app/services/catalogue.py`; ids from JSON. Live host has no `/api/ingest`. |
| Mixed H.264 / H.265 and resolutions | per-camera codec/width/height from catalogue |
| Scene discontinuity at loop | `detect_scene_cut` |

Consume only. No publish, no gateway control API, no file download of `/stream/<id>`.

## 13. PoC mapped to evaluation

| Evaluation item | Where it lives |
|---|---|
| Onboard gov + own feeds | `POST /api/cameras`, `POST /api/cameras/import`, `POST /api/cameras/sync-catalogue`, Onboard tab |
| Unified viewing | Operations Leaflet map, `POST /api/sessions`, tokenised `GET /api/stream/{id}` (no RTSP in the browser) |
| ANPR + timestamps | `POST /api/ingest/frame`, `POST /api/ingest/confirm`, `GET /api/detections` |
| Designated vehicle path | `GET /api/track/GJ01AB1234` + `GET /api/track/{plate}/report.csv` |
| Watchlist + realtime alert | `GET/POST /api/watchlist`, `GET /api/alerts`, `POST /api/alerts/{id}/ack`, `WS /ws/alerts` |
| 80k readiness | §5 (DESIGN TARGET) and §10 of this HLD |
| Bonus GIS / gaps / private feeds | Registry + `GET /api/gap-report` |
