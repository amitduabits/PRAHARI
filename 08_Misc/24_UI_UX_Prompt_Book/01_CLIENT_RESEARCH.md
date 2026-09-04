# Client research — who this UI is for

PRAHARI is not a SaaS landing page. The people who will click it in the next 72 hours are not designers. They are a screening committee, then (if shortlisted) a control-room operator and a supervising officer.

## 1. Three users, three jobs

| User | Time with the UI | Job to be done | Failure mode |
|---|---|---|---|
| Screening judge (laptop, 3 min video + optional login) | 90–180 s on camera, maybe 5 min live | See a **working duty desk**, not a student template | Looks generated → discounts the whole packet |
| SOC operator (`judge` / `soc_operator`) | Shift-length in a real PoC | Open a camera, match a plate, ack a CRITICAL, download CSV | Extra chrome, tiny type, mouse-only ack |
| Department viewer (`home.viewer`) | Minutes | See **Home** cameras only | Mall camera visible; unexplained 403 |

Design for the operator. The judge will then believe it. Do not design for Dribbble.

## 2. What they already sit in front of

Home Department and district control rooms in Gujarat already know:

- **VMS consoles** (Milestone, Genetec, HikCentral, vendor NVRs): dense tables, camera IDs as the primary string, small status dots, almost no marketing copy, dark or mid-gray, sharp corners.
- **112 / ERSS / PCR**: khaki vehicles, “Call 112”, map + incident list. Not gold-on-navy cards.
- **eGujCop / CCTNS-class forms**: labelled fields, Windows-era density, Gujarati + English. Placeholders-as-labels feel like a toy.
- **Gujarat Police identity** (emblem 2019): navy shield, Ashoka chakra, yellow wordmark. Uniform is **khaki**, not gold foil. Do not paste the full emblem as a hero. Do not use the tricolour as a UI theme.

Reference products to **steal density from**, not pixels:

| Product | Steal | Do not steal |
|---|---|---|
| Genetec Security Center | Camera-first wall, alarm list with severity leftmost | Vendor chrome |
| Milestone XProtect | Live/playback split, bookmark on the timeline | License banners |
| BriefCam | Review list with crop + timestamp | Marketing orange splash |
| Indian Railways / AAI ops walls | Shared map + exception list | Clipart |

## 3. Control-room evidence (external)

- **Three-foot vs ten-foot** (Activu / SOC wall practice): the video wall and Gujarat map must read from ~3 m (large type, 3 colours). The alert queue and tables must read at ~0.7 m (13–14 px, tabular numbers, 32–36 px rows).
- **RCMP GCPSG-003**: colours and icons follow org standards; displays match the geography being watched; red is for incidents, not decoration.
- **Datapath / command-centre 2026**: the software must not add cognitive load while an incident is live. Every extra menu is a second not spent on response.
- **ISO 11064** (control-centre ergonomics, used as a check not a certificate): information grouped by task; alarms distinguishable by more than hue (shape + word + position).

## 4. Jury constraints that are also UX constraints

The 3-minute own-feed and gov-feed videos **are** the UX test the committee will apply.

| Demo beat | UI must make it one glance |
|---|---|
| Hybrid one-liner | Header status, not a tracked kicker |
| Reconstruct `GJ01AB1234` | Track tab or a persistent plate field |
| CRITICAL stolen | Alert row: priority word + plate + camera + Ack |
| Analyse this still | Onboard: labelled file input, camera id, result as a card not a JSON dump |
| cam04 from the **table** | Cameras table: Open is the last column, caption about no GIS |
| No FRS on Paldi | Hint stays. Analyse on Gov does not offer a face card |
| DESIGN TARGET 80k | Footer, 12 px, still contains the words DESIGN TARGET and 80,000 |

If a restyle hides “Analyse this still” or the footer, `test_tabs_smoke.py` and `test_honesty.py` fail. That is a product bug, not a visual win.

## 5. Jobs and click budgets (quantified)

These are the bars in `04_QUANTIFIED_BAR.md`.

| Job | Maximum clicks from login | Maximum visible wait |
|---|---|---|
| See Gujarat map + health pins | 0 (Operations is default) | Map tiles < 2 s on LAN |
| Open fourth live tile | 2 per camera (row → Open) | Fifth tile shows a **visible** 429, not a silent fail |
| Reconstruct `GJ01AB1234` | 2 (tab + Reconstruct; `/` focuses plate) | Table + polyline < 1 s (seeded) |
| Ack a CRITICAL | 1 on the alert row | WS toast or row update < 1 s |
| Download track CSV | 1 (link next to Reconstruct) | Browser download |
| Confirm a plate | 2 (Onboard fields already filled for demo) | Alert appears without refresh |
| Open cam04 with no GIS | 2 (Cameras tab → Open on that row) | Tile or honest empty |

If a restyle adds a click to any of these, revert that part.

## 6. What “AI generated” means to this client

They will not say “shadcn smell”. They will say **“this looks like a student ChatGPT demo.”** The tells in our tree today:

- Navy `#0b1220` + gold `#d4a017` + mint `#3dd68c` (crypto-dashboard default)
- `.kicker { text-transform: uppercase; letter-spacing: 0.08em }`
- `h1 { letter-spacing: 0.12em }`
- `"Segoe UI", system-ui` only
- Hybrid manifesto as a subtitle instead of a status chip
- Forms that use placeholders as labels (`source_case_id`, `entity_type`)
- `<pre>` dumps for ANPR / analyse / gaps / predict
- Identical 1 px `#243044` border on every box
- Login card floating in a void at `12vh`

A duty desk does not letter-space its title. A duty desk labels its fields. A duty desk shows CRITICAL as a word in a list, not as a gold tab.
