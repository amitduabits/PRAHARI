# P6 prior-art review: multi-authority video analytics platform design

32 verified entries. Four dropped for unverifiable metadata (Krebs/Momm/Kounev
CLOSER'12; Bezemer & Zaidman IWPSE-EVOL'10; an Elsevier article on ICCC governance
in India's 100 smart cities; every "IoT zero-touch onboarding survey" hit, which
were vendor blogs rather than literature and were replaced by RFC 8572).

Axes: (1) city-scale surveillance and smart-city platforms, (2) video analytics
architecture and edge-cloud reference designs, (3) federation without trust
(dataspaces, mediators, data mesh, federated identity), (4) physical-security and
streaming standards, (5) onboarding and provisioning cost at scale, (6) audit
logging and accountability, (7) governance and oversight.

---

## Axis 1 - City-scale surveillance and smart-city platforms

**khochare2021anveshak** — A Scalable Platform for Distributed Object Tracking Across a Many-Camera Network. Khochare, Krishnan, Simmhan. 2021. IEEE TPDS. doi:10.1109/TPDS.2021.3049450 (arXiv:1902.05577)
Programming model and runtime that tracks an object across a wide-area camera network by dynamically scaling which streams are analysed.
*Differs:* P6 does not schedule analytics across a network it owns; it addresses how cameras owned by *different authorities* enter one registry at all, and measures onboarding rather than tracking accuracy.

**jain2020spatula** — Spatula: Efficient Cross-camera Video Analytics on Large Camera Networks. Jain, Zhang, Zhou et al. 2020. IEEE/ACM SEC. doi:10.1109/SEC50012.2020.00016
Exploits spatio-temporal correlation to prune which streams a cross-camera query must touch.
*Differs:* assumes a single administrative domain with known topology; P6's contribution is the registry-provenance layer that makes topology partially unknown and multi-owner.

**sanchez2014smartsantander** — SmartSantander: IoT Experimentation over a Smart City Testbed. Sánchez, Muñoz, Galache et al. 2014. Computer Networks 61:217-238. doi:10.1016/j.bjp.2013.12.020
Architecture, node tiers and management plane of a ~20,000-device city testbed.
*Differs:* closest in spirit, but cheap sensors under one municipal owner; P6 targets 80,000 cameras across authorities that will not expose device APIs.

**sanchez2017lessons** — Practical Lessons From the Deployment and Management of a Smart City IoT Infrastructure. Sánchez, Gutiérrez, Galache et al. 2017. IEEE Access 5:14309-14322. doi:10.1109/ACCESS.2017.2723659
Operational experience, failure modes and management cost over years.
*Differs:* the strongest existing "operational cost at city scale" paper. P6 differs by making cost per onboarded device a measured design variable across three onboarding modes, not a retrospective lessons list.

**cirillo2019fiware** — A Standard-Based Open Source IoT Platform: FIWARE. Cirillo, Solmaz, Berz et al. 2019. IEEE IoT Magazine 2(3):12-18. doi:10.1109/IOTM.0001.1800022
NGSI context-broker reference architecture for cross-domain smart-city platforms.
*Differs:* FIWARE federates via live context brokers each party must run; P6's stance is the opposite — contributors run nothing and hand over rows.

**ezzat2021horizontal** — Horizontal Review on Video Surveillance for Smart Cities. Ezzat, Abd El Ghany, Almotairi, Salem. 2021. Sensors 21(9):3222. doi:10.3390/s21093222
Reviews smart-city video surveillance across edge hardware, applications and datasets.
*Differs:* a capability review, not an architecture with a deployment target.

**praharaj2020iccc** — Development Challenges for Big Data Command and Control Centres for Smart Cities in India. Praharaj. 2020. In *Data-driven Multivalence in the Built Environment*. doi:10.1007/978-3-030-12180-8_4
Analyses India's Integrated Command and Control Centres across 83 cities, finding surveillance-first, privatised architectures.
*Differs:* directly P6's deployment context but written as urban-policy critique with no system design; P6 supplies the platform layer this chapter says is missing.

