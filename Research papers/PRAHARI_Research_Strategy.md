# PRAHARI Patent Portfolio → Research Paper Strategy
## Strategic Analysis: Alex Harmozi Framework Applied to Video Surveillance Innovation

**Document Date:** September 5, 2026  
**Patents Analyzed:** 24 claims covering provenance-gated biometric control, multi-authority video management, and federated analytic degradation  
**Research Outcome:** 6 high-impact paper opportunities × 3 venue tiers = Publication roadmap for 18–24 months

---

## PART I: THE CORE INNOVATION AUDIT

### What the Patents Actually Protect (Not What the Actionbook Claimed)

The status document identifies **nine foundational innovations** across three research domains:

#### 1. **Provenance-Gated Biometric Control** (Claims 16–18)
- **What it does:** Strips facial recognition from the permitted engine set before dispatch, based on camera ownership metadata at registration time (not query time)
- **Why it matters:** First architecture known to the research team to decouple enrollment consent from inference permission
- **Analogy:** RBAC for AI models — a camera's "clearance level" determines which neural networks can see its frames
- **Prior art gap:** No prior art found anticipating this mechanism
- **Patent strength:** Independent claims; strong defensibility

#### 2. **Two-Tier Engine Degradation with Provenance Tracking** (Claims 19–20)
- **What it does:** Falls back from a primary engine (YOLO, FaceNet) to a deterministic secondary engine (OpenCV blob + Tesseract) on exception, absence, or empty result, writing provenance into every detection record
- **Why it matters:** First system to make inference-path uncertainty observable; enables operators to distrust and reproducible results
- **Technical novelty:** Fallback is not "try again" — it's a **different algorithm class** with different semantics
- **Dependent on:** Frame-level UUID linking detections to their generating engine
- **Research lever:** Reproducibility, auditability, and degraded-performance prediction

#### 3. **Admission-Controlled Capture with Rotational Coverage** (Claim 21)
- **What it does:** Refuses new decoder sessions when at a concurrency bound; no queue, no eviction, no quality reduction
- **Why it matters:** Inverse of typical resource scheduling. Bounds peak CPU/memory; enables exact capacity planning
- **Metric:** Latency cliff at saturation (vs. traditional graceful degradation curves)
- **Coupled to:** Reachability sweep (Claims 7, 21 steps d–g); three-strike health hysteresis
- **Research lever:** Real-time systems design, predictable performance under load

#### 4. **Entity-Agnostic Event Schema with Cross-Modal Collapse** (Claim 22)
- **What it does:** Detects vehicle, person, region-occupancy with a single 9-field record shape; collapses multi-modal observations (e.g., car detected by ANPR and separately by object detector) into one alert
- **Why it matters:** First generalized schema to handle vehicles, persons, regions without a union type
- **Cross-modal matching:** Same collapse predicate applies to plate match, biometric match, region occupancy
- **Collapse interval:** 120 seconds, tuned to camera FOV depth ÷ permitted speed
- **Research lever:** Information fusion, heterogeneous sensor normalization

#### 5. **Transition-Frequency Next-Camera Prediction** (Claim 23)
- **What it does:** Predicts next-likely camera by frequency distribution of historical plate transitions; falls back to GIS distance when no history
- **Why it matters:** No Kalman filter, no road network, no motion model — topology and transitions **learned from data**
- **Distinguishing insight:** Accurate on irregular routes (godowns, parks, border crossings) where road networks fail
- **Fallback elegance:** Top-3 predicted cameras ranked by probability, with probability = transition count ÷ total
- **Research lever:** Inverse reinforcement learning, implicit motion models from observational data

#### 6. **Region-Occupancy as Zero-Extra-Inference Wrapper** (Claim 24)
- **What it does:** Person-in-ROI detection with zero additional inference cost — filters existing person boxes; computes IoU with a frame region
- **Why it matters:** Adds a new detection type (region-occupancy) without a fourth neural network
- **Semantics:** Same alert predicate matches on region-occupancy entity type; can be correlated with vehicles in the same region
- **ROI encoding:** Fractions [0,1] (normalized) or absolute pixels; embedded in camera registry as extension field
- **Research lever:** Computational efficiency, multi-task learning pipelines

