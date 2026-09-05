# P1 prior-art review: provenance-aware inference dispatch

Verified against arXiv, USENIX, ACM DL, IEEE Xplore and DBLP. 30 entries.
Six candidates were dropped as unverifiable. Scanner (SIGGRAPH 2018), Llama
(SoCC 2021) and Clipper (NSDI 2017) were checked and deliberately excluded: all
three are real, but none contains a policy, provenance or gating mechanism, so
they add nothing beyond what VideoStorm / Chameleon / INFaaS already establish.

Axes: (1) policy-based access control for ML inference, (2) privacy-by-construction
and purpose limitation in video, (3) provenance and lineage that gates rather than
records, (4) federated / multi-tenant video analytics systems, (5) consent and
enrollment-vs-inference decoupling, (6) enforcement at the model-loading layer and
information-flow control, (7) "the model saw the pixels" as a distinct harm.

---

## Entries

**zhang2017videostorm** — Live Video Analytics at Scale with Approximation and Delay-Tolerance. Zhang, Ananthanarayanan, Bodik et al. 2017. USENIX NSDI. usenix.org/conference/nsdi17/technical-sessions/presentation/zhang
Schedules concurrent video queries across a cluster, trading per-query accuracy against lag under contention.
*Differs:* its admission decision is a utility computation, not an authorization one; a query is never *forbidden* for a camera. Axis 4.

**jiang2018chameleon** — Chameleon: Scalable Adaptation of Video Analytics. Jiang, Ananthanarayanan, Bodik et al. 2018. ACM SIGCOMM. doi:10.1145/3230543.3230574
Amortises NN-configuration search across time and correlated cameras.
*Differs:* Chameleon's central optimisation is cross-camera sharing, which is exactly what P1's provenance boundary forbids. Axis 4.

**hsieh2018focus** — Focus: Querying Large Video Datasets with Low Latency and Low Cost. Hsieh, Ananthanarayanan, Bodik et al. 2018. USENIX OSDI. arXiv:1801.03493
Splits querying into cheap ingest-time indexing and expensive query-time refinement.
*Differs:* the clearest prior example of shifting work to ingest time, but what it precomputes is an index for speed, not an authorization decision. Axis 4.

**li2020reducto** — Reducto: On-Camera Filtering for Resource-Efficient Real-Time Video Analytics. Li, Padmanabhan, Zhao et al. 2020. ACM SIGCOMM. doi:10.1145/3387514.3405874
Filters frames on-camera using cheap features so only useful frames reach the server model.
*Differs:* drops frames on predicted output irrelevance; P1 blocks an entire model class on provenance. Axis 4.

**bhardwaj2022ekya** — Ekya: Continuous Learning of Video Analytics Models on Edge Compute Servers. Bhardwaj, Xia, Ananthanarayanan et al. 2022. USENIX NSDI. arXiv:2012.10557
Jointly schedules retraining and inference on edge servers within a GPU budget.
*Differs:* assumes camera pixels may be freely reused as training data, which P1's data-use class is precisely designed to forbid for some cameras. Axis 4.

**romero2021infaas** — INFaaS: Automated Model-less Inference Serving. Romero, Li, Yadwadkar, Kozyrakis. 2021. USENIX ATC. usenix.org/conference/atc21/presentation/romero
Selects and loads model variants on demand, including lazy load and unload of weights.
*Differs:* the closest technical analogue to P1's lazy construction, but its predicate is a performance SLO, never a permission. Axis 6.

**cangialosi2022privid** — Privid: Practical, Privacy-Preserving Video Analytics Queries. Cangialosi, Agarwal, Arun et al. 2022. USENIX NSDI. arXiv:2106.12083
Executes analyst queries under a differential-privacy budget by chunking video and perturbing aggregates.
*Differs:* the canonical instance of the design P1 argues against — the untrusted model does run over raw pixels; Privid protects the answer, P1 protects the exposure. Axis 7.

**poddar2020visor** — Visor: Privacy-Preserving Video Analytics as a Cloud Service. Poddar, Ananthanarayanan, Setty et al. 2020. USENIX Security. arXiv:2006.09628
Runs the pipeline inside CPU and GPU TEEs and closes the side channels.
*Differs:* hides pixels from the infrastructure operator while running every requested model; P1 hides pixels from a specific model on the camera owner's behalf. Axis 2.

**roesner2014wdac** — World-Driven Access Control for Continuous Sensing. Roesner, Molnar, Moshchuk et al. 2014. ACM CCS. doi:10.1145/2660267.2660319
Real-world objects broadcast machine-readable policies that a trusted platform detects and applies.
*Differs:* the strongest conceptual ancestor, but its policies are discovered *at sensing time* by running detectors over the very frames being protected. Axis 1.

