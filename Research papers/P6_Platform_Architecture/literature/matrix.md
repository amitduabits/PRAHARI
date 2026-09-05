# P6 literature matrix

Classified on the five dimensions the review proposes as the survey taxonomy.
Empty cells in this space are where contributions live.

| Work | Unit of contribution | Trust assumption | Reconciliation model | Transport negotiation | Accountability substrate |
|---|---|---|---|---|---|
| **This work** | **descriptor row** | none required of contributor | **bounded sweep** | negotiated per row | append-only |
| franklin2005dataspaces | descriptor | none | **none** | n/a | none |
| wiederhold1992mediators | source description | none | none | n/a | none |
| lenzerini2002dataintegration | source description (GAV/LAV) | none | none | n/a | none |
| cirillo2019fiware (NGSI-LD) | **registration + live broker** | contractual | poll | n/a | none |
| bader2020idsim (IDS) | connector + resource description | cryptographic | none | n/a | usage-control policy |
| braud2021gaiax | connector | contractual + cryptographic | none | n/a | policy |
| machado2022datamesh | **served data product** | organisational | none | n/a | governance policy |
| chadwick2009fim | identity provider | federated trust | none | n/a | audit |
| khochare2021anveshak | owned stream | single domain | n/a | fixed | none |
| jain2020spatula | owned stream | single domain | n/a | fixed | none |
| lu2016optasia | ingestible stream | single domain | n/a | fixed | none |
| zhang2017videostorm | ingestible stream | single domain | n/a | fixed | none |
| sanchez2014smartsantander | owned device | single owner | poll | fixed | none |
| rfc6962 (CT) | log entry | none | monitors + auditors | n/a | **verifiable** |
| haeberlen2007peerreview | node | Byzantine | witnesses | n/a | **provable** |
| crosby2009tamper | log entry | none | n/a | n/a | **tamper-evident** |

**The column that is ours is "reconciliation model = bounded sweep".** Every
descriptor-first row above has "none" there, because none of them describe physical
devices that can silently stop existing. Everything else in our row is taken.

Note also the accountability column: our append-only log is weaker than CT's
verifiable log and far weaker than PeerReview's provable one. Concede that rather
than let a reviewer find it.

## The gap, in one sentence

*Descriptor-first federation, long established for data, has never been
instantiated or evaluated for live physical sensor estates under multi-authority
ownership, where the descriptor must be continuously reconciled against a device
nobody in the federation operates.*

## Reading order

1. `franklin2005dataspaces` — in full, first. It is the most dangerous prior work.
2. `wiederhold1992mediators`, `lenzerini2002dataintegration` — the older ancestors.
3. `cirillo2019fiware` — NGSI-LD context source registration is functionally a registry row, and it is the external baseline we owe.
4. `tang2015config`, `verma2015borg` — for *how* to make this publishable.
5. `sanchez2017lessons` — the existing "operational cost at city scale" paper we must differentiate from.
6. `fussey2021assisted`, `kitchin2014realtime`, `praharaj2020iccc` — the ethics section, which at TETC is not optional.
