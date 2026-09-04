# HLD changelog

- 04 Sep 2026 closeout: §6 rewritten. Phase-1 now implements ANPR, CPU object detection, godown intrusion, and lawful enrolled-gallery FRS on Own cameras only. Government CCTV never runs FRS. Additive detection fields. §5 notes MEASURED 41 KB mean crop vs 80 KB DESIGN TARGET. §13 lists `/api/ingest/analyse` and object CSV.

- Section 5 bandwidth arithmetic labelled DESIGN TARGET. PoC camera count is MEASURED from the seeded registry.
- Section 12a added: Sentinel integrator compliance mapped to `tests/test_integrator_laws.py` and the capture/catalogue modules.
- Section 13 evaluation table updated to the live FastAPI paths (`/api/sessions`, `/api/stream/{id}`, `/api/ingest/confirm`, `/ws/alerts`, `/api/gap-report`).
- Cost table unchanged: about ₹5–6 Cr per year for the intelligence plane, not a VMS replacement.
