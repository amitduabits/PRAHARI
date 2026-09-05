# Real-data instrumentation outputs (P1 + P4)

Produced by `02_Code/prahari/scripts/instrument.py` from `PRAHARI_PROMPTBOOK.md`.

| File | Prompt |
|---|---|
| `prahari_real_registry.json` | P1-A census |
| `real_detections_raw.jsonl` | P1-A events (no raw video) |
| `p1_invocation_measurements.json` | P1-B CONFIG A vs B |
| `p1_audit_trail.csv` | P1-C |
| `p4_resource_log.jsonl` | P4-A |
| `p4_frontier.json` | P4-B |
| `p4_retrial_analysis.md` | P4-C |

Every numeric field is **MEASURED** on this laptop unless a note says DESIGN TARGET. A 24-hour live RTSP capture is `python scripts/instrument.py p1-a --hours 24` with `SENTINEL_HOST` set. The default smoke replays `own_feed.mp4` under the seeded registry so Gov vs Own invocation is comparable on the same pixels.
