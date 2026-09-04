# I03 — FRS law vs Arnav’s ingest

Prepend `00_MASTER_CONTEXT.md`. AGENT. Depends on I02.

## Goal

His bug was: `ingest_frame` always built `FaceAnalyzer` and ran faces on every camera. Ours must not.

## Agent

1. Read `engines_for()` in `analyse.py`. Keep the drop of `faces` for Gov and `cam\d+`.
2. `POST /api/ingest/frame` stays ANPR-only (already). `POST /api/ingest/analyse` is the multi-engine door. Do not copy his ingest_frame face loop onto `/frame`.
3. Lazy-init FaceAnalyzer **inside** the faces branch of `analyse()` after `engines_for` has allowed `faces`.
4. Test T-V04: monkeypatch `FACE_ENGINE=facenet`, POST analyse to `cam04` with a face-like PNG, assert zero person events **and** that a module-level `_face_analyzer` global is still None (or FaceAnalyzer.__init__ was not called). A spy/counter on the class is acceptable.
5. `test_privacy_frs.py` source grep still finds `frs_refused`.

## Done when

- T-F04, T-F05, T-V04 green.
- CSV I03-* DONE.

## Do not

“Fix” by running faces then deleting person events. Never construct the model on a Gov camera.