---

## PART II: RESEARCH VENUE STRATEGY

### Tier-1 Venues (High-Impact, Full Conference Cycle: 18 Months)

#### **Paper 1: "Provenance-Aware Inference Dispatch in Federated Computer Vision"**
- **Venue:** CVPR (IEEE/CVF Computer Vision & Pattern Recognition)
- **Research Angle:** 
  - Formalize the **decision tree problem**: Given camera provenance attributes (ownership, certificate status, data-use class), determine reachable inference paths *before* dispatch
  - Extend to multi-attribute case (geographic region, legal jurisdiction, consent class)
  - Provide complexity analysis: O(1) dispatch vs. O(log n) alternative approaches
- **Experimental Setup:**
  - Dataset: 80,000-camera design target case; synthetic 800-camera traced dataset from PRAHARI deployment
  - Baselines: Query-time RBAC, stateless fallback, naive union-type dispatch
  - Metrics: Dispatch latency, false-negative rate (frames wrongly blocked), audit log complexity
  - Ablation: Impact of lazy singleton construction (facial model loaded only when needed)
- **Novel Contribution:** 
  - First to decouple **registration-time provenance** from **inference-time permission**
  - Proof that lazy construction prevents model weights from ever entering memory when no camera reaches permission threshold
- **Timeline:** Proposal submission Q1 2027; presentation June 2027
- **Co-author Profile:**
  - Lead: Computer vision systems researcher with adversarial ML background
  - Co-authors: Privacy-preserving ML specialist, legal AI practitioner

---

#### **Paper 2: "Deterministic Fallback Engines & Reproducible Inference under Model Uncertainty"**
- **Venue:** ICCV (IEEE/CVF International Conf. on Computer Vision)
- **Research Angle:**
  - The **inverse problem** to Paper 1: When a primary engine fails, how do we guarantee that the fallback produces consistent, auditable results?
  - Formalize "engine equivalence under degradation": Both engines emit the same record shape; inference path is explicit and queryable
  - Prove that per-detection provenance enables post-hoc accuracy estimation without ground truth labels
- **Experimental Setup:**
  - Three primary/secondary pairs: (YOLO + OpenCV blob), (FaceNet + histogram), (PaddleOCR + Tesseract)
  - Collected dataset: PRAHARI detections (n=50,000 detections split 60% primary, 40% secondary by random failure injection)
  - Metrics: Accuracy gap between engines, latency ratio, false-positive rate on secondary
  - Reproducibility: Commit determinism proofs (Tesseract seeding, OpenCV algorithm stability)
- **Novel Contribution:**
  - Inference provenance is observable data; can predict secondary-engine accuracy from primary-engine confidence + detection class
  - First quantification of "two-tier systems" from a reliability perspective
- **Timeline:** Proposal Q2 2027; presentation Oct 2027
- **Co-author Profile:**
  - Lead: Uncertainty quantification / reliability researcher (robotics or autonomous systems background)
  - Co-author: Systems researcher (OS, resource scheduling)

---

#### **Paper 3: "Implicit Motion Models from Observational Sensor Data: Next-Camera Prediction without Road Networks"**
- **Venue:** IJCAI (International Joint Conf. on Artificial Intelligence) or AAMAS (Autonomous Agents & Multiagent Systems)
- **Research Angle:**
  - Classical Re-ID uses explicit motion models (Kalman, graph traversal). PRAHARI inverts this: **derive topology from historical transitions**
  - Formalize the problem: Given a set of cameras with unknown connectivity and a stream of plate detections, predict next-camera probability distribution
  - Compare against Kalman, against graph-based methods, against neural Re-ID
- **Experimental Setup:**
  - Synthetic road networks (generated random grids, small-world graphs)
  - Real traces: PRAHARI seeded vehicles (GJ01AB1234 etc.) driven across Valsad to Gandhinagar (320 km corridor)
  - Metrics: Top-1, Top-3 accuracy; robustness to sparse historical data; performance on irregular routes (godowns, border crossings)
  - Ablation: Frequency only vs. frequency + distance; impact of collapse window (120 s) on transition counts
