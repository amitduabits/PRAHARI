# P4 prior-art review: deterministic concurrent decoder management

31 verified entries. Five candidates dropped (Jamin et al.'s 1997 ToN version,
substituted with the verified 1995 SIGCOMM/CCR version; Bertier et al. adaptive
failure detector; Breslau et al. INFOCOM 2000 MBAC critique; Mercer et al.
processor capacity reserves; Burns & Davis mixed-criticality survey).

Axes: (1) admission control in multimedia/QoS, (2) overload control and load
shedding, (3) video analytics resource management, (4) real-time schedulability,
(5) loss systems, blocking and tail latency, (6) failure detection and probe
scheduling, (7) decode cost, ingest protocols and VMS scale.

---

## Axis 1 - Admission control in multimedia / QoS systems

**jamin1995mbac** — A Measurement-Based Admission Control Algorithm for Integrated Services Packet Networks. Jamin, Danzig, Shenker, Zhang. 1995. ACM SIGCOMM / CCR 25(4). doi:10.1145/217391.217396
Admits a flow only if measured aggregate load leaves headroom for the loss/delay bound. The canonical measurement-based CAC.
*Differs:* P4's test is a fixed integer session count, not a measured-load predicate, and failure means unconditional refusal, not re-estimation.

**vin1994statistical** — A Statistical Admission Control Algorithm for Multimedia Servers. Vin, Goyal, Goyal, Goyal. 1994. ACM MM. doi:10.1145/192593.192616
Admits streams up to a statistically derived capacity with a bounded deadline-miss probability.
*Differs:* P4 accepts no violation probability; the bound is a hard count and the trade is pushed entirely onto refusal.

**rajkumar1998resource** — Resource Kernels. Rajkumar, Juvva, Molano, Oikawa. 1998. SPIE MMCN vol. 3310. doi:10.1117/12.298417
Timely, guaranteed, enforced reservations of CPU/disk/network, with admission refused when the reservation set is infeasible.
*Differs:* P4 reserves nothing per session and models one dimension; its guarantee comes from cardinality, not a schedulability test.

## Axis 2 - Overload control and load shedding

**welsh2001seda** — SEDA. Welsh, Culler, Brewer. 2001. ACM SOSP / SIGOPS OSR 35(5). doi:10.1145/502059.502057
Stages with explicit bounded queues and per-stage controllers make overload visible.
*Differs:* SEDA's bounded queue is the mechanism P4 deletes; P4 argues the queue itself is the pathology for perishable video.

**welsh2003adaptive** — Adaptive Overload Control for Busy Internet Servers. Welsh, Culler. 2003. USENIX USITS.
Controls 90th-percentile response time by adaptively shedding and degrading.
*Differs:* P4's refusal is static and unconditional; no controller, no target percentile, no degradation branch.

**nichols2012codel** — Controlling Queue Delay. Nichols, Jacobson. 2012. CACM 55(7). doi:10.1145/2209249.2209264
Drops packets on persistent sojourn time to keep standing queues short.
*Differs:* CoDel is drop-from-inside-a-queue with a time signal; P4 has no queue and its signal is an occupancy count.

**klein2014brownout** — Brownout: Building More Robust Cloud Applications. Klein, Maggio, Årzén, Hernández-Rodriguez. 2014. ICSE. doi:10.1145/2568225.2568227
A control-theoretic dimmer drops optional content under load so latency stays bounded without rejecting requests.
*Differs:* brownout is exactly the quality-reduction arm P4 forbids. P4 must argue why partial-fidelity decode is worse than refusal, which brownout implicitly denies.

**zhou2018wechat** — Overload Control for Scaling WeChat Microservices (DAGOR). Zhou, Chen, Lin et al. 2018. ACM SoCC. doi:10.1145/3267809.3267823
Sheds at each microservice using queuing-delay overload detection plus business and user priority, in production at scale.
*Differs:* DAGOR's threshold is dynamic and priority-stratified; P4's is a static uniform K, a strictly weaker policy that must be justified on determinism grounds.

