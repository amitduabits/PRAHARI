# P4 Retrial Queue Analysis

- Label: MEASURED
- UTC: 2026-09-05T06:28:29Z
- Total admit attempts: 6
- Initial refusals: 3 (50.0%)
- Successful retries: 3 (100.0% of refusals)
- Mean retry latency: 2.980 ms
- P99 retry latency: 3.164 ms
- Abandoned requests: 0 (0.0% of refusals)
- Optimal K (this laptop): 1
- Product default K: 4
- **Conclusion:** System behavior matches a retrial queue (M/M/K/(K+R)), not Erlang-B loss. A refused open is retried after a capture slot is released; it is not a permanent fail.

Frontier points:
- K=1: p99=10.854 ms, cache_hit=100.0%, rss=0.0 MB, refusals=1, retries_ok=1
- K=2: p99=11.387 ms, cache_hit=100.0%, rss=0.0 MB, refusals=1, retries_ok=1
- K=4: p99=11.318 ms, cache_hit=100.0%, rss=0.0 MB, refusals=1, retries_ok=1

Reference: Erlang-B is M/M/K/K (loss). PRAHARI is M/M/K/(K+R) because probes retry from the app layer after MAX_OPEN_CAPTURES refuses an extra session.