- **Novel Contribution:**
  - Shows that implicit models can outperform road-network models on irregular deployments (→ Indian context)
  - Probabilistic fallback (distance-ranked neighbors) when history is absent
- **Timeline:** Proposal Q2 2027; presentation Aug 2027
- **Co-author Profile:**
  - Lead: AI/ML researcher in graph learning, reinforcement learning, or multi-agent systems
  - Co-author: Operations research / network optimization specialist

---

### Tier-2 Venues (Strong Domain, 12–18 Month Cycle)

#### **Paper 4: "Deterministic Concurrent Decoder Management in Real-Time Video Analytics"**
- **Venue:** IEEE Transactions on Multimedia or ACM Transactions on Multimedia Computing, Communications and Applications
- **Research Angle:**
  - Admission control is well-studied in cloud systems but not in video analytics
  - **Novel semantics:** Refuse without queueing, decoupled from quality reduction
  - Prove that peak resource envelope is independent of estate cardinality (80k cameras, 4 concurrent decoders → bounded CPU)
- **Experimental Setup:**
  - Latency profiling: Admit, refuse, queue, eviction policies under increasing load
  - Dataset: Synthetic camera traces (failure patterns modeled as Poisson), real PRAHARI cameras
  - Metrics: Peak latency, 99th-percentile latency, resource utilization, alert delay
- **Novel Contribution:**
  - First to couple decoder admission control with health-state hysteresis (three-strike rule)
  - Proves refusal-semantics bound achieves predictable alerting latency
- **Timeline:** Proposal Q1 2027; acceptance/revision cycle Q4 2027
- **Co-author Profile:**
  - Lead: Systems researcher (real-time systems, resource scheduling, embedded systems)
  - Co-authors: Networking specialist, database performance researcher

---

#### **Paper 5: "Cross-Modal Detection Fusion and Multi-Analytics Alert Deduplication"**
- **Venue:** IEEE Transactions on Circuits and Systems for Video Technology or Image and Vision Computing
- **Research Angle:**
  - Sensor fusion typically assumes calibrated multi-modal streams. PRAHARI fuses:
    - ANPR (character sequence) + object detection (bounding box) + occupancy (region) with **different confidence models**
  - Formalize collapse predicate: Plate match vs. biometric match vs. region occupancy, all within 120 s
  - Prove optimality of collapse window (tuned to camera FOV / speed)
- **Experimental Setup:**
  - Dataset: 50,000 detections from PRAHARI; synthetic dual-tagged frames (ANPR + object)
  - Baseline: Naive OR fusion (any match triggers alert), voting, weighted confidence
  - Metrics: Alert-fatigue reduction (%)，false-positive rate, missed-detections, latency
  - Ablation: Impact of 120 s window; sensitivity to camera speed assumptions
- **Novel Contribution:**
  - Shows that entity-agnostic schema (vehicle/person/region with same record shape) reduces implementation complexity while maintaining fusion accuracy
  - Derives optimal collapse window from first principles (FOV depth and speed limit)
- **Timeline:** Proposal Q2 2027; acceptance Q1 2028
- **Co-author Profile:**
  - Lead: Computer vision researcher (multi-task learning, sensor fusion)
  - Co-author: Probabilistic modeling / Bayesian methods specialist

---

#### **Paper 6: "Platform Design for Heterogeneous Video Analytics Across Multi-Authority Deployments"**
- **Venue:** IEEE Transactions on Emerging Topics in Computing or ACM Computing Surveys
- **Research Angle:**
  - Systems/architectural paper: Vendor-neutral design for federating independent CCTV estates
  - **Provenance model** as first-class abstraction
  - Transport protocol negotiation (RTSP/TCP, HLS, WHEP, file)
  - Health probing and coverage reporting at scale (80k design target)
- **Experimental Setup:**
  - Measured deployment: PRAHARI seeded registry + live catalogue sync
  - Synthetic scale-out: Trace replay to 80,000 cameras
  - Metrics: Onboarding latency (CSV, form, REST), system latency under load, audit log size
  - Usability: Time to operationalize a new camera / authority
- **Novel Contribution:**
  - First end-to-end architecture for **multi-authority video management without federation APIs**
  - Shows that layered abstraction (registry → ingest → analytics → event bus) generalizes to vendor mix