## Axis 2 - Video analytics architecture and reference designs

**lu2016optasia** — Optasia: A Relational Platform for Efficient Large-Scale Video Analytics. Lu, Chowdhery, Kandula. 2016. ACM SoCC. doi:10.1145/2987550.2987564
Exposes camera analytics as relational queries so an optimiser can dedupe and parallelise across cameras.
*Differs:* Optasia's boundary starts once streams are already ingestible; P6's starts one step earlier, at registry and transport negotiation.

**zhang2017videostorm** — Live Video Analytics at Scale. Zhang, Ananthanarayanan, Bodik et al. 2017. USENIX NSDI.
Schedules thousands of concurrent queries against a resource-quality-lag tradeoff.
*Differs:* scale there means query load on owned clusters; P6's scale axis is administrative, and its metric is onboarding.

**hung2018videoedge** — VideoEdge. Hung, Ananthanarayanan, Bodik et al. 2018. IEEE/ACM SEC. doi:10.1109/SEC.2018.00016
Places query components across a camera-edge-cloud hierarchy.
*Differs:* placement optimisation over a hierarchy the operator controls; P6 cannot assume control of anything upstream of the registry row.

**ananthanarayanan2017killerapp** — Real-Time Video Analytics: The Killer App for Edge Computing. Ananthanarayanan, Bahl, Bodík et al. 2017. IEEE Computer 50(10):58-67. doi:10.1109/MC.2017.3641638
The Microsoft Rocket vision and reference stack for city-scale live video analytics.
*Differs:* a vision paper without provisioning economics; P6 is the same genre but must earn its place with measured cost, transport mix and audit growth.

**xu2023edgesurvey** — Edge Video Analytics: A Survey. Xu, Razavi, Zheng. 2023. IEEE COMST 25(4):2951-2982. doi:10.1109/COMST.2023.3323091
Systematises edge video analytics applications, designs and enabling techniques.
*Differs:* the taxonomy a CSUR reviewer will benchmark P6 against. P6 is not a survey and must not pretend to be one.

**hu2023edgebased** — Edge-Based Video Analytics: A Survey. Hu, Luo, Pasdar et al. 2023. arXiv:2303.14329
Surveys edge pipelines, offloading and configuration adaptation.
*Differs:* contains no treatment of multi-owner registry federation — the gap P6 should name explicitly.

**gong2025cet** — A Survey on Video Analytics in Cloud-Edge-Terminal Collaborative Systems. Gong, Yang, Fang et al. 2025. arXiv:2502.06581
Surveys collaborative video analytics, scheduling and model partitioning.
*Differs:* confirms the field's centre of gravity is resource scheduling, leaving cross-authority integration untouched.

## Axis 3 - Federation without trust

**franklin2005dataspaces** — From Databases to Dataspaces. Franklin, Halevy, Maier. 2005. ACM SIGMOD Record 34(4):27-33. doi:10.1145/1107499.1107502
Pay-as-you-go integration: a catalogue of participant descriptions exists before, and without, full schema integration.
*Differs:* **the single most dangerous prior art for P6's central claim.** See (C).

**lenzerini2002dataintegration** — Data Integration: A Theoretical Perspective. Lenzerini. 2002. ACM PODS. doi:10.1145/543613.543644
Formalises global-as-view / local-as-view mediated integration over autonomous sources.
*Differs:* P6's registry is a degenerate GAV mediation over camera descriptors; cite it rather than let a reviewer find it.

**wiederhold1992mediators** — Mediators in the Architecture of Future Information Systems. Wiederhold. 1992. IEEE Computer 25(3):38-49. doi:10.1109/2.121508
The mediator layer reconciling autonomous heterogeneous sources without changing them.
*Differs:* the 34-year-old ancestor of "contribute rows, not endpoints". P6's novelty cannot be the pattern.

