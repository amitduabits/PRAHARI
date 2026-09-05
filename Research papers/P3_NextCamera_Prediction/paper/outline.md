# P3 outline — ~8 pages (IJCAI) or journal length

| § | Section | Words | Must establish |
|---|---|---|---|
| 1 | Introduction | 800 | **Makris 2004, Tieu 2005 and Gambs 2012 named in the first paragraph** as what we reproduce. State the question as "when does counting suffice", not "we propose counting". |
| 2 | Problem: prospective next-camera ranking | 600 | Formalise the task, the temporal split, and the metrics. Releasing this protocol is part of the contribution. |
| 3 | Method | 500 | Short, because it is not new. Transition table, normalisation, top-k, great-circle cold start. One page maximum. |
| 4 | A measure of deployment irregularity | 700 | The quantitative axis the characterisation is stated over: deviation of camera adjacency from road-network adjacency, or transition-matrix entropy. **Without this there is no characterisation.** |
| 5 | Experimental setup | 700 | VeRi-776 and CityFlow. State plainly that DukeMTMC was declined and why. Six baseline tiers. |
| 6 | Results | 1800 | Accuracy by regime; the popularity-prior comparison; the coverage sweep and its cliff; the entropy ceiling; cold-start ablation; runtime. |
| 7 | Where it collapses | 600 | The negative half of the characterisation. If there is no regime where we lose, the experiment is not hard enough. |
| 8 | Related work | 700 | Two literatures, both of which own the estimator. Concede cleanly. |
| 9 | Limitations and misuse | 500 | `lum2016predict`, `ensign2018runaway`: transition frequencies learned from where cameras happen to be reproduce the deployment's existing biases. `pereira2022banal` on function creep. This is not boilerplate for this paper. |
| 10 | Conclusion | 200 | |

**Figures.** F1 accuracy vs irregularity, all methods — the central figure.
F2 accuracy vs ALPR coverage rate with the cliff. F3 accuracy vs history depth.
F4 normalised predictability against the entropy ceiling.
