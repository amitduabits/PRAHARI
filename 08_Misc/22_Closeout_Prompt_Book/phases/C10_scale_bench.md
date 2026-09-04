# C10 — Scale bench (MEASURED laptop vs DESIGN TARGET 80k)

Prepend `00_MASTER_CONTEXT.md`. AGENT.

## Goal

Official Step 6 “participants should explain” becomes numbers with labels, not adjectives.

## Agent

1. Implement E-S1..E-S6 in `scripts/run_experiments.py --suite scale`.
   - E-S1: open 1 then 2 then 4 file-sessions on CAM-OWN-001 for 20 s each if the mp4 exists; record time, errors, rejected fifth session.
   - E-S2: mean bytes of JPEGs in data/crops or experiment stills.
   - E-S3: DESIGN TARGET bandwidth = 45000 * mean_crop_bytes * 1 / 1e9 GB/s. Write the formula.
   - E-S4: DESIGN TARGET 7-day crop storage = mean_crop_bytes * 45000 * 86400 * 7.
   - E-S5: 50 sequential GET /api/health timings.
   - E-S6: torch.cuda.is_available() or “no torch”; GPU count MEASURED.

2. Write `05_Output/experiments/SCALE_BENCH.md` with a table: concern | MEASURED | DESIGN TARGET | HLD section.

3. If MEASURED mean crop bytes differs from HLD’s 80 KB by more than 2×, add one sentence to HLD §5: “PoC mean crop MEASURED {n} bytes on {date}; statewide 80 KB remains DESIGN TARGET.”

4. Do not install Kubernetes, Prometheus, or Ceph. Name them as statewide DESIGN TARGET only, already in HLD §10.

## Done when

- SCALE_BENCH.md exists.
- Fifth session still rejected (existing behaviour).
- CSV C10-* DONE.

## Do not

Call laptop throughput “80,000 cameras”. Invent GPU counts.
