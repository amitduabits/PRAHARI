# Current UI audit (measurable)

**Files.** `02_Code/prahari/app/static/{index.html,styles.css,app.js}`  
**Scored.** 04 September 2026. Score 0–2 per row. 0 = fail, 1 = partial, 2 = pass. Target after U07: **≥ 40 / 48**.

## A. Visual identity (today 4 / 16)

| ID | Check | Evidence now | Score |
|---|---|---|---|
| V1 | Not navy-void + gold accent | `--bg:#0b1220 --accent:#d4a017` in `styles.css` L1–11 | 0 |
| V2 | Heading letter-spacing ≤ 0.02em | `h1` 0.12em, `.kicker` 0.08em uppercase | 0 |
| V3 | Named font pairing, not Segoe-only | `"Segoe UI", system-ui` | 0 |
| V4 | Red reserved for CRITICAL | `--bad` also colours generic `.err` | 1 |
| V5 | No decorative kicker | `.kicker` “PRAHARI · Gujarat Police…” | 0 |
| V6 | Density: body 13–14 px, row 32–36 px | body inherits 16 px browser default; rows padded 0.35rem | 1 |
| V7 | Corners ≤ 2 px or square | no radius (good) | 2 |
| V8 | ≤ 8 colour tokens | 8 tokens already; gold must go | 1 |

## B. Information architecture (today 8 / 10)

| ID | Check | Evidence now | Score |
|---|---|---|---|
| I1 | Seven tabs, Operations default | `index.html` L33–40 | 2 |
| I2 | Demo verbs visible: Reconstruct, Analyse this still, Open tile, Ack, Confirm | present | 2 |
| I3 | Persistent plate field or `/` shortcut | `/` focuses plate only on Track tab | 1 |
| I4 | Alerts not buried | own tab; not on Operations | 1 |
| I5 | Footer keeps DESIGN TARGET + 80,000 | `index.html` L146 | 2 |

## C. Forms and honesty (today 5 / 10)

| ID | Check | Evidence now | Score |
|---|---|---|---|
| F1 | Every input has a visible `<label>` | login has labels; onboard/watchlist use placeholders as names | 0 |
| F2 | No raw `<pre>` as the primary result | ANPR, analyse, gaps, predict, enroll all `<pre>` | 0 |
| F3 | Confirm not styled as ANPR | separate buttons; good | 2 |
| F4 | FRS Own-only hint on Analyse | `index.html` L122 | 2 |
| F5 | Login does not show `.env` path in the primary sentence | hint L18 names `.env` | 1 |

## D. Accessibility (today 4 / 8)

| ID | Check | Evidence now | Score |
|---|---|---|---|
| A1 | WCAG 2.2 AA text contrast ≥ 4.5:1 | muted `#9aa8bd` on `#0b1220` ≈ 7:1 (pass); gold on navy for `.tab.on` text `#0b1220` on `#d4a017` needs check | 1 |
| A2 | Focus ring ≥ 2 px, 3:1 | no `:focus-visible` rule | 0 |
| A3 | `role="tablist"` + selected state | tablist yes; `aria-selected` missing | 1 |
| A4 | Reduced motion respected | no animation (pass by absence) | 2 |

## E. Operator tasks (today 6 / 8)

| ID | Check | Evidence now | Score |
|---|---|---|---|
| T1 | Open tile ≤ 2 clicks | map popup or table button | 2 |
| T2 | Fifth session error visible | `tile-err` 429 copy | 2 |
| T3 | Ack = 1 click | yes | 2 |
| T4 | Analyse result is a card (plate / class / face), not JSON | JSON in `<pre>` | 0 |

**Today total: 27 / 48.** Direction of travel: kill V1–V5 and F1–F2 first. That is what reads as “AI”.

## Slop grep list (U07 must be zero hits in `app/static`)

Forbidden in CSS/HTML after U01:

- `#d4a017`, `#0b1220`, `#3dd68c` as named accent/ok (replace)
- `letter-spacing` above `0.02em`
- `text-transform: uppercase` on chrome
- `Segoe UI` as the only family
- `glass`, `gradient`, `Inter`, `Roboto`, `Lucide`, `shadcn`
- `box-shadow` larger than `0 1px 0` (no floating cards)
- animation / `@keyframes` unless `prefers-reduced-motion: reduce` disables them

Allowed to remain:

- Leaflet OSM tiles
- `hls.min.js` vendored
- Seven tab `data-tab` values
- Footer DESIGN TARGET sentence
- “Analyse this still”, “Enroll Missing/Wanted Person”
