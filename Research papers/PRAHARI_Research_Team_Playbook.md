# PRAHARI Research Program: Team Composition & Hiring Playbook
## Building the Research Engine for 6 High-Impact Papers

---

## EXECUTIVE SUMMARY

To publish **6 papers (3 Tier-1, 3 Tier-2 venues)** in 18–24 months, assemble **7 FTE across 4 circles**:

| **Circle** | **Headcount** | **Focus** | **Papers Owned** |
|---|---|---|---|
| **A: Vision & AI** | 2.5 | Inference observability, sensor fusion, uncertainty | Papers 1, 2, 5 |
| **B: Systems & Infrastructure** | 2.5 | Resource scheduling, multi-authority design, real-time | Papers 3, 4, 6 |
| **C: Domain & Deployment** | 1.5 | Grounding, operationalization, reproducibility | All (support) |
| **D: Legal & Policy** | 0.5 | Compliance, AI regulation, ethics review | All (advisory) |

---

## CIRCLE A: COMPUTER VISION & AI RESEARCH (2.5 FTE)

### Position A1: **Principal Researcher / Senior Research Scientist** (1.0 FTE)

#### **Role**
- **Primary:** Leads Papers 1 & 2 (provenance-gating, fallback engines)
- **Secondary:** Supervises two graduate researchers; owns experimental rigor
- **Tertiary:** Liaison with Circles B & C on vision-systems integration

#### **Ideal Profile**
- **Background:** PhD in Computer Vision, AI, or related field; 5+ years post-PhD
- **Publication Record:** 
  - ≥3 papers in CVPR / ICCV / NeurIPS (or equivalent)
  - Experience publishing in reliability/uncertainty topics preferred
  - Track record in systems-vision (not just vision theory)
- **Specific Expertise:**
  - Multi-task learning OR uncertainty quantification in neural networks
  - Adversarial robustness (transferable mindset: how to make systems fail gracefully)
  - OR: Real-time computer vision systems (embedded, edge, or server deployments)
- **Mindset:** Obsessed with **observability**. Asks "How do we know if/why this failed?" Questions easy assumptions (e.g., "does every frame need the same algorithm?").
- **Signal Flags:**
  - Has shipped systems (not just papers)
  - Understands deployment constraints (latency, memory, thermal)
  - Comfortable with "imperfect but predictable" as a design goal

#### **What They'll Do (Quarterly Milestones)**
- **Q1:** Formalize provenance-gating problem (Claims 16–18); design experiments
- **Q2:** Write Paper 1 proposal; submit to CVPR
- **Q3:** Run fallback-engine degradation experiments; begin Paper 2 writing
- **Q4:** Paper 2 in submission; mentor team on reproducibility standards

#### **Hiring Channels**
- **Direct Outreach:**
  - Alumni networks (MIT CSAIL, CMU Vision, Stanford AI Lab, UC Berkeley AI)
  - Contact: Colleagues at Meta (Platforms/Computer Vision), Google Research, DeepMind
- **Search Strategy:** Look for **"ex-practitioner academics"** — people who worked at tech companies, then moved to PhD or postdocs
- **Interview Question (Red Flag Test):**
  - "Tell me about a computer vision system you built that failed in production. What surprised you?"
  - Red flag if answer: "We just retrained the model" (no systems thinking)
  - Green flag if: "We discovered the camera angle changed; had to re-label. Led us to design for sensor drift." (observability + pragmatism)

#### **Compensation & Timeline**
- **Level:** Research Scientist / Principal Postdoc (career stage = 3–5 years PhD)
- **Salary Range:** $150–180k USD (+ benefits)
- **Commitment:** 3 years (two paper submission cycles)
- **Recruitment Timeline:** Start outreach Oct 2026; hire by Jan 2027

---

### Position A2: **Postdoctoral Researcher – Fallback Engine Design** (0.75 FTE)

#### **Role**
- **Primary:** Owns Papers 2 (fallback engines, determinism guarantees) + core experiments
- **Secondary:** Contributes to Paper 5 (multi-modal fusion)
- **Tertiary:** Builds code reproducibility infrastructure

