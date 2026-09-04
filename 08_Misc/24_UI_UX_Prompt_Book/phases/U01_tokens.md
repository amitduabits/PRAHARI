# U01 — Tokens and type

AGENT. Depends on U00.

## Goal

`styles.css` `:root` matches `03_DESIGN_DIRECTION.md`. Gold is no longer the brand. Tracking dies.

## Agent

1. Replace `:root` with the locked tokens. Map old `--ok/--bad/--accent` usages to `--live/--critical/--khaki` or `--high`.
2. `html, body { font-family: var(--sans); font-size: var(--fs); }`
3. `h1 { letter-spacing: 0; font-size: 18px; font-weight: 600; }`
4. Delete `.kicker` uppercase rules or the class.
5. Vendor IBM Plex Sans + Mono woff2 under `app/static/fonts/` **or** one fonts.google.com link with `display=swap` plus the same stack ending in `Segoe UI, sans-serif` for air-gap.
6. `:focus-visible { outline: var(--focus); outline-offset: 2px; }`
7. Tick U01-*.

## Done when

No `#d4a017` except as `--high`. No `letter-spacing` > 0.02em. Body 13–14 px.

## Do not

Touch HTML copy except dropping the kicker element if CSS requires it. Do not add Tailwind.
