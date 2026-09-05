# P6 outline — ~12 pages (IEEE TETC)

| § | Section | Words | Must establish |
|---|---|---|---|
| 1 | Introduction | 900 | The design tension: integration cost against liveness fidelity. State the falsifiable position and the crossover claim in the first column. |
| 2 | Setting | 700 | Multi-authority CCTV estates in India; why contributors will not operate a connector; `praharaj2020iccc` for the deployment context. |
| 3 | Related work | 1200 | **Franklin, Wiederhold, Lenzerini and NGSI-LD named by page 3.** Concede the pattern explicitly, then state the reconciliation gap. |
| 4 | Architecture | 1400 | Four layers, three invariants, and what each invariant buys. Written so the design is describable without our deployment. |
| 5 | The reconciliation loop | 900 | The sweep as the price of deferred integration: coverage interval, staleness bound, and the coupling to the ingest budget (cross-reference P4). **This is the novel component.** |
| 6 | Onboarding cost | 1200 | Three internal modes plus at least one external baseline. Distributions, not means. The honest 8x, and why the form tail dominates. |
| 7 | Transport reality | 1400 | The measured mix and, more importantly, the **failure** distribution: ONVIF conformance vs actual negotiation, the file-drop tail, unresolvable rows. |
| 8 | Scale | 900 | The knee: what fails at 8,000, what changed for 80,000, audit growth against retention. |
| 9 | Invariant violation | 700 | Drop each invariant, report what breaks. |
| 10 | Governance and ethics | 800 | Subscriber scoping, provenance-derived access, tamper-evident audit as the oversight artefact, retention derived from §8. `fussey2021assisted` on where discretion actually sits. Concede that our log is evidentiary, not provable (`haeberlen2007peerreview`). |
| 11 | Limitations | 500 | One deployment; modelled transport mix until §7 is measured; no external baseline until §6 is done; the pattern is not new. |
| 12 | Conclusion | 200 | |

**Figures.** F1 the four layers with the reconciliation loop drawn as the feedback
edge. **F2 onboarding cost per camera, all modes including the external baseline,
with the crossover marked — the falsifiable claim made visual.** F3 the transport
failure distribution, a stacked bar by authority. F4 coverage interval against
registry size, with the knee. F5 audit growth against retention policy.