#### **Ideal Profile**
- **Background:** PhD in Computer Vision, Machine Learning, or related; 0–3 years post-PhD
- **Publication Record:** 
  - 2–5 publications in peer-reviewed venues
  - At least one systems-oriented paper (deploying models, reproducibility, robustness)
- **Specific Expertise:**
  - Determinism in neural networks (seed management, floating-point reproducibility)
  - OR: Robustness testing (how to make algorithms fail *predictably*)
  - OR: Model serving + inference (TensorFlow Serving, TorchServe, or custom)
  - Bonus: Experience with Tesseract OCR, OpenCV internals
- **Mindset:** Methodical experimenter. Loves reproducibility; writes detailed lab notebooks; version-controls data.
- **Signal Flags:**
  - Has re-run someone else's paper code successfully (and wrote about it)
  - Comfortable with "boring" systems work (determinism proofs, latency benchmarks)
  - Experience debugging ML production systems

#### **What They'll Do**
- **Q1:** Set up determinism test suite (seed variation, FP precision); benchmark primary/secondary engines
- **Q2:** Conduct latency + accuracy profiling; run ablations
- **Q3:** Draft Paper 2 results; iterate on reproducibility kit
- **Q4:** Respond to ICCV reviewers; prepare revision

#### **Hiring Channels**
- **Postdoc Networks:** 
  - CS conferences (CV reps, postdoc workshops)
  - Postdoc-specific job boards (postdocsusa.com, academic networks)
- **Direct Outreach:** 
  - Professors working on determinism (e.g., work on floating-point reproducibility)
  - Former PhD students from reliable ML groups

#### **Compensation**
- **Salary Range:** $70–90k USD
- **Commitment:** 2 years (focuses on Papers 2, 5, then follows up on revisions)
- **Hiring Timeline:** Start Jan 2027; hire by March 2027

---

### Position A3: **Graduate Researcher – Multi-Modal Fusion & Sensor Integration** (0.75 FTE)

#### **Role**
- **Primary:** Owns Paper 5 (cross-modal detection fusion) + experiments
- **Secondary:** Contributes to Claim 24 (region-occupancy analysis)
- **Tertiary:** Maintains PRAHARI multi-task pipeline

#### **Ideal Profile**
- **Background:** MSc/PhD candidate in Computer Vision, AI, or Data Science
- **Publication Record:** 
  - 1–3 publications (internship papers or early PhD work)
  - Strong coursework in probabilistic modeling, Bayesian methods, or multi-task learning
- **Specific Expertise:**
  - Multi-task learning (MTL) in vision (ideally surveillance or detection context)
  - Sensor fusion or information integration
  - Bonus: Familiarity with PyTorch, Lightning, or similar frameworks
  - Bonus: Experience with datasets (COCO, Pascal VOC) or annotation workflows
- **Mindset:** Curious about **why** fusion works (not just "ensemble = better"). Asks good causal questions.
- **Signal Flags:**
  - Has implemented a multi-task learning paper from scratch
  - Written clear code with tests
  - Comfortable with messy real data (not just academic datasets)

#### **What They'll Do**
- **Q1:** Literature review on fusion methods; design Paper 5 dataset protocol
- **Q2:** Implement baselines (naive OR, voting, weighted fusion); run ablations
- **Q3:** Draft Paper 5; conduct sensitivity analysis (collapse window impact)
- **Q4:** Prepare submission; handle reviewers

#### **Hiring Channels**
- **Universities:** Target departments with strong vision labs
  - India: IIT Delhi, IIT Bombay, IIIT Hyderabad (computer vision groups)
  - Global: Stanford, CMU, UC Berkeley, MIT (if open to remote/partial)
- **Internship Path:** Consider offering 3-month internship first; convert to grad hire if strong fit

#### **Compensation**
- **Salary Range:** $30–50k USD (+ tuition if pursuing PhD)
- **Commitment:** 2–3 years
- **Hiring Timeline:** Start March 2027 (later, to allow recruitment flexibility)

---

