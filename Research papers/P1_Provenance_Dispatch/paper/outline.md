# P1 outline — target ~9 pages + references

| § | Section | Words | Must establish |
|---|---|---|---|
| 1 | Introduction | 900 | That invocation and release are different harms, with the naive-union example in the first column. Contribution list of three, one of which is the measurement. |
| 2 | Background and threat model | 700 | Who the adversary is: a curious or compromised operator of the analytics stack, not the cloud provider (that is Visor) and not the query analyst (that is Privid). State what the model does *not* protect against. |
| 3 | Related work | 1100 | **Written first.** Capsicum, XEngine, Ancile, WDAC and Privid all named by page 3. Concede the combinational nature explicitly, then say what is left. |
| 4 | Provenance-gated dispatch | 1200 | Attribute schema; deny rules and why they compose by intersection so order does not matter; registration-time compilation; the O(1) dispatch; lazy construction and its precondition. |
| 5 | Properties | 700 | P1 dispatch is O(1) in policy size. P2 an engine's weights are never materialised unless some registered camera permits it. Short proofs; state the atomicity and re-registration assumptions. |
| 6 | Implementation | 600 | The deployed system, honestly: which parts are in `app/services/analyse.py` today and which are the research prototype. |
| 7 | Evaluation | 1800 | E1.1-E1.4 plus the leakage experiment. Lead with exposure, not latency — latency is the least interesting result and the most obviously anticipated by XEngine. |
| 8 | Discussion and limitations | 700 | Shared backbones; re-registration; no formal statement about what a permitted model leaks; the combinational novelty; synthetic policy cardinality. |
| 9 | Ethics | 300 | Deployment context is police surveillance. Say so. Say what the mechanism does and does not constrain. |
| 10 | Conclusion | 200 | |

**Figures.** F1 architecture (registration vs dispatch path, one diagram).
F2 dispatch latency vs policy size (have it). F3 forbidden invocations by method,
bar chart (the paper's central figure). F4 resident weight bytes with and without
a permitted camera.

**Table.** T1 the four-property matrix from `literature/matrix.md`, in the related
work section, not the appendix.
