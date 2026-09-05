# P5 outline — ~10 pages (IEEE TCSVT), reframed

| § | Section | Words | Must establish |
|---|---|---|---|
| 1 | Introduction | 800 | The question is how long a presence is, not what schema to use. State the negative result about the geometric derivation in the abstract. |
| 2 | Background | 700 | Normalised alert records (IDMEF, OCSF, JDL common referencing) and keyed session windows (Dataflow) as **established background, not contribution**. Say so in the first sentence of the section. |
| 3 | The collapse predicate as deployed | 600 | One entity-keyed predicate across ANPR, faces and region occupancy. Precise window semantics: anchored or merging. |
| 4 | Choosing W | 1400 | The four families: mixture crossover, spec-based timer design, Kneedle, cost-weighted ROC. **Lead with the ROC framing** so the value judgement is explicit and other deployments can pick a different point. |
| 5 | Why the geometric derivation fails | 800 | FOV/speed gives 1.3-9.6 s; the measured knee is 15-30 s; 120 s masks 3.2% of distinct incidents for 1.4% more suppression. Report the discrepancy plainly. |
| 6 | Evaluation | 1800 | The operating curve with both failure modes; per-camera fitted W and its distribution; global-W ablation with its recall cost; baselines including Valdes-Skinner weighted similarity; operator-burden numbers. |
| 7 | Related work | 700 | Debar-Wespi, Valdes-Skinner, Dataflow, JDL, the process-control timer line. Concede the schema and the predicate cleanly. |
| 8 | Limitations | 500 | Synthetic-versus-real; window semantics; single-estate; the case-grouping alternative reading. |
| 9 | Conclusion | 200 | |

**Figures.** F1 the operating curve, duplicate suppression against incident
masking, with the deployed 120 s marked on the wrong side of the knee — **the
paper's central figure.** F2 the inter-observation-time distribution with the
fitted mixture and the crossover. F3 per-camera fitted W across the estate.
F4 geometric window vs fitted window, scatter, showing the order-of-magnitude gap.