## CIRCLE B: SYSTEMS & INFRASTRUCTURE RESEARCH (2.5 FTE)

### Position B1: **Senior Systems Researcher** (1.0 FTE)

#### **Role**
- **Primary:** Leads Papers 3, 4, and 6 (decoder management, prediction, multi-authority architecture)
- **Secondary:** Supervises one engineer; owns systems benchmarking
- **Tertiary:** Liaison with Circle C on deployment infrastructure

#### **Ideal Profile**
- **Background:** PhD in Computer Science (systems track); 5+ years post-PhD in academia or industry
- **Publication Record:**
  - 3+ papers in OSDI, SOSP, ATC, VLDB, or equivalent systems venues
  - Experience publishing in real-time systems, databases, or networking
- **Specific Expertise:**
  - Resource scheduling, admission control, or capacity planning (cloud systems, VMs, containers, or embedded)
  - Real-time systems (predictable latency, bounded resources)
  - Distributed systems or multi-node coordination
  - Bonus: Video/media systems (streaming, transcoding, frame processing)
  - Bonus: Knowledge of video codec/container internals (RTSP, HLS, WHEP)
- **Mindset:** Thinks in constraints and tradeoffs. Loves measuring things (latency histograms, resource saturation curves). Skeptical of "works on my machine" claims.
- **Signal Flags:**
  - Has built a system and published an honest "systems paper" (measurements, ablations, lessons learned)
  - Understands the cascade of latency (network → decode → inference → network again)
  - Experience deploying research systems to real hardware

#### **What They'll Do**
- **Q1:** Formalize admission-control problem (Claim 21); design metrics and baselines
- **Q2:** Build decoder latency profiler; design health-probe experiments; submit Paper 4
- **Q3:** Analyze PRAHARI traces to derive transition-frequency model (Paper 3 foundation); submit Paper 3 proposal
- **Q4:** Draft Paper 6 (architecture synthesis); respond to reviewers

#### **Hiring Channels**
- **Direct Outreach:**
  - Alumni networks (UC Berkeley, CMU, MIT, UIUC, Cornell systems programs)
  - Contact: Researchers at AWS, Microsoft Research, Google Cloud, IBM Research
  - Academic systems labs (search "real-time systems lab" or "distributed systems group")
- **Search Strategy:** Look for people who have **published systems papers** (not just papers *about* systems)
- **Interview Question:**
  - "Describe a resource-scheduling problem you solved. What was the unexpected outcome?"
  - Green flag: "We thought we needed dynamic scheduling; turns out static admission with refusal was more predictable."

#### **Compensation & Timeline**
- **Level:** Research Scientist / Senior Postdoc
- **Salary Range:** $150–180k USD
- **Commitment:** 3 years
- **Recruitment Timeline:** Start Oct 2026; hire by Jan 2027

---

### Position B2: **Postdoctoral Researcher – Video Systems & Decoder Management** (0.75 FTE)

#### **Role**
- **Primary:** Owns Paper 4 (concurrent decoder management, admission control)
- **Secondary:** Contributes to Paper 6 (multi-authority platform design)
- **Tertiary:** Instruments PRAHARI for measurement (decoder logs, health probes)

#### **Ideal Profile**
- **Background:** PhD in Systems, Networking, or related; 0–3 years post-PhD
- **Publication Record:**
  - 2–5 systems papers
  - At least one paper involving measurement or benchmarking
- **Specific Expertise:**
  - Video streaming (DASH, HLS, WHEP) or codec internals
  - Profiling and instrumentation of real systems
  - Resource management in real-time or embedded systems
  - Bonus: Experience with OpenCV or FFmpeg
- **Mindset:** Pragmatic experimental builder. Comfortable with hardware; enjoys instrumentation.
- **Signal Flags:**
  - Has built a measurement infrastructure from scratch
  - Published a paper with latency histograms, CDF plots, or tail-latency analysis
  - Comfortable working with code at system calls level (strace, perf, profilers)

