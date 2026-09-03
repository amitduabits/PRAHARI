# A13. Hosted URL (S1, S6)

Prepend `00_MASTER_CONTEXT.md`. HUMAN. **Gated.**

## Gate (must all be true)

- Lead completed A01 (passwords rotated).
- `python scripts/audit_gate.py` exit 0 for S2 S3 S4 S5.
- Bind remains 127.0.0.1 unless TLS or a trusted tunnel is in front.

## HUMAN

1. If using ngrok/cloudflared: tunnel to 8080. HTTPS on the public name.
2. If public HTTPS: set `COOKIE_SECURE=1` in `.env` (agent may add the config key in this session: cookie `secure=True` when that env is 1). Default 0 on localhost.
3. Incognito: login `judge` / rotated password. Reconstruct `GJ01AB1234`.
4. Put hosted URL + `judge` + password **only in the Google form**, not in the public GitHub README. `SUBMISSION_PACK.md` may say “hosted URL issued; password in form” without the secret.
5. Close the tunnel after screening if possible.

## Agent

1. Optional: `app/routers/login.py` `set_cookie(..., secure=bool(config.getenv("COOKIE_SECURE")))`.
2. Refuse to write the live password into any committed file.
3. Refuse this phase if audit_gate fails S2–S5.

## Done when

- Incognito reconstruct works.
- CSV A13-001 DONE or `SKIPPED` if the team chooses not to host (optional on the form).

## Do not

Bind `0.0.0.0` without TLS. Do not leave example passwords.