- **Timeline:** Proposal Q3 2027; acceptance/revision Q2 2028
- **Co-author Profile:**
  - Lead: Systems/software architecture researcher
  - Co-authors: Database specialist (schemas, scale-out), networking/protocols researcher

---

### Tier-3 Venues (Specialized, Fast Track: 6–12 Months)

#### **Workshops & Fast-Track Venues (Not full conference cycle)**
1. **IEEE/CVF Workshop on Surveillance & Detection (CVPR satellite)**
   - Topic: Audit trails for AI-generated detections
   - Fast-track; acceptance rates higher

2. **ACM International Conference on Distributed Computing (ICDCS) applications track**
   - Topic: Geo-distributed enforcement of computer vision policies

3. **IEEE Transactions on Vehicular Technology (vehicle Re-ID angle)**
   - Topic: Plate-based cross-camera tracking without road network assumptions

---

## PART III: TEAM COMPOSITION FRAMEWORK

### The "Three-Circle" Model for Research Excellence

Drawing on the principle of **intersection research** (where innovations from different domains collide), I recommend organizing the team around three overlapping circles:

### **Circle A: Computer Vision & AI** (Lead: 1 researcher, Supporting: 2)
**Who:** PhD-level specialists in surveillance, multi-task learning, uncertainty quantification
**Why:** Papers 1, 2, 5 originate here
- **Lead hire (Level: Principal/Senior Postdoc):**
  - 5+ years in CVPR/ICCV publications
  - Background: Adversarial robustness OR multi-task learning OR uncertainty in vision models
  - Obsession: How to make AI inference observable and auditable
  - *Example profile:* Former Meta/Google research engineer; has shipped federated vision systems
  
- **Supporting researchers (2 × Grad student / Postdoc):**
  - One focused on **fallback engine design** (determinism guarantees, latency profiling)
  - One focused on **sensor fusion** (ANPR ∪ object ∪ occupancy as information products)

**Key Responsibility:** Papers 1, 2, 5 + experimental validation

---

### **Circle B: Systems & Infrastructure** (Lead: 1 researcher, Supporting: 2)
**Who:** Systems researchers with real-time, distributed systems, or databases background
**Why:** Papers 3, 4, 6 originate here
- **Lead hire (Level: Senior researcher / Research scientist):**
  - 5+ years in systems conferences (OSDI, SOSP, ATC, VLDB)
  - Background: Resource scheduling, real-time systems, OR databases at scale
  - Obsession: How to bound latency and resource consumption in unpredictable environments
  - *Example profile:* Former Bell Labs or CMU Systems Group; understands concurrency bounds
  
- **Supporting researchers (2 × Grad student / Software engineer):**
  - One focused on **decoder management & reachability probing** (Claims 7, 21)
  - One focused on **multi-authority onboarding** (registry schema, protocol negotiation, health reporting)

**Key Responsibility:** Papers 3, 4, 6 + systems benchmarking

---

### **Circle C: Domain & Deployment** (Lead: 1 researcher, Supporting: 1 engineer)
**Who:** Practitioners with surveillance or government deployment experience
**Why:** Grounding; ensures research answers real problems
- **Lead hire (Level: Research scientist or domain expert):**
  - 3+ years in CCTV, law enforcement operations, or government digitization projects
  - Background: Video management systems, ANPR in real deployment, privacy/compliance frameworks
  - Obsession: What does operationalization actually require? (Hint: not what researchers assume)
  - *Example profile:* Former government CTO or VMS integrator; knows Gujarat context is advantage
  
- **Supporting engineer (1 × Full-stack engineer):**
  - Builds the reference implementation; maintains PRAHARI codebase for experiments
  - Runs deployments to collect measured traces (seeded registry, catalogue sync)
  - Ensures papers are **reproducible with code release**

**Key Responsibility:** Ground truth; experimental datasets; operationalization validation

---

### **Circle D: Legal & Policy** (Advisory, 0.5 FTE)
**Who:** Privacy/AI regulation expert (part-time advisor or close collaborator)
**Why:** Papers must address Section 64(1)(j) concern (false suggestion claims)
- **Role:**
  - Reviews every claim in every paper to ensure no accuracy / performance claims exceed measured evidence
  - Advises on regulatory positioning (Indian demographics concern, consent models)
  - Contributes to Paper 1 (provenance as legal-compliance mechanism)