**cho2020breakwater** — Overload Control for μs-scale RPCs with Breakwater. Cho, Saeed, Fried et al. 2020. USENIX OSDI.
Server-driven credit-based admission bounding in-server concurrency to preserve microsecond tails.
*Differs:* Breakwater's credit pool is dynamically sized from measured delay; P4 fixes it a priori and its sessions last seconds to hours.

**tatbul2003loadshedding** — Load Shedding in a Data Stream Manager. Tatbul, Çetintemel, Zdonik et al. 2003. VLDB.
Drops tuples inside a stream query plan when input rates exceed capacity.
*Differs:* P4 sheds at whole-session granularity at ingest, so its loss is all-or-nothing per camera.

## Axis 3 - Video analytics resource management

**zhang2017videostorm** — Live Video Analytics at Scale. Zhang, Ananthanarayanan, Bodik et al. 2017. USENIX NSDI.
Schedules thousands of queries by trading resource allocation against quality and lag.
*Differs:* VideoStorm degrades and delays to fit everything in; P4 refuses instead, and its axis is decoder sessions, not a quality knob.

**jiang2018chameleon** — Chameleon. Jiang, Ananthanarayanan, Bodik et al. 2018. SIGCOMM. doi:10.1145/3230543.3230574
Amortises re-picking near-optimal NN configurations.
*Differs:* P4 holds configuration fixed and adapts admission instead.

**hung2018videoedge** — VideoEdge. Hung, Ananthanarayanan, Bodik et al. 2018. IEEE/ACM SEC. doi:10.1109/SEC.2018.00016
Places and configures pipelines across camera-edge-cloud to maximise accuracy under limits.
*Differs:* P4 does no placement and no accuracy optimisation; it is a single-tier ingest gate whose objective is envelope determinism.

**bhardwaj2022ekya** — Ekya. Bhardwaj, Xia, Ananthanarayanan et al. 2022. USENIX NSDI.
Co-schedules retraining and inference on a shared edge GPU.
*Differs:* P4 has one workload class and its arbitration is a refusal, not a share.

**li2020reducto** — Reducto. Li, Padmanabhan, Zhao et al. 2020. SIGCOMM. doi:10.1145/3387514.3405874
Pushes cheap frame-differencing onto the camera to cut server load.
*Differs:* Reducto reduces demand at the source; P4 bounds supply. A reviewer will ask why not both.

**jain2019scaling** — Scaling Video Analytics Systems to Large Camera Deployments. Jain, Ananthanarayanan, Jiang et al. 2019. HotMobile. doi:10.1145/3301293.3302366
Argues per-camera-independent processing does not scale; proposes cross-camera correlation.
*Differs:* the closest position paper to P4's scaling claim; P4's answer is cardinality-bounded admission rather than sharing, and must contrast the two directly.

**shen2019nexus** — Nexus: A GPU Cluster Engine for Accelerating DNN-Based Video Analysis. Shen, Chen, Jin et al. 2019. ACM SOSP. doi:10.1145/3341301.3359658
Squishy bin-packing of batched inference with per-query latency SLOs, rejecting infeasible placements.
*Differs:* Nexus derives its bound from an SLO through a batching model; P4 asserts K as an operator constant with no derivation.

**gujarati2020clockwork** — Serving DNNs like Clockwork. Gujarati, Karimi, Alzayat et al. 2020. USENIX OSDI. arXiv:2006.02464
Predictable tails by making every layer deterministic, centralising choice, and dropping requests predicted to miss SLO.
*Differs:* the strongest existing "determinism by construction plus refuse-what-you-cannot-serve" system. P4 must position as the same philosophy on a different substrate, not as a novel philosophy.

## Axis 4 - Real-time schedulability

**liu1973scheduling** — Scheduling Algorithms for Multiprogramming in a Hard-Real-Time Environment. Liu, Layland. 1973. JACM 20(1):46-61. doi:10.1145/321738.321743
Rate-monotonic and EDF optimality with utilisation-bound admission tests.
*Differs:* P4's bound is a session count, not a utilisation test; it inherits "admit only what is provably feasible" without a timing model of the work.

**abeni1998cbs** — Integrating Multimedia Applications in Hard Real-Time Systems. Abeni, Buttazzo. 1998. IEEE RTSS.
Constant Bandwidth Server: each soft task gets a reserved, temporally isolated CPU fraction.
*Differs:* CBS bounds per task by reservation and isolation; P4 bounds globally by count and provides no isolation between admitted decoders.