#### **What They'll Do**
- **Q1:** Instrument PRAHARI decoders with latency + resource tracing; design benchmarking harness
- **Q2:** Run admission-control experiments (admit, queue, refuse semantics); collect latency curves
- **Q3:** Draft Paper 4 results; run ablations on health-probe hysteresis
- **Q4:** Prepare revision; implement recommendations

#### **Compensation**
- **Salary Range:** $70–90k USD
- **Commitment:** 2 years
- **Hiring Timeline:** Start Jan 2027; hire by March 2027

---

### Position B3: **Systems Engineer – Multi-Authority Platform** (0.75 FTE)

#### **Role**
- **Primary:** Implements multi-authority platform abstraction (Paper 6 foundation); maintains PRAHARI codebase
- **Secondary:** Builds reproducibility & benchmarking infrastructure
- **Tertiary:** Supports Circle A on experiments

#### **Ideal Profile**
- **Background:** BS/MS in Computer Science or related; 2–5 years industry systems experience
- **Technical Skills:**
  - Fluent in Python (PRAHARI stack); comfortable with C/C++ for performance work
  - Databases: SQLite, PostgreSQL; understands schema design for multi-tenant systems
  - Networking: RTSP, HLS, HTTP; protocol implementation comfortable
  - Bonus: Docker, Kubernetes, or container orchestration
- **Mindset:** Pragmatic builder. Cares about code quality (tests, documentation). Bridges research and implementation.
- **Signal Flags:**
  - Has maintained a production system > 1 year
  - Contributed to open-source projects with quality standards
  - Comfortable with "research code → production code" refactoring

#### **What They'll Do**
- **Q1:** Design multi-authority schema extensions; implement registry abstraction layer
- **Q2:** Build benchmarking harness for Papers 4 & 6; instrument PRAHARI
- **Q3:** Prepare datasets & code for publication; create reproducibility docker images
- **Q4:** Support paper revisions; maintain open-source release

#### **Compensation**
- **Salary Range:** $80–110k USD
- **Commitment:** 3 years
- **Hiring Timeline:** Start Dec 2026; hire by Feb 2027

---

## CIRCLE C: DOMAIN & DEPLOYMENT (1.5 FTE)

### Position C1: **Research Scientist – Surveillance Systems & Government Tech** (1.0 FTE)

#### **Role**
- **Primary:** Domain expert and deployment liaison; ensures research grounding and operationalization
- **Secondary:** Contributes to Papers 4, 5, 6 (systems grounding); validates assumptions against real deployment
- **Tertiary:** Co-publishes with Circle A & B; advises on India/government context

#### **Ideal Profile**
- **Background:** 3+ years in CCTV, law enforcement tech, government digitization, or VMS integration
  - Could be former government CTO, VMS integrator, or law enforcement IT specialist
  - PhD not required; deep domain knowledge is the hire criterion
- **Knowledge Areas:**
  - CCTV VMS landscape (Genetec, Milestone, Axis, Hikvision ecosystem understanding)
  - ANPR in real deployment (accuracy realistic expectations, false-positive rates)
  - Government procurement and deployment constraints (India context preferred)
  - Privacy frameworks (GDPR, Indian data protection, consent models)
  - Law enforcement operations (what they actually need vs. what tech demos show)
- **Mindset:** Healthy skepticism. Asks "Would an operator actually use this?" and "What could go wrong?"
- **Signal Flags:**
  - Has deployed or supported a large-scale surveillance system
  - Understands SLAs, reliability requirements, operational support costs
  - Has fought through government procurement processes
  - Knows where research claims diverge from reality

#### **What They'll Do**
- **Q1:** Conduct stakeholder interviews (Gujarat departments, operators); validate problem assumptions for Papers 4, 6
- **Q2:** Help design experiments with real deployment constraints; advise on dataset collection
- **Q3:** Review papers for operationalization feasibility; flag unrealistic claims
- **Q4:** Support reproducibility & deployment validation; serve as domain advisor

#### **Key Responsibility: The "Reality Check"**
- Ensures Papers 1, 2, 4, 6 don't make claims that will embarrass the team in court or with operators
- Translates research insights into deployment language
- Identifies second-order problems (e.g., "admission control + health hysteresis is great, but operators don't know how to tune the three-strike rule")

