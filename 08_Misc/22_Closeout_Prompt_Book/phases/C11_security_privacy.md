# C11 — Security and FRS privacy tests

Prepend `00_MASTER_CONTEXT.md`. AGENT.

## Goal

Eval bonus cybersecurity/privacy is demonstrated as tests, and FRS cannot be turned into public-face scraping.

## Agent

1. Extend `tests/test_security.py`:
   - home.viewer POST /api/faces/enroll → 403
   - auditor POST /api/ingest/confirm-face → 403
   - unauthenticated analyse → 401

2. `tests/test_privacy_frs.py`: read `app/services/analyse.py` (and faces.py) as text; assert a refuse on `cam` prefix or ownership Gov exists. Also runtime: analyse on Gov camera with a face fixture yields zero person events.

3. `tests/test_honesty.py` as in C06 if not already added.

4. Run `python scripts/audit_gate.py`. Must still PASS. If new files mention `live VAHAN`, fix the words.

5. Confirm GET /api/faces/gallery has no key named embedding, descriptor, or lbph.

## Done when

- pytest security + privacy + honesty green.
- audit_gate PASS.
- CSV C11-* DONE.

## Do not

Log raw face embeddings. Store gov-camera crops in data/faces/. Weaken path jail.
