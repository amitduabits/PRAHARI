# Design direction (locked)

**Name.** Duty desk.  
**One sentence.** A Gujarat Police workstation for a 3-minute demo and an 8-hour shift: khaki-ink on paper-dark olive, not gold-on-navy SaaS.

If an agent wants a second aesthetic, stop. Two aesthetics is how slop returns.

## 1. What it is

A **mid-dark industrial console**. Think a radio room that also has a map: olive-black field, paper-coloured type, one navy strip for the agency header, **red only on CRITICAL**. Khaki appears as a 3 px rank bar on the header, not as a background.

## 2. What it is not

- Linear / Vercel / “SOC startup” navy + gold
- Cream + rust “Claude Design” slides
- Purple glass cards
- Tricolour chrome
- A marketing site with a kicker and a manifesto subtitle
- A new SPA. Stay vanilla JS + Leaflet. No npm UI kit.

## 3. Locked tokens

Put these in `:root` in `styles.css`. Do not add more hues without a new token name.

```css
:root {
  --ink: #e6e4d8;          /* primary text */
  --muted: #b4b19a;        /* secondary text; WCAG ≥ 4.5:1 on --field */
  --field: #16180f;        /* page background, olive-black */
  --panel: #1f2218;        /* tables, header, wall chrome */
  --line: #3a3d32;         /* 1 px rules only */
  --navy: #1e2a4a;         /* 48 px header bar only */
  --khaki: #a38b4d;        /* 3 px header rank stripe + focus ring */
  --critical: #d6453d;     /* CRITICAL alerts and errors only */
  --high: #d4a017;         /* HIGH only — not brand gold */
  --live: #3f8f5b;         /* health live */
  --offline: #8a4038;      /* health offline */
  --warn: #c4a35a;         /* degraded */
  --mono: "IBM Plex Mono", "Consolas", ui-monospace, monospace;
  --sans: "IBM Plex Sans", "Noto Sans", "Segoe UI", sans-serif;
  --fs: 13px;
  --row: 34px;
  --focus: 2px solid var(--khaki);
}
```

**Type.** Load IBM Plex Sans + IBM Plex Mono from a **vendored** `app/static/fonts/` or a single Google Fonts link with `display=swap`. If offline demo is a risk, vendor the woff2 files (same rule as `hls.min.js`). Do not use Inter, Roboto, Space Grotesk, or letter-spaced all-caps.

**Wordmark.** Header left: `PRAHARI` at 18 px / 600, tracking 0. Department line under it: `Home Department · SOC` at 12 px `--muted`. No uppercase kicker.

**Hybrid story.** One status chip in the header: `Hybrid 1+2+thin 3`. Not a subtitle paragraph.

## 4. Layout (1280×720 minimum, the video frame)

```
[ 48 px navy header | wordmark | role | health chips | clock ]
[ 36 px tab strip — 7 tabs, selected = ink on panel, 3 px khaki underline ]
[ main: 12 px padding ]
[ footer 28 px: DESIGN TARGET sentence · WS state ]
```

Operations (default):

```
[ map 58% minmax 0 ] [ wall 42% ]
wall: 2×2 tiles, each tile: id + close, video fill, 4:3 or 16:9 object-fit contain
```

Alerts:

```
list, not cards. Columns: PRI | entity | camera | age | count | Ack
CRITICAL rows: left 4 px --critical, priority word in --critical
pending_review: the word visible, Ack still works
```

## 5. Colour law

| Meaning | Token | Also encoded as |
|---|---|---|
| CRITICAL | `--critical` + the word CRITICAL | leftmost column, not colour alone |
| HIGH | `--high` + HIGH | |
| live camera | `--live` 8 px dot | plus the word live in the table |
| offline | `--offline` dot | plus the word |
| brand / selected tab | khaki underline, not a filled gold pill | |

Red is not used for “Sign in”, links, or the page background.

## 6. Copy law (UX writing)

- Buttons: Reconstruct, Open, Ack, Confirm plate, Confirm face, Analyse still, Save, Enroll. Verbs. Not “Submit”, not “Sign in” → use **Log in** (duty desk).
- Field labels visible above the control: Camera ID, Plate, Gallery ID. Placeholders are examples (`GJ01AB1234`), never the only label.
- Results: a two-column definition list or a small table: Plate / Confidence / Source / Camera. Source `operator_confirm` must be readable as **Operator confirm**. Never restyle it as ANPR.
- Empty: one sentence + one action. “No open alerts.” “Live catalogue has no coordinates. Open cam04 from this table.”
- Login hint: “Judge password is JUDGE_PASSWORD in the local environment.” Do not print `.env` as the first line.

## 7. Motion

None, except Leaflet pan/zoom. If a toast is added for CRITICAL, it is a 200 ms opacity fade, disabled under `prefers-reduced-motion: reduce`.

## 8. Breakpoints

| Width | Behaviour |
|---|---|
| ≥ 1280 | Operations split 58/42. Video frame. |
| 900–1279 | Split 1fr / 1fr |
| < 900 | Stack map then wall. Tabs wrap. **Jury video is 1280.** Do not optimise mobile at the cost of 1280. |