---

## PART IV: PUBLICATION ROADMAP (18–24 Months)

### **Phase 1: Foundation Papers (Months 1–6)**

| **Month** | **Paper** | **Venue** | **Status** | **Owner Circle** | **Key Dependency** |
|-----------|-----------|----------|-----------|-----------------|-------------------|
| M1–M3 | Paper 4 (Decoder Mgmt) | IEEE Trans. MM | Proposal/writing | B | PRAHARI code stable |
| M1–M4 | Paper 1 (Provenance) | CVPR | Writing / Internal review | A | Papers 2 & 3 experiments |
| M2–M5 | Paper 3 (Implicit Models) | IJCAI / AAMAS | Proposal | A+B | Real traces from PRAHARI |

**Milestone:** Three proposals submitted; begin experimental validation.

---

### **Phase 2: Validation & Scale (Months 6–12)**

| **Month** | **Paper** | **Venue** | **Status** | **Owner Circle** | **Blocker** |
|-----------|-----------|----------|-----------|-----------------|-----------|
| M6–M8 | Paper 2 (Fallback Engines) | ICCV | Proposal / Experiments | A | Determinism proofs done |
| M6–M9 | Paper 5 (Multi-Modal Fusion) | IEEE Trans. CSVT | Writing / Rebuttal prep | A | Dataset labeling complete |
| M7–M10 | Paper 4 | IEEE Trans. MM | Revision / Camera-ready | B | Reviewer revisions |

**Milestone:** Three papers under review; experimental infrastructure mature.

---

### **Phase 3: Impact & Systems (Months 12–18)**

| **Month** | **Paper** | **Venue** | **Status** | **Owner Circle** | **Acceptance Likely?** |
|-----------|-----------|----------|-----------|-----------------|----------------------|
| M10–M12 | Paper 1 | CVPR | Decision / Camera-ready | A | High (novel + no prior art) |
| M11–M13 | Paper 3 | IJCAI | Decision / Camera-ready | A+B | High (inverse framing novel) |
| M12–M15 | Paper 6 (Architecture) | IEEE Trans. Emerging | Writing | B | Systems maturity |

**Milestone:** First acceptances; prepare workshop presentations.

---

### **Phase 4: Polish & Dissemination (Months 15–24)**

| **Month** | **Activity** | **Target** | **Amplification** |
|-----------|------------|----------|-----------------|
| M15–M18 | Paper 6 revision | IEEE Trans. Emerging | Systems community |
| M18–M21 | Workshop papers | CVPR/ICCV satellites | Practitioner reach |
| M21–M24 | Patent-to-research bridge | IEEE/ACM blogs | Policy influencers |

**Milestone:** 6 papers published across T1/T2 venues; reference implementation open-sourced with reproducibility kit.

---

## PART V: SUCCESS METRICS & GATE CRITERIA

### **Per-Paper Success (Minimum Threshold)**

1. **Acceptance Rate:** Tier-1 venues aim for top-tier (CVPR/ICCV acceptance ~20–25%). Tier-2 aim for acceptance + desk rejection rejection rate <20%.
2. **Reproducibility:** Code release within 30 days of acceptance. Datasets published (anonymized where needed).
3. **Citations:** Target 5+ citations per Tier-1 paper within 18 months of publication (video surveillance community has active researchers).
4. **Practitioner Impact:** At least one follow-up deployment or integrator using published techniques.

### **Portfolio Success (Cumulative)**

- **6 papers published** across 5 different venues within 24 months
- **2 workshops/short papers** at satellite venues
- **1 systems deployment** validating Papers 4 & 6 recommendations
- **3+ collaborations** initiated with other research groups (universities, other VMS vendors)
- **Patent strengthening:** 2–3 additional continuation patents filed from research insights

---

## PART VI: BUDGET & RESOURCE ALLOCATION

### **Year 1 Budget Estimate (USD)**