**kim2023erebus** — Erebus: Access Control for Augmented Reality Systems. Kim, Goutam, Rahmati, Kaufman. 2023. USENIX Security. usenix.org/conference/usenixsecurity23/presentation/kim-yoonsang
A permission DSL giving AR apps least-privilege access to perception outputs rather than raw sensors.
*Differs:* mediates what an application may *receive*; the platform's recognizers still run. Output-level least privilege, not invocation-level. Axis 6.

**jana2013darkly** — A Scanner Darkly: Protecting User Privacy from Perceptual Applications. Jana, Narayanan, Shmatikov. 2013. IEEE S&P. doi:10.1109/SP.2013.31
Interposes a privacy layer returning transformed features instead of raw frames.
*Differs:* degrades the input uniformly for all applications; P1 keeps full fidelity for permitted engines and denies the pipeline entirely for forbidden ones. Axis 6.

**aditya2016ipic** — I-Pic: A Platform for Privacy-Compliant Image Capture. Aditya, Sen, Druschel et al. 2016. ACM MobiSys. doi:10.1145/2906388.2906412
Bystanders broadcast a privacy choice plus a face descriptor so nearby cameras obscure them at capture.
*Differs:* binds consent to a *subject* and applies it per-capture by running face matching on every frame, which is itself an inference; P1 binds policy to the *camera* before capture. Axis 5.

**raval2016markit** — What You Mark is What Apps See. Raval, Srivastava, Razeen et al. 2016. ACM MobiSys. doi:10.1145/2906388.2906405
Users physically mark private regions; the OS redacts them before any app sees the stream.
*Differs:* redacts spatial regions identically for all apps; P1 partitions the model set per camera. Axis 6.

**shu2018cardea** — Cardea: Context-Aware Visual Privacy Protection for Photo Taking and Sharing. Shu, Zheng, Hui. 2018. ACM MMSys. doi:10.1145/3204949.3204973
Enforces context-dependent visual privacy preferences at capture and sharing.
*Differs:* evaluates context per photo using cloud-side recognition — the query-time re-evaluation P1 replaces with a compiled mask. Axis 5.

**bagdasaryan2019ancile** — Ancile: Enhancing Privacy for Ubiquitous Computing with Use-Based Privacy. Bagdasaryan, Berlstein, Waterman et al. 2019. ACM WPES. doi:10.1145/3338498.3358642
Data carries a reactive program specifying permitted transformations; applications may only apply admitted operations.
*Differs:* the strongest formal match for policy-that-gates-computation, but policies are interpreted dynamically per operation and the forbidden module stays resident and callable. Axis 1.

**wang2019riverbed** — Riverbed: Enforcing User-defined Privacy Constraints in Distributed Web Services. Wang, Ko, Mickens. 2019. USENIX NSDI. usenix.org/conference/nsdi19/presentation/wang-frank
Refuses to send data to server instances whose declared processing does not satisfy the attached policy.
*Differs:* gates at the granularity of a server instance via attestation; P1 gates an individual engine inside one process. Axis 6.

**yip2009resin** — Improving Application Security with Data Flow Assertions. Yip, Wang, Zeldovich, Kaashoek. 2009. ACM SOSP. doi:10.1145/1629575.1629604
Language-runtime data-flow assertions checked wherever tainted data crosses an I/O boundary.
*Differs:* checks at output boundaries — exactly P1's naive-union baseline. Can prove an embedding was never released, not that it was never computed. Axis 6.

**myers1997difc** — A Decentralized Model for Information Flow Control. Myers, Liskov. 1997. ACM SOSP. doi:10.1145/268998.266669
Decentralized labels enabling static checking of information flow under mutual distrust.
*Differs:* constrains where data may flow, not which computation may be instantiated; a face model with a restrictive output label is DIFC-legal and P1-illegal. Axis 6.

**watson2010capsicum** — Capsicum: Practical Capabilities for UNIX. Watson, Anderson, Laurie, Kennaway. 2010. USENIX Security. usenix.org/conference/usenixsecurity10/capsicum-practical-capabilities-unix
Capability mode: a process holds an unforgeable pre-acquired set of rights and cannot name resources outside it.
*Differs:* operates on descriptors and syscalls; P1's contribution is instantiating that discipline over model engines with provenance as the capability source. Axis 1.

**byun2008purpose** — Purpose Based Access Control for Privacy Protection in Relational Database Systems. Byun, Li. 2008. The VLDB Journal. doi:10.1007/s00778-006-0023-0
Labels data with intended purposes and queries with access purposes; grants on entailment.
*Differs:* evaluated per query against stored tuples; P1 evaluates purpose once per camera and compiles it into a dispatch mask over models. Axis 1.

