# U04 — Alerts (three-foot)

AGENT. Depends on U02.

## Goal

A queue a duty officer acks in one click. CRITICAL is a word, not a gold box.

## Agent

1. Render a table or a list with columns: PRI, entity, camera, count, Ack.
2. CRITICAL: `--critical` left bar + the letters CRITICAL in the PRI column (ink if red fails 4.5:1).
3. Person: show `entity_id` / name, not a blank plate.
4. Intrusion: `INTRUSION @ camera_id`.
5. `pending_review` visible as that word. Ack still posted.
6. Fetch open + pending_review (already in `app.js`).
7. Tick U04-001.

## Do not

Toast spam. Auto-ack. Hide pending_review.
