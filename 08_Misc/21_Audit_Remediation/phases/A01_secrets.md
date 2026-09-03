# A01. Rotate secrets (S1)

Prepend `00_MASTER_CONTEXT.md`. HUMAN (Lead). Agent may remind, must not invent passwords.

## Goal

Default passwords and `SECRET_KEY=change-me` cannot appear on a tunnel.

## HUMAN (Lead, now)

In `02_Code/prahari/.env` only:

- Set `JUDGE_PASSWORD` to a new value. Not `set-this-before-submit`.
- Set `ADMIN_PASSWORD` to a new value. Not `admin`.
- Set `SECRET_KEY` to a long random string. Not `change-me`.
- Leave `SENTINEL_PASSWORD` as the live access password. Do not paste it into chat, slides, or GitHub.
- Do not commit `.env`.

Tell the agent only: `A01 rotated` or `A01 not rotated`. Never send the new password in the agent thread.

## Agent

1. Confirm `git check-ignore -v 02_Code/prahari/.env` still ignores.
2. Confirm `.env.example` still has placeholders, not live values.
3. Patch `scripts/preflight_demo.ps1` and `scripts/incognito_preflight.ps1` so they read `JUDGE_PASSWORD` from the environment or from `.env` and do not hard-code `judge:set-this-before-submit` as the only pair. If `.env` is missing, FAIL with that fact.
4. Do not print the password.

## Done when

- Lead states A01 rotated.
- Preflight scripts no longer assume the example password as the only secret.
- CSV A01-001 DONE.

## Do not

Put the new password in `SUBMISSION_PACK.md` until A13 (hosted URL field only, not git if the pack is public). Prefer telling the committee in the form, not in the repo.