**agrawal2002hippocratic** — Hippocratic Databases. Agrawal, Kiernan, Srikant, Xu. 2002. VLDB. doi:10.1016/B978-155860869-6/50021-4
Purpose, consent and limited retention as first-class schema elements enforced by the engine.
*Differs:* established purpose-binding-in-architecture for structured records; P1 extends it to an unstructured sensor stream enforced against neural models. Axis 2.

**park2012pbac** — A Provenance-based Access Control Model. Park, Nguyen, Sandhu. 2012. IEEE PST. doi:10.1109/PST.2012.6297930
Access decisions computed from a provenance graph rather than subject/object attributes.
*Differs:* the gating is a runtime query over the provenance DAG at each access; P1 shows the query is loop-invariant per camera and hoists it out of the frame loop. Axis 3.

**muniswamyreddy2006pass** — Provenance-Aware Storage Systems. Muniswamy-Reddy, Holland, Braun, Seltzer. 2006. USENIX ATC. usenix.org/legacy/events/usenix06/tech/full_papers/muniswamy-reddy/
Collects file lineage at the OS layer so ancestry can be queried later.
*Differs:* makes provenance observable, explicitly not operative; can report afterwards that a forbidden model read a stream, not prevent it. Axis 3.

**namaki2020vamsa** — Vamsa: Automated Provenance Tracking in Data Science Scripts. Namaki, Floratou, Psallidas et al. 2020. ACM KDD. doi:10.1145/3394486.3403205
Statically recovers which dataset columns fed which trained model, for compliance.
*Differs:* reconstructs lineage after the fact for audit; P1 uses provenance ex ante as an admission predicate. Axis 3.

**mitchell2019modelcards** — Model Cards for Model Reporting. Mitchell, Wu, Zaldivar et al. 2019. ACM FAT*. doi:10.1145/3287560.3287596
Standard documentation declaring intended and out-of-scope uses.
*Differs:* states intended use in prose for humans; P1 makes it machine-checkable and binding. Axis 3.

**gebru2021datasheets** — Datasheets for Datasets. Gebru, Morgenstern, Vecchione et al. 2021. CACM. doi:10.1145/3458723
Standardised documentation of a dataset's provenance, consent and recommended uses.
*Differs:* records almost exactly P1's registration inputs, but terminates in a document. Axis 3.

**liu2008xengine** — XEngine: A Fast and Scalable XACML Policy Evaluation Engine. Liu, Chen, Hwang, Xie. 2008. ACM SIGMETRICS. doi:10.1145/1375457.1375488
Compiles XACML into a normalised decision-diagram form for orders-of-magnitude faster evaluation.
*Differs:* the true precedent for compiling a policy into a fast structure, but it still evaluates per request and returns permit/deny to a caller already invoked. Axis 1.

**shastri2019sevensins** — The Seven Sins of Personal-Data Processing Systems under GDPR. Shastri, Wasserman, Chidambaram. 2019. USENIX HotCloud. arXiv:1903.09305
Identifies structural conflicts between GDPR purpose limitation and modern data-system design.
*Differs:* names purpose limitation as an unmet systems requirement; motivation for P1, not prior art against it. Axis 2.

**nissenbaum2004contextual** — Privacy as Contextual Integrity. Nissenbaum. 2004. Washington Law Review 79(1):119-158.
Privacy as preservation of context-relative informational norms.
*Differs:* the normative justification for jurisdiction- and ownership-scoped model permissions; offers no mechanism. Axis 2.

**kaminski2017avertingroboteyes** — Averting Robot Eyes. Kaminski, Rueben, Smart, Grimm. 2017. Maryland Law Review 76(4).
Argues a sensor's *perception* of a person is itself privacy-relevant, distinct from recording or disclosure.
*Differs:* the only work found that states P1's axis-7 premise directly, but as legal argument with no system, measurement or mechanism. Axis 7.

---

## (A) Closest prior art: the five a CVPR reviewer will raise

**1. roesner2014wdac (World-Driven Access Control, CCS 2014).**
*Rebuttal:* WDAC discovers policy by running detectors over the live stream — the policy-detection pass is itself an inference over the pixels it protects, and detection failure is an acknowledged attack surface. P1's decision is offline against a registry record: no perception in the loop, no false-negative policy channel.
*Concession:* WDAC already owns the idea that policy is a property of the device or scene rather than of the query, and already argues for enforcing it below the application. P1's novelty is timing and compilation, not the concept of world-attached policy.