**bader2020idsim** — The International Data Spaces Information Model. Bader, Pullmann, Mader et al. 2020. ISWC. doi:10.1007/978-3-030-62466-8_12
Ontology for describing data-space participants, resources and usage restrictions.
*Differs:* IDS still requires each participant to operate a connector; P6's contributors operate nothing, a real delta worth quantifying in integration effort.

**braud2021gaiax** — The Road to European Digital Sovereignty with Gaia-X and IDSA. Braud, Fromentoux, Radier, Le Grand. 2021. IEEE Network 35(2):4-5. doi:10.1109/MNET.2021.9387709
Positions Gaia-X and IDSA as federated infrastructure for organisations that do not trust each other.
*Differs:* policy-level framing with no operational cost data; use it to establish the problem class, not to claim novelty.

**machado2022datamesh** — Data Mesh: Concepts and Principles. Machado, Costa, Santos. 2022. Procedia Computer Science 196:263-271. doi:10.1016/j.procs.2021.12.013
Domain ownership, data-as-a-product, federated computational governance.
*Differs:* data mesh assumes each domain team runs and serves its product; P6 inverts this, which is the sharpest available contrast.

**chadwick2009fim** — Federated Identity Management. Chadwick. 2009. FOSAD, LNCS. doi:10.1007/978-3-642-03829-7_3
Federated identity models, trust establishment and attribute release across domains.
*Differs:* federating identity still requires each authority to run an IdP; P6 avoids that for camera contribution, and should say why that is acceptable and where it is not.

**eugster2003pubsub** — The Many Faces of Publish/Subscribe. Eugster, Felber, Guerraoui, Kermarrec. 2003. ACM CSUR 35(2):114-131. doi:10.1145/857076.857078
The design space of pub/sub decoupling in space, time and synchronisation.
*Differs:* the reference for P6's event-bus layer; the contribution is subscriber scoping by contributing authority, not the pattern.

## Axis 4 - Standards (marked as standards, not prior art)

**rfc7826** *(STANDARD)* — RTSP 2.0. Schulzrinne, Rao, Lanphier et al. 2016. IETF. doi:10.17487/RFC7826
**rfc8216** *(STANDARD)* — HTTP Live Streaming. Pantos, May. 2017. IETF.
**rfc9725** *(STANDARD)* — WebRTC-HTTP Ingestion Protocol (WHIP). 2025. IETF.
**whep** *(STANDARD, draft)* — WebRTC-HTTP Egress Protocol. draft-ietf-wish-whep-04, 2026. P6 should flag that WHEP is still an Internet-Draft, which is itself an honest operational finding about transport-mix risk.
**onvif** *(STANDARD)* — ONVIF Profiles and Core Specification.
*Differs across all five:* these are ingest modes, not contributions. P6's premise is that ONVIF conformance is claimed far more often than it interoperates in the field; **quantifying that gap across an 80k estate would be a genuine contribution no standard or vendor paper provides.**

## Axis 5 - Onboarding and provisioning cost

**rfc8572** *(STANDARD)* — Secure Zero Touch Provisioning. Watsen, Farrer, Abrahamsson. 2019. IETF.
Bootstraps factory-default devices without operator input.
*Differs:* SZTP requires vendor and owner cooperation; P6's contributors cannot or will not touch their devices, which is why registry rows are the unit of contribution.

**rahman2019iac** — A Systematic Mapping Study of Infrastructure as Code Research. Rahman, Mahdavi-Hezaveh, Williams. 2019. IST 108:65-77. doi:10.1016/j.infsof.2018.12.004
Maps the IaC research landscape including provisioning automation.
*Differs:* establishes provisioning cost as a legitimate research object; P6 extends it from machines to third-party physical devices.

**tang2015config** — Holistic Configuration Management at Facebook. Tang, Kooburat, Venkatachalam et al. 2015. ACM SOSP. doi:10.1145/2815400.2815401
A production configuration system with quantitative data on change volume and operational cost.
*Differs:* **the best available template for how to make onboarding cost publishable.** Copy its measurement discipline, not its subject.

## Axis 6 - Audit logging and accountability

