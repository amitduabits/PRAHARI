# P4 literature matrix

## Part 1 — the admission policy

| Work | Bound is a fixed cardinality | No queue | No eviction | No quality reduction | Bound derived from an SLO | Priority classes |
|---|---|---|---|---|---|---|
| **This work** | yes | yes | yes | yes | **no — asserted** | no |
| erlang1917 | yes | yes | yes | yes | n/a (analysis, not a system) | no |
| jamin1995mbac | no — measured load | yes | yes | yes | yes | no |
| vin1994statistical | no — statistical capacity | yes | yes | yes | yes | no |
| welsh2001seda | no | **no — bounded queue** | yes | yes | partly | no |
| welsh2003adaptive | no | no | yes | **no — degrades** | yes | no |
| klein2014brownout | no | no | yes | **no — dims content** | yes | no |
| zhou2018wechat (DAGOR) | no — dynamic | no | yes | yes | yes | **yes** |
| cho2020breakwater | no — credit-based | no | yes | yes | yes | partly |
| shen2019nexus | derived | no | yes | yes | **yes** | yes |
| gujarati2020clockwork | n/a | yes — drops predicted misses | yes | yes | **yes** | no |
| abeni1998cbs | per-task reservation | yes | yes | yes | yes | yes |
| vestal2007mixed | n/a | n/a | drops by criticality | n/a | yes | **yes** |

The row that should worry us: **erlang1917 matches on all four policy columns.**
The columns where we are *worse* than the field: no SLO derivation, no priority
classes. Both are things reviewers will ask us to justify, and "determinism" is
the only available answer.

## Part 2 — the health sweep

| Work | Round-robin at bounded rate | Multi-strike hysteresis | Adaptive threshold | Probe budget shared with the data path | Coverage interval bounded analytically |
|---|---|---|---|---|---|
| **This work** | yes | yes (three strikes) | no | **yes — this is the novel column** | yes |
| das2002swim | yes | yes (suspicion) | no | no | yes (protocol period) |
| hayashibara2004phi | n/a | continuous suspicion | **yes** | no | no |
| chandra1996unreliable | n/a | formalised properties | n/a | no | n/a |
| guo2015pingmesh | yes | no | no | no | yes |
| durumeric2013zmap | yes | no (stateless) | no | no | yes |

One column is ours. That column, crossed with Part 1, is the paper.

## The gap, in one sentence

*No published system draws its reachability-probe concurrency from the same bound
as its data-path concurrency, so the trade-off between blocking probability and
health-staleness has never been stated, let alone characterised.*

## Reading order

1. `erlang1917` and `sevastyanov1957` — the policy and the theorem that makes it rigorous for real session distributions.
2. `das2002swim` — in full. The health half is this paper unless the coupling carries it.
3. `gujarati2020clockwork` — the strongest "determinism by construction, refuse the rest" system.
4. `zhou2018wechat`, `cho2020breakwater` — the dynamic controllers we are strictly weaker than.
5. `bossen2012hevc` — the evidence that a decoder session is not a unit of cost.
6. `kelly1991loss` — the multi-resource generalisation we do not solve.
