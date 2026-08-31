# Evaluation, test case, and submission

Source: https://sentinel.gujarat.gov.in/problems  
Archived for PRAHARI: 2026-08-31

## Technical evaluation / test case

After registration, ~50 geographically distributed cameras are available on the Resources page.

- Cameras span departments, technologies, formats, VMS, storage.
- Onboard them onto one integrated platform.
- Centralised monitoring and AI-powered video analytics.
- Evaluators provide a designated vehicle registration number. Identify, trace, and present movement across the network as it appears at different camera locations and times.
- Continuously cross-reference live CCTV with a representative watchlist. Automated real-time alerts on match. Own representative watchlist is allowed.

### Expected output

- Trace of the designated vehicle using the registration number given at evaluation.
- Complete route: timestamped, location-wise movement history.
- Working watchlist + continuous cross-reference + automated real-time alerts.
- Evidence of integration, analytics, interoperability, scalability, end-to-end performance.

## Submission requirements

1. **Solution presentation (PPT/PDF).** Model justification, overview, architecture, AI approach, watchlist correlation, stack, scale/security/deployment, operational impact.
2. **HLD.** Architecture, heterogeneous integration, stream ingest, watchlist correlation, ANPR/FRS/object tracking, alert workflow, 80k scale, departmental prerequisites.
3. **Own-feed demonstration.** Screen-recorded, maximum 2–3 minutes, live or recorded CCTV of our choice. Must be a fully functional working solution. Mock-ups, animations, simulated interfaces, or concept videos without an operational backend will not be considered. Show onboard, ANPR (or proposed analytics), watchlist match, automatic alert.
4. **Government-feed demonstration.** Onboard government-provided feed(s). Live or recorded viewing. Analytics output. Screen-recorded video plus an output report of detected vehicles or number plates with timestamps.

### How to submit

- Unlisted YouTube, visibility Unlisted.
- Google Drive or OneDrive: Anyone with the link — Viewer.
- Optional hosted URL + test login for the screening committee.
- Optional GitHub or GitLab of the source.

## Evaluation framework

### A. Common evaluation areas

1. Successful test case on government-provided feed.
2. Solution presentation clarity and completeness.
3. Solution architecture (sound, feasible, secure, interoperable).
4. Working platform and demonstration (own feed + government feed).
5. Video analytics output quality (ANPR, detection, timestamps, reports).
6. Scalability and PoC readiness toward ~80,000 cameras.
7. Submission completeness (links, credentials, documents).

### B. Bonus (does not compensate for missing mandatory items)

- Innovative hybrid architecture with operational value.
- Advanced cross-camera vehicle tracking.
- Additional reliable analytics beyond mandatory ANPR.
- Edge-processing / low-connectivity operation.
- Enhanced cybersecurity, privacy, audit, RBAC.
- Operational dashboards, automated alerts, health monitoring, integration-ready APIs.

## Official integrator pre-submission checklist

See `SENTINEL_Integrator_Guide.md` §4. These eight items are also PRAHARI test gates.
