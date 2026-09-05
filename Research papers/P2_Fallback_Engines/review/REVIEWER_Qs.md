# P2 anticipated reviewer questions

**Q1. Is this not NoScope's cascade with a different name?**
Partly yes. NoScope's cheap stages are filters, not answer producers, and are tuned
against a labelled reference model. Concede the cascade, claim only the provenance
plumbing. — *answerable now.*

**Q2. Is this not the Simplex architecture?**
Yes, architecturally. Learned primary, classical secondary, shared interface,
explicit switch. Say it in the introduction. — *answerable now.*

**Q3. Why not just fit ATC per stratum?**
**Not answerable.** This is the experiment that decides the paper. Run it.

**Q4. Average Confidence is unbiased under calibration. Why would stratification
help?**
It does not, for batch accuracy — that is our finding, and the theorem is
`kivimaki2025confidence`. It helps for per-path estimates, which are conditional
quantities the theorem says nothing about. — *answerable now, and this is the
strongest thing in the paper.*

**Q5. Mandoline already does slice-conditioned estimation.**
Correct. With the provenance field as a slicing function, our estimator is a
special case. Run Mandoline as a baseline and position accordingly.

**Q6. Your engines are simulated.**
Correct. This is the single largest weakness. Either run real YOLO/FaceNet/PaddleOCR
or restrict every accuracy claim to the simulation and say so in the abstract.

**Q7. Deep inference can be made deterministic. Why is your reproducibility claim
interesting?**
Only because of the throughput cost, which we do not currently measure. Measure it
or drop the claim.

**Q8. Retry beats your fallback on accuracy. Why use a fallback?**
Bounded latency and determinism, not accuracy. State it in the results section
where the losing row appears, not in a footnote.

**Q9. Where are the confidence intervals on the estimate?**
Not present. Add them, via the JAIR method or conformal risk control.