**crosby2009tamper** — Efficient Data Structures for Tamper-Evident Logging. Crosby, Wallach. 2009. USENIX Security.
History trees giving append-only logs with efficient membership and incremental proofs.
*Differs:* gives P6 the mechanism; P6's contribution must be the growth-rate and retention economics at 80k cameras, not the data structure.

**rfc6962** *(STANDARD)* — Certificate Transparency. Laurie, Langley, Kasper. 2013. IETF.
Public append-only Merkle logs with monitors and auditors as a governance mechanism.
*Differs:* the strongest architectural analogue for multi-authority oversight; P6 should either adopt or explicitly reject the monitor/auditor split and say why.

**haeberlen2007peerreview** — PeerReview: Practical Accountability for Distributed Systems. Haeberlen, Kouznetsov, Druschel. 2007. ACM SOSP. doi:10.1145/1294261.1294279
Provable accountability in a mutually distrusting system via tamper-evident logs and witnesses.
*Differs:* directly on point for "authorities that do not trust each other". P6 does not attempt Byzantine accountability and should concede its audit log is evidentiary, not adversarially provable.

## Axis 7 - Governance and oversight

**padilla2015visualprivacy** — Visual Privacy Protection Methods: A Survey. Padilla-López, Chaaraoui, Flórez-Revuelta. 2015. ESWA 42(9):4177-4195. doi:10.1016/j.eswa.2015.01.041
Redaction, obfuscation and privacy-by-design for video.
*Differs:* P6's actual privacy lever is architectural (who may subscribe to which events), not pixel-level.

**kitchin2014realtime** — The Real-Time City? Kitchin. 2014. GeoJournal 79(1):1-14. doi:10.1007/s10708-013-9516-8
Critiques real-time urban data infrastructures on technocratic-governance and surveillance grounds.
*Differs:* supplies the normative frame P6's ethics section must engage rather than gesture at.

**fussey2021assisted** — 'Assisted' Facial Recognition and the Reinvention of Suspicion and Discretion in Digital Policing. Fussey, Davies, Innes. 2021. Brit. J. Criminol. 61(2):325-344. doi:10.1093/bjc/azaa068
Ethnography of live facial recognition in UK policing showing how operator discretion reshapes automated outputs.
*Differs:* the empirical basis for arguing that federating estates changes *who* can act on an alert. P6's event-bus subscriber model is exactly the surface this study problematises.

**verma2015borg** — Large-scale Cluster Management at Google with Borg. Verma, Pedrosa, Korupolu et al. 2015. EuroSys. doi:10.1145/2741948.2741964
Included as the exemplar of a single-deployment description that cleared the publication bar. See (B).

---

## (A) Closest prior art: the five a reviewer will raise

**1. franklin2005dataspaces.** *Charge:* "registry rows instead of federation APIs is pay-as-you-go dataspace integration, published in 2005." *Rebuttal:* dataspaces is an abstraction proposal about schema heterogeneity in document and database corpora with no execution semantics; P6 must additionally negotiate live media transport, per-row provenance under legal ownership, and a sweep that reconciles rows against physical reality. None of that is in the dataspace model, and dataspaces never quantified integration cost per source. *Concession:* the core intellectual move — accept descriptors now, defer integration, keep sources autonomous — is theirs. At best P6 is a domain instantiation with an operational cost model.

**2. cirillo2019fiware.** *Rebuttal:* FIWARE requires every contributing domain to deploy and operate a connector or broker adapter, precisely the requirement P6's contributors will not meet; the reported result should be that broker-based federation has a per-authority fixed cost that registry contribution does not. *Concession:* NGSI-LD entity registration *is* a registry-row model with a standardised schema, with real city deployments. Without a measured cost delta against a broker baseline, the distinction collapses into implementation preference.

**3. sanchez2017lessons.** *Rebuttal:* single-owner municipal testbed, low-bandwidth sensors, no transport negotiation, no cross-authority provenance, and retrospective narrative rather than a controlled comparison of onboarding modes. *Concession:* it already established deployment and management cost at city scale as a publishable object, with more longitudinal data than P6 is likely to have. "What does your cost analysis show that theirs did not?" is a fair question.