| **Category** | **Cost** | **Notes** |
|---|---|---|
| **Salaries (3 years commitment)** | $600k | Principal researcher: $150k; 2 postdocs/grads: $100k each; domain expert: $120k; engineer: $80k |
| **Computing & Infrastructure** | $80k | GPUs for fallback engine validation; high-memory workstations; cloud burst compute |
| **Data Collection & Annotation** | $40k | PRAHARI deployment instrumentation; dataset labeling (100k detections) |
| **Conference Travel & Fees** | $60k | 6 papers × $10k (fees, flights, accommodations) |
| **Contingency (15%)** | $90k | |
| **TOTAL Y1** | **$870k** | Y2–Y3 reduced proportionally; Y3 focused on dissemination |

### **Resource Allocation Across Circles**

| **Circle** | **FTE** | **Primary Focus** |
|---|---|---|
| A (Vision) | 2.5 | Papers 1, 2, 5 + experiments |
| B (Systems) | 2.5 | Papers 3, 4, 6 + benchmarking |
| C (Domain) | 1.5 | Grounding + PRAHARI maintenance |
| D (Legal) | 0.5 | Compliance review (advisory) |
| **Total** | **7** | |

---

## PART VII: STRATEGIC POSITIONING

### **Why This Research Matters (Beyond Patents)**

1. **Privacy-by-Architecture:** Provenance-gating (Paper 1) is a model for **architecture-level privacy enforcement**, not post-hoc audit. This resonates with:
   - EU GDPR implementations (automated decision-making transparency)
   - US AI Bill of Rights (algorithmic accountability)
   - Indian data protection frameworks (upcoming)

2. **Operational Safety:** Deterministic fallback engines (Paper 2) + admission control (Paper 4) address a gap in **autonomous system reliability**. Academic venue: robotics + real-time communities.

3. **Data Efficiency:** Implicit motion models (Paper 3) + zero-cost occupancy (Claims 24 / Paper 5) show how **resource-constrained deployments** can achieve results comparable to GPU-heavy baselines. This opens markets in tier-2/tier-3 cities globally.

4. **Horizontal Stack:** The platform paper (Paper 6) positions PRAHARI as a **reference architecture for multi-authority video platforms**. Cities, states, and large enterprises will reuse this pattern.

---

## PART VIII: RISKS & MITIGATION

### **Risk 1: "Prior Art Invalidates Novelty"**
- **Mitigation:** Begin with **freedom-to-operate search** (FTO analysis) in Tier-1 venues. Claim 23 (transition prediction) may have overlap with Re-ID literature; differentiate on "no road network" angle.
- **Action:** Assign Circle A lead to conduct exhaustive literature search in Q1 2027.

### **Risk 2: "Reproducibility Issues Kill Acceptance"**
- **Mitigation:** Begin experiments **now**, not at submission time. Use PRAHARI codebase as ground truth; archive datasets and random seeds with every result.
- **Action:** Assign Circle C engineer to build reproducibility kit (Docker, notebooks, traces) in parallel with writing.

### **Risk 3: "Multi-Author Coordination Delays Papers"**
- **Mitigation:** Establish **weekly sync meetings** per paper (30 min). Use shared Google Docs with version control. Assign one "paper owner" per submission with veto authority over scope creep.
- **Action:** Project manager or Circle lead owns timeline.

### **Risk 4: "Regulatory Changes Invalidate Claims"**
- **Mitigation:** Monitor Indian data protection policy (Advisory Circle D role). If Section 64(1)(j) tightens, pivot Papers 1 & 2 to "privacy by design" framing, not "inference observability."
- **Action:** Quarterly compliance review meetings.

---

## PART IX: GO-TO-MARKET FOR RESEARCH INSIGHTS

### **Pathways to Influence Beyond Publications**

1. **Standards Bodies:** Present Claim 1 (multi-authority CCTV architecture) to ISO/IEC standards working groups (video surveillance).
2. **Government**: Brief state/central IT departments on Papers 4 & 6 (how to scale video analytics within budget).
3. **Industry Partnerships:** Co-publish with VMS vendors (Genetec, Milestone) on platform interoperability (Paper 6).
4. **Open Source:** Release PRAHARI reference implementation after first paper acceptances → GitHub credibility.

---

## RECOMMENDATIONS (Harmozi-Framed)