**vestal2007mixed** — Preemptive Scheduling of Multi-criticality Systems. Vestal. 2007. IEEE RTSS. doi:10.1109/RTSS.2007.35
Founds mixed-criticality: on budget overrun, low-criticality work is dropped so high-criticality guarantees hold.
*Differs:* P4 drops by arrival order under a constant bound with no criticality classes. A reviewer will ask why the 80,001st camera is less important than the first.

## Axis 5 - Loss systems, blocking, tail latency

**erlang1917** — Solution of Some Problems in the Theory of Probabilities of Significance in Automatic Telephone Exchanges. Erlang. 1917. Post Office Electrical Engineers' Journal 10:189-197. No DOI (pre-DOI era).
Derives Erlang-B for a loss system with fixed trunks and no waiting room.
*Differs:* **this is P4's admission policy, stated in 1917.** P4 must cite it and claim only the systems instantiation.

**sevastyanov1957** — An Ergodic Theorem for Markov Processes and Its Application to Telephone Systems with Refusals. Sevast'yanov. 1957. Theory Probab. Appl. 2(1):104-112. doi:10.1137/1102005
Proves insensitivity: blocking depends only on offered load and server count, not on the service-time distribution beyond its mean.
*Differs:* none in policy. This is the theorem that makes P4's claim rigorous for realistic heavy-tailed session lifetimes; it should be cited as P4's own proof device.

**kelly1991loss** — Loss Networks. Kelly. 1991. Ann. Appl. Probab. 1(3):319-378. doi:10.1214/aoap/1177005872
Multi-resource blocking, fixed-point approximations, large-system asymptotics.
*Differs:* P4 is the single-resource special case; the multi-resource extension (decoder + CPU + memory) is the problem Kelly formalises and P4 does not solve.

**dean2013tail** — The Tail at Scale. Dean, Barroso. 2013. CACM 56(2):74-80. doi:10.1145/2408776.2408794
Why tail latency dominates at scale, and tail-tolerant techniques.
*Differs:* P4's mechanism is tail *elimination* by construction — an admitted session never waits — so the tail claim is definitional rather than mitigative.

## Axis 6 - Failure detection, hysteresis, probe scheduling

**chandra1996unreliable** — Unreliable Failure Detectors for Reliable Distributed Systems. Chandra, Toueg. 1996. JACM 43(2):225-267. doi:10.1145/226643.226647
Formalises failure detectors by completeness and accuracy.
*Differs:* P4's three-strike rule is an unanalysed eventually-strong detector; the paper states no completeness or accuracy property for it.

**hayashibara2004phi** — The φ Accrual Failure Detector. Hayashibara, Défago, Yared, Katayama. 2004. IEEE SRDS. doi:10.1109/RELDIS.2004.1353004
Continuous suspicion level from the heartbeat-arrival distribution; the application picks its threshold.
*Differs:* the direct competitor to three-strike hysteresis, and adaptive where P4 is fixed. P4 must justify a hard integer 3 against an adaptive score.

**das2002swim** — SWIM. Das, Gupta, Motivala. 2002. IEEE DSN. doi:10.1109/DSN.2002.1028914
Randomised round-robin ping with indirect probing and a suspicion sub-protocol, at constant per-node cost.
*Differs:* **the closest single prior work to P4's health component.** SWIM already gives round-robin probing at bounded rate plus multi-stage hysteresis. P4's differences: centre-out probing of passive cameras rather than peer-to-peer, and coupling the probe budget to the same K as the decoders.

**guo2015pingmesh** — Pingmesh. Guo, Yuan, Xiang et al. 2015. ACM SIGCOMM. doi:10.1145/2785956.2787496
Always-on, budget-controlled probe mesh with engineered probe rates and coverage intervals.
*Differs:* Pingmesh sizes its probe budget independently; P4 shares it with the decoder pool, a coupling Pingmesh does not have and which a reviewer will want measured.