**2. bagdasaryan2019ancile (WPES 2019).**
*Rebuttal:* Ancile interprets use-based policies per operation; the forbidden transformation is a resident, callable object refused at call time. P1's lazy construction means the weights are never resident, changing the threat model from "the policy engine must be correct" to "the code path does not exist".
*Concession:* Ancile genuinely is provenance/policy that gates computation rather than records it. If a reviewer says the conceptual contribution is Ancile's, that is defensible; the honest differentiator is the static O(1) set and the memory-residency claim.

**3. watson2010capsicum (USENIX Security 2010).**
*Rebuttal:* Capsicum concerns OS resources and has no notion of models, provenance attributes or inference dispatch; porting its discipline to a model registry raises new questions (how the mask is attested, what re-registration does, how shared backbones interact).
*Concession:* the mechanism is architecturally identical — rights fixed at entry, enforced by unavailability. A reviewer can fairly call this capability mode for model registries, and the paper should say so first.

**4. liu2008xengine (SIGMETRICS 2008).**
*Rebuttal:* XEngine makes the check cheap, not absent. P1's claim is that after registration there is no check and no callee.
*Concession:* "compile once, evaluate in near-constant time" is XEngine's stated contribution. The O(1) bitmask claim alone is not novel against it; only consumption at object-construction time is.

**5. cangialosi2022privid (NSDI 2022).**
*Rebuttal:* Privid is P1's named strawman and behaves as described — the analyst's model runs over raw video and privacy is recovered by noising the aggregate. Under P1's threat model (a curious or compromised operator of the analytics stack) that offers nothing.
*Concession:* Privid gives a *formal* guarantee with a stated budget. P1 gives an architectural guarantee with no formal statement about what a permitted model leaks about a forbidden attribute — a permitted person-detector can still be probed for identity. Reviewers will press this, and the paper needs an answer.

---

## (B) Does anything anticipate registration-time compilation of a permitted-model set?

**No.** No paper compiles device-provenance attributes at enrollment into a static
permitted-engine set consumed by the dispatcher. A direct search for it returned
product documentation, not literature.

Closest, in descending order:

1. **bagdasaryan2019ancile** — closest in *semantics*; differs in *time* (dynamic, per-operation, forbidden code loaded).
2. **liu2008xengine** — closest in *mechanism*; differs in *what is gated* (a decision returned to a running request; nothing is unbuilt).
3. **watson2010capsicum** — closest in *enforcement discipline*; differs in *domain* (OS objects, no provenance input).
4. **romero2021infaas** — closest in *implementation artefact* (real lazy model load/unload); differs completely in *predicate* (SLO, not permission).

Honest summary for the related-work section: every ingredient exists separately,
and no published work combines them at the camera-registration boundary for video
inference. That is a legitimate but **combinational** novelty claim, and a strong
reviewer will read it that way. The paper is much safer if the empirical
contribution — a measurement separating "model was invoked" from "output was
released", which only kaminski2017avertingroboteyes even asserts and no systems
paper measures — carries as much weight as the mechanism.

---

## (C) Venues where this framing has already appeared

1. **ACM CCS / IEEE S&P** — roesner2014wdac, jana2013darkly. The natural home for gating what the perception stack may compute.
2. **USENIX Security** — kim2023erebus, poddar2020visor, watson2010capsicum. Erebus makes "least privilege over vision capabilities" current here.
3. **ACM WPES** — bagdasaryan2019ancile. Use-based privacy as policy-that-gates-computation was published exactly here.
4. **USENIX NSDI / OSDI** — cangialosi2022privid, wang2019riverbed, and the video-analytics line P1 argues against.
5. **ACM MobiSys** — aditya2016ipic, raval2016markit. Capture-time consent enforcement is a MobiSys tradition.
6. **ACM FAccT** — mitchell2019modelcards, as documentation only.

**Implication:** the framing has *not* appeared at CVPR/ICCV/ECCV. That is both
the opportunity and the risk — the vision community will find it novel and a
security-literate reviewer will find it familiar. Cite roesner2014wdac,
bagdasaryan2019ancile and watson2010capsicum prominently and early; being seen to
have missed them is the single most likely cause of a reject.

---

## Verification caveats

Page ranges for hsieh2018focus, cangialosi2022privid, poddar2020visor,
romero2021infaas, bhardwaj2022ekya, wang2019riverbed, muniswamyreddy2006pass,
namaki2020vamsa and mitchell2019modelcards come from proceedings records rather
than PDF front matter in every case; the DOIs, arXiv ids and URLs are directly
verified. Capsicum and the HotCloud paper have no page numbers in the canonical
USENIX record, so none are given.