#### **Compensation & Timeline**
- **Salary Range:** $120–160k USD (senior IC, not junior researcher)
- **Commitment:** 3 years
- **Recruitment Timeline:** Start Oct 2026; hire by Dec 2026
- **Hiring Channels:**
  - Government tech communities (India: Government CIO forums, e-gov conferences)
  - VMS vendor networks (Genetec reseller communities, integrator conferences)
  - Consultancies specializing in government tech (EY Advisory, Deloitte India)
  - Direct outreach: Former CTOs of state police departments, ex-integrators at companies like Wipro/TCS working on CCTV

---

### Position C2: **Full-Stack Engineer – Reproducibility & Deployment** (0.5 FTE)

#### **Role**
- **Primary:** Maintains PRAHARI production/test split; owns reproducibility infrastructure and datasets
- **Secondary:** Supports all circles on experimental harness; builds Docker/notebooks for paper code
- **Tertiary:** Runs live deployments for data collection

#### **Ideal Profile**
- **Background:** BS/MS in CS; 2–4 years industry full-stack engineering
- **Technical Skills:**
  - Python (experiments); JavaScript/React (UI for operators if needed)
  - Linux systems administration; Docker, git, CI/CD pipelines
  - Database operations (SQLite → PostgreSQL migration path)
  - Bonus: Kubernetes or container orchestration
  - Bonus: Experience with data pipelines (DVC, MLflow, or similar)
- **Mindset:** Detail-oriented; obsessed with reproducibility and documentation
- **Signal Flags:**
  - Maintains a public GitHub with clean, documented projects
  - Has written reproducibility instructions that others followed successfully
  - Comfortable supporting researchers (translates wishes into working code)

#### **What They'll Do**
- **Q1:** Version-control PRAHARI codebase; set up reproducibility infrastructure (notebooks, Docker, DVC)
- **Q2:** Instrument data collection from deployments; ensure dataset versioning
- **Q3:** Prepare code & data artifacts for each paper submission
- **Q4:** Manage open-source releases; support reproducibility requests from reviewers

#### **Compensation**
- **Salary Range:** $60–80k USD
- **Commitment:** 3 years
- **Hiring Timeline:** Start Feb 2027 (can start with contractor; convert to hire later)

---

## CIRCLE D: LEGAL & POLICY ADVISORY (0.5 FTE)

### Position D1: **AI Ethics & Regulation Advisor** (0.5 FTE, Advisory)

#### **Role**
- **Primary:** Reviews all papers for overstated claims; ensures no false suggestions (Section 64 concern)
- **Secondary:** Advises on privacy-preserving framing (provenance = privacy tool, not surveillance tool)
- **Tertiary:** Liaison with regulators (if needed) on policy questions

#### **Ideal Profile**
- **Background:** Law degree + AI expertise, or AI PhD + regulatory background; 2+ years in AI policy/ethics
- **Knowledge Areas:**
  - AI regulation (EU GDPR, US AI Bill of Rights, Indian data protection frameworks)
  - Patent law (especially biotechnology/AI claims; understanding Section 64)
  - Privacy-preserving technologies and frameworks
  - Government procurement & public sector tech procurement regulations
- **Mindset:** Cautious but not blocking. Asks "Could this claim be misinterpreted?"
- **Signal Flags:**
  - Has reviewed technical claims in legal/policy contexts before
  - Understands difference between "could be used for" and "is designed for"
  - Comfortable saying "no, don't publish this claim"

#### **What They'll Do**
- **Monthly:** Review paper drafts for compliance; flag problematic claims
- **Quarterly:** Advise on policy positioning; monitor regulatory changes affecting PRAHARI
- **On-demand:** Brief team on legal risks (e.g., if export controls tighten on face recognition)

#### **Engagement Model**
- **0.5 FTE** = ~20 hours/month
- **Contract or Advisory Board seat** (not full-time hire)
- **Compensation:** $80–120k USD/year (or equivalent consulting rate)
- **Hiring Channels:**
  - AI policy organizations (Brookings, Center for Security and Emerging Technology)
  - Law firms specializing in tech/AI
  - Academic researchers in AI ethics (MIT Media Lab, Stanford Internet Observatory, etc.)