**durumeric2013zmap** — ZMap. Durumeric, Wustrow, Halderman. 2013. USENIX Security.
Stateless, rate-bounded sweeps of an entire address estate with deterministic completion time.
*Differs:* ZMap's coverage-time-equals-estate-over-rate is the same arithmetic as P4's n/K·T; P4 adds statefulness (three-strike memory) and shares the rate bound with decode.

## Axis 7 - Decode cost, ingest protocols, VMS scale

**schulzrinne2016rtsp2** — RTSP 2.0. Schulzrinne, Rao, Lanphier et al. 2016. IETF RFC 7826. doi:10.17487/RFC7826
Defines session establishment, state and teardown, including the 453 "Not Enough Bandwidth" refusal.
*Differs:* P4 should map its refusal onto these existing status codes rather than presenting refusal as a new interface.

**bossen2012hevc** — HEVC Complexity and Implementation Analysis. Bossen, Bross, Sühring, Flynn. 2012. IEEE TCSVT 22(12). doi:10.1109/TCSVT.2012.2221255
Measures decoder complexity and memory bandwidth across configurations and resolutions.
*Differs:* the evidence that a decoder session is **not** a constant-cost unit, which directly threatens P4's claim that counting sessions bounds the resource envelope.

---

## (A) Closest prior art: the five a reviewer will raise

**1. erlang1917 + sevastyanov1957, the Erlang loss system.** *Rebuttal:* Erlang gives a stationary blocking probability for an abstract server pool; it says nothing about decoder cost, enforcing a bound across a distributed ingest fleet without a global lock, or the interaction with a coverage sweep. A queueing result is not a system. *Concession:* the policy is Erlang's. Bounded envelope, load-independent admitted latency and blocking-as-the-only-degradation are all restatements of a 1917 model. We cannot claim the policy.

**2. das2002swim.** *Rebuttal:* SWIM's round-robin probing and suspicion operate over a peer group of mutually probing processes; our sweep is centre-out over passive, non-cooperating cameras that cannot gossip, and our probe concurrency is drawn from the same bounded pool as decode, which creates a resource coupling SWIM never faces. *Concession:* mechanically, "round-robin sweep at bounded rate" plus "multi-strike hysteresis before declaring dead" is SWIM, and our n/K·T bound is SWIM's protocol-period argument. If a reviewer says the health half is SWIM in a surveillance costume, that is fair.

**3. gujarati2020clockwork.** *Rebuttal:* Clockwork makes stateless millisecond inference deterministic and drops requests predicted to miss an SLO; decoder sessions are long-lived, stateful and externally driven, so per-request prediction has no analogue and the bound must be on concurrency. *Concession:* Clockwork already established the thesis "eliminate choice and variance from the bottom up, refuse what you cannot serve, and the tail flattens". Our contribution is a different substrate, not that thesis.

**4. zhang2017videostorm / jiang2018chameleon.** *Rebuttal:* both assume every stream must be served and search a quality/lag space to fit demand into supply. We assert that degraded evidentiary video is worse than no video, so the configuration space collapses and admission becomes the only free variable. *Concession:* that is a domain assumption we assert rather than demonstrate. VideoStorm's delay-tolerance argument and our perishability argument are the same observation with opposite conclusions, and we have no user study or evidentiary-quality analysis to justify choosing refusal.

**5. zhou2018wechat / cho2020breakwater.** *Rebuttal:* both are dynamic controllers with priority stratification tuned continuously against measured delay; their determinism is statistical. Our bound is a compile-time constant, so the peak envelope is provable by inspection rather than an outcome of a loop that can be mistuned. *Concession:* they are strictly more capable, in production at far larger scale, and show priority-aware shedding beats FIFO shedding. Our uniform static K is a degenerate special case, and we have no evidence determinism is worth the lost adaptivity.

---

## (B) Blunt verdict: yes, it is Erlang-B

**Refuse-at-the-bound with no queue is the M/M/c/c loss system, 1917 mathematics.**

