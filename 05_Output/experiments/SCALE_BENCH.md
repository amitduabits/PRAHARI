# Scale bench (C10)

**Date.** 2026-09-04. Laptop PoC. Every statewide figure is DESIGN TARGET.

| Concern | MEASURED (this laptop) | DESIGN TARGET (statewide) | HLD |
|---|---|---|---|
| Open captures | 1/2/4 file sessions on `own_feed.mp4` succeeded; fifth rejected | Regional worker is the scale unit; SOC wall 16–64 HLS tiles | §10 |
| Mean JPEG crop | 41 288 bytes (8 own-feed stills) | 80 KB used in bandwidth arithmetic | §5 |
| Analytics bandwidth | — | `45_000 × mean_bytes × 1 fps` → 3.6 GB/s naive at 80 KB; 1.86 GB/s if 41 KB holds | §5 |
| 7-day crop store | — | 45k cameras × crop × 86400 × 7 | §5 hot |
| `/api/health` | p50 2.6 ms, p99 9.4 ms (50 sequential calls) | Prometheus, camera-health SLO 99% | §10 |
| GPU count | 0 | 5 regional GPU nodes (8×L40S class) | §10 / §12 |
| HA / DR | none | active-active API, RPO 15 min metadata, RTO 1 h | §10 |

PoC mean crop MEASURED 41 KB on 04 Sep 2026 from `own_feed.mp4` stills. Statewide 80 KB remains DESIGN TARGET (ratio 1.9×, under the 2× rewrite trigger).

GPU count MEASURED 0. Regional accelerators stay DESIGN TARGET. Do not present laptop throughput as 80,000 cameras.