**4. bader2020idsim / braud2021gaiax.** *Rebuttal:* IDS and Gaia-X solve sovereignty through usage-control policies at connectors, presupposing technically capable, contractually aligned participants. P6's setting — police and municipal estates with no engineering staff and no willingness to expose endpoints — falls outside that participation model. *Concession:* "federating organisations that do not trust each other via descriptions rather than data" is the literal thesis of the data-space movement. P6's stance is a weaker, cheaper point on the same axis, not a new axis.

**5. zhang2017videostorm / lu2016optasia.** *Rebuttal:* both are resource-allocation systems whose input is an already-ingestible set of streams; neither says how a stream gets into the platform, who owns it, or what the 40,001st camera costs. P6's contribution lives below their abstraction line. *Concession:* they define what "a video analytics platform paper" means to this community and cleared the bar with sharp quantitative claims against real baselines. A registry/ingest paper with only descriptive numbers will look thin beside them.

---

## (B) What makes an architecture paper publishable at TETC or CSUR, bluntly

An architecture paper is rejected as an engineering report when it answers *what
we built* instead of *what is now known that was not known before*.

1. **A stated design tension with a falsifiable position.** Not "we built a layered platform" but "endpoint federation and descriptor federation trade integration cost against liveness fidelity, and below X cameras per authority endpoint federation never pays back." A reviewer must be able to imagine a result that would refute you. "Registry rows, not endpoints" is currently a stance; it becomes a contribution when you state where it is the *wrong* choice and show the crossover.
2. **A baseline you implemented, not a strawman.** CSV vs REST vs web form is a three-way A/B of your own UI, and reviewers will say so. You need an external comparator: ONVIF/WS-Discovery auto-onboard, NGSI-LD broker registration, or a VMS-federation path with published per-site effort. Without one, the cost numbers are self-referential.
3. **Generality that survives removing your deployment.** State the architecture as invariants and their consequences (the registry row is the unit of ownership; ingest is transport-agnostic and negotiated per row; event-bus subscribers are scoped by contributing authority), then show what breaks when each is dropped.
4. **Scale claims that are load-bearing.** "Design target 80,000" is worthless unless you show what specifically fails at 8,000 and what change made 80,000 possible. Sweep coverage interval versus registry size is the right shape; audit-log growth versus retention is the second. Report the knee, not the headline.
5. **Negative results and operational reality.** Transport mix is the most publishable asset precisely if it is ugly: the fraction of "ONVIF-conformant" cameras that failed RTSP negotiation, the tail reachable only by file drop, the rows that never resolved to a live device. Nobody has published that distribution at this scale. Publish the failures.
6. **Ethics as a design constraint with mechanism.** At TETC, an ethics section citing only Kitchin is a liability. Show subscriber scoping, provenance-derived access, tamper-evident audit as the oversight artefact, and the retention policy that follows from the log-growth measurement. Tie it to fussey2021assisted's finding that discretion migrates to whoever sees the alert.

**Examples that cleared the bar and why.** verma2015borg — one internal deployment, accepted because it published a decade of quantitative operational behaviour, stated the decisions they regretted, and generalised into lessons others could act on. tang2015config — the closest structural template for P6: made provisioning cost a first-class measured property with change-volume and incident data, and articulated a principle separable from Facebook. lu2016optasia and zhang2017videostorm — each reduced a platform design to one falsifiable claim with a measured baseline. cirillo2019fiware — survived because it was tied to a standard and its generality was demonstrated by other people's deployments.

The pattern: **a design principle + a measurement that could have come out the other way + evidence the design outlives the deployment.** P6 has the first and a partial second.

---

## (C) Is "registry rows instead of federation APIs" genuinely distinct?

**No. It is a known pattern with at least four names.**