---

## HIRING ROADMAP & TIMELINE

### **Phase 1: Recruitment (Oct 2026 – Mar 2027)**

| **Month** | **Position** | **Status** | **Owner** | **Notes** |
|---|---|---|---|---|
| **Oct 2026** | A1 (Principal Researcher) | Outreach begins | Amit/Research Lead | Contact alumni networks |
| **Oct 2026** | B1 (Senior Systems Researcher) | Outreach begins | Amit/Research Lead | Parallel track with A1 |
| **Oct 2026** | C1 (Domain Expert) | Outreach begins | Amit/Domain Lead | Government/VMS networks |
| **Nov 2026** | D1 (Legal Advisor) | Sourcing begins | Amit | Law firm + policy networks |
| **Dec 2026** | A1, B1, C1 | Interviews 1–2 rounds | Amit + hiring panel | Virtual / in-person |
| **Dec 2026** | D1 | Advisory agreement signed | Amit | Contract or retainer |
| **Jan 2027** | A1, B1 | Offers extended | Amit | Expect 4–6 week notice from current roles |
| **Jan 2027** | A2, B2 | Postdoc search begins | A1, B1 | Internal job postings, academic networks |
| **Feb 2027** | A1, B1 | Onboarding begins | Team | Ramp-up on PRAHARI codebase, claims, prior art |
| **Feb 2027** | C1 | Onboarding begins | Amit | Parallel with A1/B1 |
| **Mar 2027** | A2, B2 | Offers extended | A1, B1 | Postdoc recruitment slower (visa timelines) |
| **Mar 2027** | A3, B3 | Grad student / engineer search | A1, B1 | University + internship networks |

### **Phase 2: Ramp-up & Early Papers (Apr 2027 – Jun 2027)**

| **Month** | **Milestone** | **Papers** | **Owner** |
|---|---|---|---|
| **Apr 2027** | A2, B2 onboarded; A3, B3 offers out | — | A1, B1 |
| **Apr 2027** | Literature reviews + problem formulation complete | 1, 2, 4, 6 | All circles |
| **May 2027** | Experiment design approved; infrastructure built | 1, 2, 3, 4 | A, B, C circles |
| **Jun 2027** | Paper proposals drafted for internal review | 1, 2, 3, 4 | Paper owners |

### **Phase 3: Submission Wave 1 (Jul 2027 – Sep 2027)**

| **Month** | **Event** | **Papers** | **Venue Deadline** |
|---|---|---|---|
| **Jul 2027** | Paper 4 submitted | Paper 4 | IEEE Transactions on MM (rolling) |
| **Aug 2027** | Papers 1 & 3 submitted | Papers 1, 3 | CVPR 2028 (Aug 15 deadline) |
| **Sep 2027** | Experiments continue | 2, 5, 6 | — |

### **Phase 4: Revision & Submission Wave 2 (Oct 2027 – Dec 2027)**

| **Month** | **Event** | **Papers** | **Notes** |
|---|---|---|---|
| **Oct 2027** | Paper 4 revision (likely) | Paper 4 | Revise or new reviewer round |
| **Nov 2027** | Paper 2 submitted | Paper 2 | ICCV 2028 (Nov 1 deadline, ~3-month review) |
| **Dec 2027** | Papers 5 & 6 near completion | Papers 5, 6 | Begin finalization |

---

## COMPENSATION SUMMARY