- With Poisson arrivals λ, mean duration 1/μ, offered load a = λ/μ, K servers and **zero waiting positions**, refusal probability is Erlang-B, B(K,a) = (a^K/K!) / Σ_{i=0}^{K} a^i/i!.
- **"Peak envelope is exactly K, independent of estate size" is not a finding.** It is the definition of a K-server loss system: the state space is {0,…,K} by construction, and n enters only through λ. Demonstrating it at 800 and 80,000 cameras shows the semaphore has no bug, nothing more.
- **"p99 latency flat across offered load" is likewise definitional.** In a pure loss system there is no waiting time; an admitted session's sojourn is its own service time, independent of λ by assumption. A flat p99 is measuring the service-time distribution, not a scheduling achievement. The contrast case (a queueing tail diverging as ρ→1) is standard M/M/c and Kingman-bound material.
- **The insensitivity result matters more than Erlang-B itself.** sevastyanov1957 proves blocking depends only on a and K, not on the shape of the service-time distribution. Real decoder sessions are wildly non-exponential, so this is the theorem that lets us claim anything rigorously.
- **kelly1991loss** covers the multi-resource generalisation we actually need and do not have.

**What is genuinely left:**

1. **The coupling, not the policy.** Sharing one K between decode and the sweep makes coverage interval n/K·T and blocking probability B(K,a) functions of the same parameter, so choosing K trades detection latency against refusal rate. That two-sided frontier is a real, non-obvious, unpublished design artefact. **Make this the paper.**
2. **Hysteresis under a bounded probe budget.** Detection latency is bounded by 3·⌈n/K⌉·T; false-alarm rate under i.i.d. probe loss p is p³ per triple. Deriving "three" from a target false-alarm MTBF under a probe budget that is itself K is a real result. Asserting "three" is not.
3. **The domain argument** that loss dominates queueing for perishable evidentiary video. This is where the multimedia-venue contribution lives, and it needs evidence, not assertion.
4. **The empirical envelope measurement** in a real VMS at 800→80,000 cameras — only if CPU, memory, PCIe and NVDEC are actually measured, not just the counter.

**The sharpest attack, which must be pre-empted: we do not actually have a loss system.** A refused session retried on the next sweep is a **retrial (orbit) queue**, not M/M/c/c. The queue has not been eliminated, it has been moved into the sweep at a constant retrial rate and made invisible to our instrumentation. Under that model effective blocking is *not* Erlang-B and "no queue" is false as stated. Either prove refusals are never retried, or model it as a constant-retrial-rate M/M/c/c retrial queue and report orbit occupancy. (Falin's 1990 *Queueing Systems* survey and Artalejo & Gómez-Corral's monograph are the standard entry points — **both unverified in this pass; verify before citing.**)

---

## (C) The formal results to state and prove

**Proposition 1 (envelope invariant).** At every instant, live decoder sessions ≤ K. Proof by counting-semaphore argument over admit/release transitions; state the atomicity assumption on the counter and the behaviour under multi-node ingest. Frame it as an invariant, **not** an experimental result — presenting "envelope = K at both scales" as a finding invites the reviewer to say we validated a definition.

**Proposition 2 (refusal probability, insensitive form).** For Poisson requests with offered load a = λ·E[S], stationary refusal probability is B(K,a), for **arbitrary** session-duration distribution with finite mean. Cite erlang1917 for the formula, sevastyanov1957 for insensitivity. Give the recursion B(K,a) = a·B(K−1,a)/(K + a·B(K−1,a)), B(0,a)=1, and use it to state a **K-sizing rule**: the minimum K meeting a target refusal SLO. This converts K from a magic constant into a derived quantity, which is the difference between a system paper and a config note.

**Proposition 3 (coverage interval).** With n cameras, probe concurrency K, per-probe wall time ≤ T, and a work-conserving round robin, every camera is probed within every window C = ⌈n/K⌉·T, and worst-case staleness < C. State the assumptions (bounded probe timeout, no starvation, sweep-pointer persistence across restarts). A reviewer will attack the timeout case, since T is then the timeout not the RTT and C blows up on a degraded estate.

**Proposition 4 (detection latency and false alarms under three strikes).** A camera failing at t is marked offline no later than t + 3C and no earlier than t + 2T. Under independent probe loss p, false-marking probability per triple is p³, giving expected time-to-false-alarm C/p³. **Derive 3 from a target MTBF and a measured p** rather than asserting it. If losses are correlated — and they are, a switch flap takes 40 cameras at once — state that p³ is a lower bound.