### **The Leverage Point**

PRAHARI solves a **specific, large, measurable problem:**
- **Customer:** Gujarat (80k design target cameras), tier-2 cities across India, emerging markets
- **Problem:** CCTV estates are fragmented; watchlists exist but are unused; no statewide view
- **Solution:** Federated intelligence plane without rip-and-replace

### **The Research Multiplier**

Publishing 6 papers (T1 venues) does three things:
1. **Validates the architecture** (reduces risk for further deployments)
2. **Attracts partnerships** (academic credibility → industry collaborations)
3. **Protects IP** (publications + patents = comprehensive moat)

### **The Recommended Path**

1. **Hire the three circles immediately** (6 months for recruitment + onboarding)
2. **Run Papers 4 & 1 in parallel** (shortest path to acceptance; both solid technically)
3. **Collect PRAHARI deployment data** starting Month 1 (Papers 3, 5, 6 depend on real traces)
4. **Gate each paper submission** on reproducibility (code + data published before submission)
5. **Plan for 18-month publication cycle**, not 12 (realistic for Tier-1 venues; mitigates rejection risk)

---

## APPENDIX A: Author Pool & Recommended Outreach

### **Tier-1 Researchers to Engage (Co-author Prospects)**

#### **Circle A (Vision)**
- **Prof. Kaiming He** (Meta AI) — Fallback engine design; reproducibility angle
- **Prof. Li Fei-Fei** (Stanford) — Multi-task learning for surveillance; policy connections
- **Prof. Silvio Savarese** (Stanford) — Scene understanding; prediction angle
- **Dr. Xiaofeng Liu** (University of Oulu) — Surveillance video analysis; robust detection
- **Prof. Jiasen Lu** (Georgia Tech) — Multi-modal fusion; reasoning under uncertainty

#### **Circle B (Systems)**
- **Prof. Matei Zaharia** (UC Berkeley) — Resource scheduling; real-time analytics
- **Prof. Andrew Pavlo** (CMU) — Database systems; scale-out design
- **Prof. Peter Bailis** (Stanford) — Distributed systems; latency bounds
- **Dr. Michael Kaminsky** (Intel Labs) — Systems for computer vision; scale
- **Prof. Christos Karamanolis** (IBM Research) — Performance modeling

#### **Circle C (Domain)**
- **Dr. Ramachandra Kota** (Microsoft Research India) — Government digitization; India context
- **Prof. Ponnurangam Kumaraguru** (IIIT Delhi) — Privacy, surveillance, India policy
- **Dario Amodei** — AI safety; deployment rigor (advisory)

### **Venue Editorial Contacts**

- **CVPR Program Chair:** Reach out Q4 2026 for feedback on Paper 1 scope
- **ICCV Program Chair:** Similar outreach Q1 2027 for Paper 2
- **IEEE Trans. MM Editor:** Reach out Q4 2026 with paper outline for Paper 4 (journal prefers early feedback)

---

## APPENDIX B: Comparison Matrix (This Strategy vs. Alternatives)

| **Strategy** | **Timeline** | **Risk** | **Impact** | **Recommended?** |
|---|---|---|---|---|
| **Recommended (6 papers, T1/T2)** | 18–24 mo | Medium | High (cross-domain reach) | ✅ YES |
| Fewer, deeper papers (3 papers, all CVPR) | 24–36 mo | Low | High (narrow credibility) | ⚠️ Maybe (if team small) |
| Workshop-first strategy (workshops → conferences) | 12–18 mo | Low | Medium (incremental build) | ⚠️ Maybe (slower start) |
| Patent-only, no publications | 0 mo | Low | Very Low (no credibility, slower licensing) | ❌ NO |

---

## FINAL RECOMMENDATION

**Go with the recommended strategy: 6 papers, 3 circles, 18-month horizon.**

The patents are strong; the research insights are genuinely novel. The combination of tight integration with deployment data + systems rigor + policy awareness positions PRAHARI as a **reference architecture**, not a one-off system.

Hire the teams. Run the experiments. Publish the results. The market will follow.

---

**Prepared by:** Alex Harmozi Framework for Research ROI  
**Date:** September 5, 2026