| **Position** | **Level** | **FTE** | **Annual Salary** | **3-Year Total** | **Benefits** |
|---|---|---|---|---|---|
| A1 (Principal Researcher) | Senior/Scientist | 1.0 | $150–180k | $450–540k | Standard (health, 401k, etc.) |
| A2 (Postdoc – Fallback) | Postdoc | 0.75 | $70–90k | $157–202k | Standard + parental leave |
| A3 (Grad – Fusion) | PhD Candidate | 0.75 | $30–50k | $67–112k | Tuition waiver + stipend |
| B1 (Senior Systems) | Senior/Scientist | 1.0 | $150–180k | $450–540k | Standard |
| B2 (Postdoc – Decoders) | Postdoc | 0.75 | $70–90k | $157–202k | Standard + parental leave |
| B3 (Engineer – Platform) | Senior Engineer | 0.75 | $80–110k | $180–247k | Standard |
| C1 (Domain Expert) | Research Scientist | 1.0 | $120–160k | $360–480k | Standard |
| C2 (Engineer – Reproducibility) | Engineer | 0.5 | $60–80k | $90–120k | Standard (can start as contractor) |
| D1 (Legal Advisor) | Advisory | 0.5 | $80–120k/yr | $240–360k | Consulting retainer |
| **TOTAL** | — | **7.0** | **$810–1,050k/yr** | **~$2.2–3.1M** | — |

### **Funding Assumption**
- Assume $870k budget for Year 1 (recruiting, ramp-up, early experiments)
- Year 2: $950k (all team ramped; paper submissions)
- Year 3: $750k (post-submission support; wind-down or transition to production)
- **Total 3-year program cost: ~$2.6M USD**

---

## HIRING DECISION TREES

### **For A1 (Principal Researcher): Red Flags vs. Green Flags**

#### **Red Flags (REJECT)**
- ❌ "I've only published in top venues; I'm not sure about systems work"
- ❌ "I want to publish 10 papers, fast" (wrong mindset for rigor)
- ❌ No published systems work (only theory or simulation)
- ❌ Uncomfortable with deployment realities ("Can't we just retrain?")
- ❌ No track record of mentoring junior researchers

