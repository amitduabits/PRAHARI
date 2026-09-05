# P2 outline — workshop paper, ~6 pages

Reframed as a negative result plus a systems note. Do not write the ICCV version.

| § | Section | Words | Must establish |
|---|---|---|---|
| 1 | Introduction | 600 | The operator's question: "how accurate is today's output?" with no labels and two engines. State the negative result in the abstract. |
| 2 | Setting | 400 | The two-tier pipeline as deployed; the nine-field record; what provenance is recorded. |
| 3 | Why the obvious estimator wins | 700 | Average Confidence is unbiased under calibration (`kivimaki2025confidence`). Derive why stratification cannot beat it on batch accuracy. **This is the paper's spine.** |
| 4 | What stratification does buy | 800 | Per-path accuracy: the number the operator actually needs, and which no unstratified estimator expresses. Per-stratum calibration error. |
| 5 | Baselines | 700 | AC, global ATC, per-stratum ATC, DoC, COT, Mandoline-with-provenance-slices. If per-stratum ATC ties, say so in this section, not the appendix. |
| 6 | Related work | 600 | NoScope, Neural Simplex, Mandoline, ATC. Concede the architecture is anticipated. |
| 7 | Limitations | 400 | Behavioural engine models; injected failure rates; determinism claim is about cost not capability. |
| 8 | Conclusion | 200 | |

**Figures.** F1 the two-tier pipeline with the record schema. F2 estimation error
by method, batch vs per-path — the central figure, and it should show us losing on
one and winning on the other.

**If per-stratum ATC ties on the per-path metric**, delete sections 3-5, keep the
systems description, and submit it as an experience report. That is a legitimate
outcome and should be decided before drafting, not during.
