# Quantified pass bar

An implementation is **done** only when these numbers pass. Subjective “looks nicer” is not done.

## 1. Visual (grep + computed style)

| Metric | Pass | Fail |
|---|---|---|
| Colour tokens in `:root` | ≤ 12 custom properties for colour | Extra gold/navy/mint leftovers |
| `#d4a017` used as page accent / tab fill | 0 hits except HIGH priority token `--high` | Gold tabs, gold h1, gold buttons |
| `letter-spacing` on `h1`, `.kicker`, `header` | ≤ `0.02em` | 0.08em / 0.12em tracking |
| `text-transform: uppercase` on chrome | 0 | `.kicker` |
| Primary font | IBM Plex Sans (or Noto Sans) listed **before** Segoe | Segoe-only stack |
| Body size | 13 px or 14 px | 16 px luxury / 11 px unreadable |
| Table row height | 32–36 px | card-like 56 px+ |
| Box radius | ≤ 2 px | 12 px pills |
| `box-shadow` | none or `0 1px 0` | floating cards |
| Tab selected | 3 px khaki **underline**, not filled gold pill | `.tab.on` gold fill |

## 2. Contrast (WCAG 2.2 AA + dark-UI sanity)

Compute with relative luminance `(L1+0.05)/(L2+0.05)`.

| Pair | Minimum |
|---|---|
| `--ink` on `--field` | 7:1 (shift work, ten-foot) |
| `--ink` on `--panel` | 7:1 |
| `--muted` on `--field` | 4.5:1 |
| `--critical` on `--panel` | 3:1 for the bar; the **word** CRITICAL uses `--ink` if the red fails 4.5:1 |
| Focus ring `--khaki` on `--field` | 3:1 (1.4.11) |
| Log in button text on its fill | 4.5:1 |

Also report APCA Lc if a checker is available: body text **|Lc| ≥ 75** on `--field`. WCAG 2 overstates dark-mode contrast; if muted fails the eye test, darken `--muted` even when 4.5:1 already passes.

Script: `tests/test_ux_contrast.py` reads the `:root` block, parses hex, asserts the table. No browser required.

## 3. Accessibility

| Metric | Pass |
|---|---|
| Visible `:focus-visible` | ≥ 2 px solid, not `outline: none` |
| Tab buttons | `role="tab"` + `aria-selected="true|false"` |
| Tab panels | `role="tabpanel"` + `aria-labelledby` |
| Every input | `<label for>` or wrapping `<label>` |
| Images / map | map container `aria-label="Gujarat camera map"` |
| Keyboard | Tab order = header → tabs → main. `/` still focuses plate. Enter on Reconstruct works |
| Reduced motion | no required animation |
| Login error | `role="alert"` |

## 4. Task times (manual, 1280×720, judge user, seeded db)

Stopwatch. Three trials. Report median.

| Task | Pass median | How to measure |
|---|---|---|
| Login → map pins visible | ≤ 8 s | from Log in click |
| Reconstruct GJ01AB1234 | ≤ 6 s including tab change | count ≥ 6 in meta |
| Ack first CRITICAL | ≤ 3 s from Alerts tab | row gone or acked |
| Open CAM-OWN-001 tile | ≤ 8 s | video element playing or honest empty |
| Analyse still round-trip | ≤ 15 s after file chosen | card with entity_type, not a crash |
| Download CSV | 1 click from Track | browser starts download |

If a restyle exceeds these, the chrome is too heavy.

## 5. Demo-script compatibility (automated)

`GET /` HTML must still contain, case-insensitive:

- `analyse this still`
- `DESIGN TARGET`
- `80,000` or `80000`
- `Enroll`
- `Reconstruct`
- `operator confirm` or `Confirm plate`
- seven `data-tab` values: operations, cameras, track, alerts, watchlist, onboard, gaps

Must **not** contain: `lorem`, `todo`, `tbd`, `rtsp://`.

Existing tests stay green: `test_tabs_smoke.py`, `test_honesty.py`, `test_enroll_ui.py`, `test_no_rtsp_leak.py`.

## 6. Anti-slop automated tests (new)

`tests/test_ux_duty_desk.py`:

1. `styles.css` has `--field` and `--khaki`.
2. `styles.css` does not set `h1 { letter-spacing` above 0.02em (regex).
3. No `.kicker` class, or kicker has `text-transform: none` and tracking ≤ 0.02em.
4. `index.html` has `<label` count ≥ 12 (login + onboard + watchlist + confirm).
5. `index.html` primary analyse result is not the only child of a raw `<pre id="analyse-out">` used as layout — wrap in `.result-card` (pre may remain as detail).
6. Tab selected style is not `background: var(--accent)` gold fill.
7. `IBM Plex` or `Noto Sans` appears in the font stack.

## 7. Audit score

Re-run the table in `02_CURRENT_AUDIT.md`. **Pass ≥ 40 / 48.** Publish the new scores in the U07 log.

## 8. What we will not measure (out of scope)

- Gujarati localisation (Phase-2)
- Custom Gujarat basemap tiles (OSM stays)
- 60 fps wall, WebRTC
- Mobile-first layout
- User testing with 12 operators (no time). The 3-minute video **is** the test.