#### **Green Flags (HIRE)**
- ✅ "I ship systems; I've encountered weird edge cases" (+++ for each example)
- ✅ Familiar with CVPR/ICCV submission process; knows reviewer psychology
- ✅ Published at least one "honest" paper (measurements, ablations, things that didn't work)
- ✅ Asks clarifying questions about deployment constraints
- ✅ References mention "great mentor" or "helped me ship"
- ✅ Has worked at companies (Meta, Google, Apple) where systems reasoning matters

---

### **For B1 (Senior Systems Researcher): Red Flags vs. Green Flags**

#### **Red Flags (REJECT)**
- ❌ "I'm great at distributed systems theory" (ask: "Have you built and deployed one?")
- ❌ All papers are modeling/simulation (no real measurements)
- ❌ "Latency is not really that important" (wrong for this program)
- ❌ No experience with real failure modes (only textbook scenarios)
- ❌ Can't explain why their system design matters

#### **Green Flags (HIRE)**
- ✅ "I built a system; here's what surprised us" (every answer should have an anecdote)
- ✅ Latency histograms in papers (CDF plots, tail analysis, p99/p999 breakdowns)
- ✅ Comfortable saying "we trade off X for Y; here's why"
- ✅ Experience with real scale (1000+ nodes or 10B+ events)
- ✅ References from systems leaders (OSDI/SOSP/ATC committees, research leads)
- ✅ Can explain real-world deployment constraints (thermal, power, cost)

---

### **For C1 (Domain Expert): Questions That Matter**

#### **Disqualifying Answers (REJECT)**
- ❌ "CCTV is simple; just use the latest AI model" (lacks deployment experience)
- ❌ "All ANPR systems achieve >99% accuracy" (unrealistic; suggests never deployed)
- ❌ "Privacy is solved by encryption" (oversimplified; suggests policy naiveté)

#### **Ideal Answers (HIRE)**
- ✅ "I've deployed ANPR in {location}. Accuracy was X%, but {failure mode} was bigger problem" (honest, specific)
- ✅ "Government procurement required us to {constraint}; it changed our architecture" (pragmatic, learned lessons)
- ✅ "Operators never use feature X because Y" (user-centric observations)
- ✅ "The regulatory risk is {specific item}; we handle it by {mechanism}" (understands compliance)
- ✅ Can name 3+ CCTV platforms and honestly compare them (not just "Genetec is best")

---

## INTEGRATION PLAYBOOK: HOW CIRCLES INTERACT

### **Weekly Cadence**
- **Monday 9 AM UTC:** Whole-team sync (30 min)
  - Updates from each circle
  - Blockers and asks
- **Wednesday 2 PM UTC:** Circle A sync (Vision team) — 30 min
- **Wednesday 3 PM UTC:** Circle B sync (Systems team) — 30 min
- **Thursday 2 PM UTC:** Joint A+B sync (cross-circle dependencies) — 30 min

### **Critical Handoffs**
1. **Circle A → Circle B:** "Fallback engine experiments ready" → B2 benchmarks latency
2. **Circle B → Circle A:** "Decoder logs available" → A uses real failure traces for Paper 2
3. **Circle C → All:** "Deployment feedback" → Feeds into all papers' assumptions
4. **Circle D → All:** "Claim review complete" → Gate on paper submission

### **Decision Rights**
- **Paper scope:** Paper owner (A1, A2, A3, B1, B2, B3 for their papers)
- **Experiment design:** Co-owned by paper owner + C1 (domain validation)
- **Publication timing:** Paper owner + C1 + D1 (compliance check)
- **Code release:** B3 (engineer) with B1 + C2 sign-off (quality, reproducibility)

---

## ANTI-PATTERNS TO AVOID

1. **"Hire slow, fire fast" becomes "hire never, fire immediately"**
   - *Fix:* Commit to 90-day onboarding; evaluate at 6 months with clear rubric

2. **Too many meetings, no time for research**
   - *Fix:* Strict agenda + time-box all syncs; async updates in shared docs acceptable

3. **Papers don't align with patents; wasted effort**
   - *Fix:* C1 + D1 read every claim before first team meeting

4. **Reproducibility is an afterthought**
   - *Fix:* Require code + data artifacts 4 weeks before submission (not at submission)

5. **Researchers work in silos; duplication**
   - *Fix:* Monthly brown-bag presentations; every researcher presents progress to whole team

6. **Domain expert hired too late; research built on false assumptions**
   - *Fix:* C1 onboards in parallel with A1/B1 (Month 1, not Month 3)

---

## SUCCESS METRICS FOR HIRING TEAM

### **At Month 6 (Jan 2028)**
- [ ] All 6 primary positions hired and onboarded
- [ ] A2, B2 offers accepted and start dates set
- [ ] Papers 1, 2, 3, 4 under review or accepted
- [ ] C1 has conducted ≥3 stakeholder interviews; feedback integrated

### **At Month 12 (Jul 2028)**
- [ ] A2, B2 onboarded and contributing
- [ ] Papers 4, 1, 3 have decisions (accept, reject, or revision)
- [ ] Papers 5, 6 drafts complete; internal review finished
- [ ] Reproducibility kit ready (>80% code + data)

### **At Month 18 (Jan 2029)**
- [ ] Papers 2, 5, 6 decisions received
- [ ] ≥4 papers accepted (across T1/T2 venues)
- [ ] Code + data released (with DOI, reproducible)
- [ ] Team has published 1–2 follow-up position papers or blogs

### **At Month 24 (Jul 2029)**
- [ ] All 6 papers published (or in final revision)
- [ ] ≥3 external research groups have cited PRAHARI papers
- [ ] ≥1 new deployment validates recommendations from Papers 4 & 6
- [ ] Team has presented at ≥3 external venues (CVPR, IJCAI, systems workshops)

---

## FINAL HIRING RECOMMENDATION

**Go forward with 7 FTE across 4 circles. Hire A1 & B1 immediately (Oct 2026). Bring in C1 by Dec 2026.**

The team composition reflects the **three critical competencies** for research at the intersection of vision, systems, and deployment:
1. **Technical depth** (A, B)
2. **Pragmatic grounding** (C)
3. **Compliance rigor** (D)

This balanced approach maximizes chances of **publication impact** AND **practical relevance**—the dual goal for a patent-backed research program.

---

**Prepared by:** Alex Harmozi Framework  
**Date:** September 5, 2026  
**Status:** Ready for Approval
