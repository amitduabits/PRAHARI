# P4 anticipated reviewer questions

**Q1. Is refuse-at-the-bound not just Erlang-B?**
Yes. Say it in the introduction, cite 1917, and make clear the contribution is the
coupling to the sweep. — *answerable now, and it must be pre-empted.*

**Q2. "Peak envelope equals K independent of estate size" — is that not the
definition of a K-server loss system?**
Yes. Present it as an invariant with a proof, not as an experimental finding.
— *answerable now.*

**Q3. Your p99 is flat because there is no queue. That is not a scheduling result.**
Correct. The result being reported is the service-time distribution. Keep the
contrast with queueing, drop the framing. — *answerable now.*

**Q4. You assume exponential service times. Real decoder sessions are not.**
`sevastyanov1957` insensitivity: blocking depends only on offered load and K, for
any duration distribution with finite mean. Cite it, and report the empirical
duration distribution. — *answerable once the distribution is measured.*

**Q5. If a refused session is retried on the next sweep, this is a retrial queue,
not a loss system, and B(K,a) is wrong.**
**Not answerable.** The most dangerous question. Either prove refusals are never
retried or model the orbit.

**Q6. A decoder session is not a unit of cost. K bounds a counter, not a resource.**
**Not answerable.** Needs the per-session CPU, memory, bandwidth and NVDEC
measurements. `bossen2012hevc` is the citation they will use.

**Q7. Why is the 80,001st camera less important than the first? Where are your
priority classes?**
**Not answerable** as designed. Mixed-criticality (`vestal2007mixed`) and DAGOR both
stratify. Either add priority or justify uniformity explicitly.

**Q8. Why three strikes, and why not φ-accrual?**
**Not answerable.** Derive 3 from a target false-alarm MTBF and a measured probe-loss
p, and benchmark against `hayashibara2004phi`.

**Q9. Your probe losses are modelled as i.i.d. They are not — a switch flap takes
forty cameras.**
Correct. State that p³ is a lower bound on the false-alarm probability and measure
the correlation structure.

**Q10. What is your refusal rate at each load point?**
0.22 at offered load 0.8, rising to 0.77 at 4.0. It must appear alongside every
latency figure. — *answerable now; the honest number is not flattering.*

**Q11. Why refuse rather than degrade? Brownout says degrade.**
Because degraded evidentiary video is worse than none. **This is asserted, not
demonstrated.** It needs an operator study or an evidentiary-quality argument.

**Q12. Split brain: does K become 2K if an ingest node is wrongly presumed dead?**
**Not answerable.** Specify and test.
