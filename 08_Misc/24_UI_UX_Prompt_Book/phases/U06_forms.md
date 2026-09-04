# U06 — Watchlist, Onboard, Gaps

AGENT. Depends on U02.

## Goal

Visible labels. Analyse/ANPR results as cards. FRS hint stays.

## Agent

1. Every form control: `<label for="...">` visible. Placeholders are examples only.
2. Onboard: Analyse this still heading **unchanged**. Hint: Own faces only; government cameras never run FRS.
3. Replace primary `<pre id="analyse-out">` with a `.result-card` listing entity_type, plate/face_id/object_class, source, confidence. Keep a collapsible raw JSON if useful.
4. Confirm plate / Confirm face remain separate. Do not style confirm as ANPR.
5. Enroll Missing/Wanted Person heading stays (T-V10).
6. Gaps: object CSV link + a small table of counts, not only `<pre>`.
7. Tick U06-001.

## Do not

Drop Analyse this still. Eighth tab. NLP labelling on query.