- **Mediated integration over autonomous sources** (wiederhold1992mediators; lenzerini2002dataintegration): sources are described, not modified; a mediator holds the descriptions. The registry is a mediator catalogue and the rows are source descriptions. Textbook.
- **Pay-as-you-go / dataspace integration** (franklin2005dataspaces): explicitly "admit sources on the strength of metadata, defer integration". Closest match, 21 years old.
- **Catalogue / metadata-only federation**: the OAI-PMH and open-data-portal tradition, and NGSI-LD *context source registration*, which is functionally a registry row.
- **Registry/repository and broker patterns** in enterprise integration and service discovery, and IDS participant/resource descriptions.

**What is genuinely ours, framed correctly:**

1. **The domain is physical, live, and adversarial to metadata.** A camera row makes a claim about a device you do not own, that may be off, moved, re-IP'd or replaced. Dataspaces never had to reconcile descriptors against physical reality. **The sweep coverage interval is exactly this reconciliation and has no analogue in that literature. This is the defensible novel component.**
2. **The unit of contribution is legally, not technically, motivated.** Authorities contribute rows because rows carry no operational obligation and no uptime liability. No published federation design has *the contributor's unwillingness to operate anything* as its primary constraint, with cost evidence for why that constraint binds at 80k scale.
3. **Transport negotiation as the deferred-integration step.** In dataspaces the deferred work is schema mapping; here it is transport and codec negotiation per row, and the resulting transport-mix distribution is new.

**Recommended framing:** do not claim a new integration pattern. Claim that
*descriptor-first federation, long established for data, has not been instantiated
or evaluated for live physical sensor estates under multi-authority ownership*,
name Wiederhold/Lenzerini/Franklin/NGSI-LD in the first three pages, and make the
contribution the reconciliation loop, the cost model, and the transport-mix
evidence. A reviewer who finds Franklin et al. themselves will reject; one who
sees you position against it will not.

---

## (D) Is ACM Computing Surveys achievable?

**As currently described: no, not close.** CSUR does not publish architectures. It
publishes surveys and tutorials whose contribution is a taxonomy plus a
systematic, reproducible synthesis. A layered design for one platform with
measurements from one deployment is the wrong artefact and is desk-rejected on
that basis routinely. Nothing about the quality of the system changes this; it is
a venue-type mismatch.

A CSUR submission would require:

1. **A different paper** — something like *"Federating Heterogeneous Video Surveillance Estates: A Survey of Integration Architectures, Transport Interoperability, and Onboarding Models."* The platform becomes one row in a comparison table and a short case study.
2. **A documented systematic protocol** — search strings, databases, date range, inclusion/exclusion criteria, PRISMA-style flow, typically 150-350 references. We have ~30.
3. **A generative taxonomy**, not a descriptive one: unit of contribution (endpoint / broker / connector / descriptor row); trust assumption (contractual / cryptographic / none); reconciliation model (push / poll / sweep / none); transport negotiation (fixed / negotiated / brokered); accountability substrate (none / append-only / verifiable). Classify every surveyed system and show which cells are empty. **The empty cells are the survey's contribution.**
4. **Coverage across five distinct literatures** — data integration and dataspaces, IoT platforms, edge video analytics, physical-security standards, federated identity, and surveillance governance. A reviewer will check all of them were read properly.
5. **Uniform comparative criteria** across surveyed systems, with explicit "not reported" cells, which are themselves a finding.
6. **No new system.** If our own numbers are the evidence, it is not a survey.

**Recommendation.** Target IEEE TETC (or IEEE TSC, ACM TOIT, or a systems venue
such as Middleware or SEC) with the architecture paper strengthened per (B): one
falsifiable design claim, one external baseline, negative transport-mix results,
and a scale knee. Separately, the survey in (D)(1) is genuinely publishable at
CSUR **and does not exist yet** — xu2023edgesurvey, hu2023edgebased and gong2025cet
all omit cross-authority federation entirely. That gap is real, but it is a second
paper with a different first author's workload, and pretending one submission can
be both is the fastest route to two rejections.
