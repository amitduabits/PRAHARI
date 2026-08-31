# Problem statement — Gujarat CCTV Hackathon 2026

Source: https://sentinel.gujarat.gov.in/problems  
Archived for PRAHARI: 2026-08-31

## Background

26 Government Departments operate independent CCTV systems across the State. Analog and IP cameras. Sites from border districts to Valsad, Dahod, Somnath, Jamnagar, Dwarka. Some cloud storage, some local NVR. Retention 7 days in some estates, 15 days or more in others.

Usage differs:

- Home Department: public domain, traffic, law and order, crime detection.
- Food & Civil Supplies: godowns, PDS shops.
- RTO: offices, testing tracks, checkpoints.

The Government intends to integrate government cameras deployed in the public domain into a unified video management and analytics ecosystem. The solution should also support viewing of public-facing CCTV installed by societies, malls, commercial establishments and other private entities, wherever feasible and permitted.

Critical databases already exist: VAHAN, SARTHI, eGujCop (CCTNS), AFIS, NAFIS — arrested persons, stolen vehicles, wanted criminals, missing persons, unidentified dead bodies, fingerprint data. The CCTV system should be integrated with these for automated real-time alerts.

Core goal: a secure, scalable, interoperable, technically feasible, cost-effective approach that uses existing infrastructure to the maximum practical extent.

## Key challenges

1. Heterogeneous infrastructure — vendors, VMS, AMC, storage, camera types, formats, feed-sharing protocols.
2. Geographical dispersion — ~1,000 km.
3. Unified analytics across onboarded cameras.
4. Scalability to new cameras, departments, systems, and future analytics without major redesign.

## Reference models

Model 1 is the common CCTV registry and GIS foundation and may support Models 2, 3, and 4.

| Model | Name | PRAHARI stance |
|---|---|---|
| 1 | Centralised CCTV Registry & GIS Mapping | Mandatory foundation. Build now. No live video required for this layer. |
| 2 | Unified Viewing & Metadata Analytics | Direct RTSP / ONVIF / vendor API. ANPR, tagging, video wall. Build now. |
| 3 | VMS Federation & Middleware | Adapter/plugin + event bus. PRAHARI takes a thin slice: detection JSON bus, not a vendor-SDK zoo. |
| 4 | Central VMS | Full ingest, tiered storage, FRS, 80k recording. Phase-2 selected cameras only. |
| Hybrid | Combine models | This is PRAHARI. |

All solutions should use open-source technologies. Recommended: React, Python, Node.js, PostgreSQL, PostGIS, WebRTC, RTSP, Kafka, RabbitMQ, TensorFlow, PyTorch, FFmpeg, GStreamer, Leaflet, OpenLayers.

## Expected solution approach

Continuously process CCTV feeds from the hackathon portal. Integrate with a searchable watchlist (stolen vehicles, wanted persons, missing persons, blacklisted vehicles, suspects). AI analysis and automated alerts on match. Teams create and use representative datasets. During evaluation, identify specified vehicles from the feeds and generate accurate real-time alerts.

Cover: overall architecture, integration strategy, AI and video analytics, cybersecurity, deployment, infrastructure sizing, cost-benefit, department-wise information requirements, scalability, future roadmap.

Architecture shall be open, modular, scalable, secure, standards-based, vendor-neutral. No vendor lock-in.
