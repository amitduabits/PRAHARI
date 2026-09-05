# P1 anticipated reviewer questions

Each must be answerable in writing before submission. "We assert" is not an answer.

**Q1. Is this not Capsicum applied to model registries?**
Yes, in enforcement discipline. Say it first, in the related work section. The
delta is that the capability is derived from device provenance rather than granted
by the process itself, and that the measurement of exposure has no Capsicum
analogue. — *answerable now.*

**Q2. XEngine already compiles policy. What is new about O(1) dispatch?**
Nothing, on its own. XEngine makes the check cheap; we make it absent. The claim
must be phrased as "the compiled artefact is consumed at object-construction time",
not "policy evaluation is fast". — *answerable now.*

**Q3. A permitted person-detector can be probed for identity. What does your
guarantee actually buy?**
**Not answerable.** This is C5 in `experiments/EXPERIMENTS.md` and it is not run.
Either run it or scope the claim to "the facial model's own representation never
exists", which is weaker and must be stated as such.

**Q4. Privid gives a differential-privacy guarantee. You give an architectural one.
Why is yours better?**
It is not better, it is different: Privid bounds what an analyst learns from
released output; we prevent a class of computation from occurring. Under our threat
model Privid offers nothing, and under Privid's threat model we offer nothing.
State both directions. — *answerable now.*

**Q5. What happens when a camera's provenance changes?**
**Not answerable.** Re-registration semantics are unspecified. Specify them.

**Q6. Do the engines share a backbone? If so the forbidden model is partly built.**
**Not answerable on the production stack.** Audit `app/engines/` and report.

**Q7. Your exposure numbers come from a simulation of engines, not the engines.**
Correct as of today. Instrument `analyse.py` before submission.

**Q8. Your policy has six rules; you swept to 192 by padding with inert rules.**
Correct. Report the real policy cardinality and say the sweep is a stress test of
the dispatcher, not a claim about real policy sizes.

**Q9. Is the estate-size independence claim not trivially true?**
Yes. It is a property of the design, not a finding. Present it as an invariant.

**Q10. Ethics: this is a police surveillance system.**
Answer directly. The mechanism narrows what may run on which camera; it does not
constrain what the permitted analytics are used for, and it is not a substitute for
oversight. Cite `fussey2021assisted` (in P6's bibliography) on where discretion
actually sits.
