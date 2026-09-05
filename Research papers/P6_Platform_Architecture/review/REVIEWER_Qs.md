# P6 anticipated reviewer questions

**Q1. Is "registry rows instead of federation APIs" not pay-as-you-go dataspace
integration, published in 2005?**
Yes, as a pattern. Concede it in the introduction. The delta is that a camera row
describes a live physical device nobody in the federation operates, so the
descriptor must be continuously reconciled — and dataspaces have no such loop.
— *answerable now, if we lead with it.*

**Q2. NGSI-LD context source registration is a registry row. How are you different
from FIWARE?**
**Not answerable quantitatively.** FIWARE requires each domain to run a broker;
we claim that fixed per-authority cost is the difference. Without a measured cost
delta the distinction is implementation preference. Run the baseline.

**Q3. SmartSantander already reported operational cost at city scale.**
Single-owner municipal testbed, low-bandwidth sensors, no transport negotiation, no
cross-authority provenance, and retrospective narrative rather than a controlled
comparison. But they had more longitudinal data, and "what does your cost analysis
show that theirs did not" is fair. Answer it explicitly.

**Q4. Your onboarding comparison is a three-way A/B of your own UI.**
Correct as of today. That is exactly why the external baseline in Q2 decides
publishability.

**Q5. What is load-bearing about 80,000?**
**Not answerable.** Show what fails at 8,000 and what change made 80,000 possible.
Report the knee.

**Q6. Would this design survive without your deployment?**
State the three invariants and measure what breaks when each is dropped. Not yet done.

**Q7. Is your audit log adversarially sound?**
No. It is evidentiary, not provable. `haeberlen2007peerreview` and `rfc6962` are
stronger. Concede it and say why the weaker guarantee is the right cost for this
setting — or adopt the CT monitor/auditor split and say so.

**Q8. Ethics: this federates police surveillance across authorities. What changes
about who can act on an alert?**
Answer with mechanism: subscriber scoping by contributing authority, provenance-
derived access, retention from the measured log growth. Cite `fussey2021assisted`
on discretion migrating to whoever sees the alert. Do not answer with a citation to
Kitchin alone.

**Q9. Why is this not an ACM Computing Surveys paper?**
It is not a survey. CSUR requires a systematic protocol, 150-350 references and a
generative taxonomy, and forbids a new system being the evidence. The survey is a
separate, genuinely unfilled paper.

**Q10. Your transport mix is modelled, not measured.**
Correct. The mix shares are plausible; the failure numbers do not exist yet, and
those are the interesting ones. Measure them before submitting.