**Corollary, the actual contribution.** Combining 2 and 3: the probe budget and the decode budget draw from the same K, so the operator faces a real allocation problem between K_decode and K_probe. **Plot that frontier. That figure is the paper.**

---

## (D) What a systems reviewer will demand and we do not have

Modelling only decoder occupancy is the fatal gap. The argument writes itself: *a decoder session is not a unit of cost.* bossen2012hevc is the citation they will use — decode cost varies by an order of magnitude across resolution, codec, bit depth and GOP. K bounds a counter, not a resource.

**Per-session cost characterisation (missing this kills the claim):**
1. CPU utilisation per session, as a distribution not a mean, by resolution (D1/720p/1080p/4K), codec (H.264/HEVC) and frame rate, with the coefficient of variation.
2. Resident and peak memory per session, including the decoded-frame buffer pool and its dependence on reference-frame count.
3. NVDEC/VAAPI hardware-decoder occupancy and the **vendor concurrent-session limits**, which are hard caps that interact with K.
4. Memory-bandwidth and PCIe-bandwidth per session — usually the real bottleneck before core count.
5. File-descriptor, socket and thread counts per session.

**Envelope validation, not assertion:**
6. Measured peak of every resource at K versus the linear extrapolation K·(mean per-session cost). It will be superlinear via cache and memory-bandwidth contention, which makes "envelope is exactly K" true for the counter and false for the machine. **Report the non-linearity honestly.**
7. Worst-case-mix stress: all K sessions at 4K HEVC simultaneously, not a representative mix.

**Latency methodology:**
8. State which latency is measured — session establishment, first frame, or steady-state frame-to-inference. Only the first is arguably affected by admission control.
9. Open-loop load generator, not closed-loop. A closed-loop generator cannot produce the tail divergence we claim to avoid, and a reviewer at this venue will check.
10. Full CDFs, not p99 points; also p99.9.
11. **Refusal rate at every load point, alongside latency.** A flat p99 obtained by refusing 60% of requests is arithmetic, not a result. Omitting this is the single most likely cause of rejection.

**Scale claim:**
12. State plainly whether the 80,000-camera experiment used real cameras, emulated RTSP sources or a synthetic trace; if emulated, characterise fidelity on session duration and failure behaviour.
13. The arrival process actually observed. Police estates have strong diurnal and incident-driven bursts, which breaks the Poisson assumption behind Erlang-B and matters for the tail.
14. The empirical session-duration distribution, which is what justifies invoking sevastyanov1957 rather than assuming exponential.

**Sweep and health:**
15. Measured coverage interval versus ⌈n/K⌉·T, including the tail of probe completion times.
16. Measured probe-loss probability p and its **correlation structure**, to justify or refute the p³ model.
17. Detection-latency distribution and false-positive/negative rates for three-strike, against at least one baseline; hayashibara2004phi is the obvious one and its absence will be noted.
18. Interference between sweep and decode when both draw from K: does an estate-wide network incident starve decode admission with timing-out probes? This is the most interesting failure mode in the system and should be measured deliberately.

**Baselines that must be implemented, or this is a single-system description:**
19. Bounded queue with timeout (SEDA-style). 20. LRU/idle eviction. 21. Quality-reduction admission (the brownout arm). 22. A dynamic controller (DAGOR-style).
Report all four on the same axes: p99, refusal/eviction/degradation rate, and peak resource envelope.

**Overhead and correctness:**
23. Cost of the admission check under contention, and the synchronisation design across ingest nodes at 80,000 cameras.
24. Behaviour on ingest-node failure: does K become 2K when a peer is wrongly presumed dead? The classic split-brain failure of a distributed global bound.

---

## Bottom line for framing

Drop "we introduce refuse-at-the-bound" — that is Erlang 1917 and a TOMM or TMM
reviewer will know it. Lead with the K-allocation frontier between decode
admission and probe coverage, prove Propositions 2-4, cite Sevastyanov for
insensitivity, address the retrial-queue objection head on, and back it with real
multi-resource measurements. Without the CPU/memory/NVDEC data, the central claim
reduces to "our semaphore works".
