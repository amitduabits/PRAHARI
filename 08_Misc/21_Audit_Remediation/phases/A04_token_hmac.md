# A04. HMAC and password compare (S4)

Prepend `00_MASTER_CONTEXT.md`. AGENT.

## Goal

Stop truncating HMAC. Stop using `==` on passwords.

## Agent

1. `app/auth.py` `_sign`: return `hmac.new(...).hexdigest()` with no slice.
2. `lookup_user`: use `hmac.compare_digest` on passwords. If lengths differ, compare against a dummy digest so you do not early-return on length in a way that leaks (hash both with the same secret and compare, or pad via compare_digest on utf-8 bytes only when `len` matches; if lengths differ return None after a dummy `compare_digest` of two equal-length zeros).
3. Keep `compare_digest` on session and stream signatures.
4. Tokens remain query-string for HLS (browser limitation). Do not spend this session moving them to cookies. Document in a one-line comment in `stream.py`: query token expires in `STREAM_TOKEN_TTL_S`.
5. `tests/test_security.py` still passes. Add a test that a tampered password fails lookup.
6. `python scripts/audit_gate.py` prints `PASS S4`.

## Done when

- No `[:32]` on the HMAC in `auth.py`.
- `lookup_user` uses `compare_digest`.
- CSV A04-001 DONE.

## Do not

Change cookie format field order. Do not log tokens.
