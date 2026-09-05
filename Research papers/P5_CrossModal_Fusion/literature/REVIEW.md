I have enough verified material. Here is the review.

---

# PRIOR-ART REVIEW — Paper 5: Cross-Modal Detection Fusion and Multi-Analytics Alert Deduplication

**Verification note:** every DOI below was resolved through the Crossref REST API or the publisher/USENIX/IETF landing page. I **dropped 3 candidates** I could not verify to my own standard: (i) the *Computers & Chemical Engineering* 2014 paper "An online method to remove chattering and repeating alarms based on alarm durations and intervals" (PII S0098135414000994 exists on ScienceDirect but Crossref would not return its DOI/authors for me, and ScienceDirect blocks fetch); (ii) "Heterogeneous Information Fusion and Visualization for a Large-Scale Intelligent Video Surveillance System" (found only on ResearchGate, no verifiable DOI record); (iii) Carbone et al., "Apache Flink" (IEEE Data Eng. Bull. 2015 — no DOI exists, and I did not want an unverifiable URL-only entry when Akidau et al. covers session windows better). Nothing below is reconstructed from memory alone.

**35 verified entries + 4 clearly-marked non-paper references.**

---

## Axis 1 — Alert fatigue, alarm flood, alarm management

**[tariq2025alertfatigue]** *Alert Fatigue in Security Operations Centres: Research Challenges and Opportunities.* Shahroz Tariq, Mohan Baruwal Chhetri, Surya Nepal, et al. 2025. ACM Computing Surveys (CSUR) 57(9):1–38. DOI 10.1145/3723158.
Systematic survey defining alert fatigue as a measurable socio-technical failure mode and cataloguing mitigation families (reduction, prioritisation, correlation, automation).
*Difference:* Paper 5 is a deployed video-analytics system with a single collapse predicate and measured incident recall, not a survey of cyber-alert mitigations. **Axis 1.**

**[alahmadi2022falsepositives]** *99% False Positives: A Qualitative Study of SOC Analysts' Perspectives on Security Alarms.* Bushra A. Alahmadi, Louise Axon, Ivan Martinovic. 2022. 31st USENIX Security Symposium (USENIX Security '22). https://www.usenix.org/conference/usenixsecurity22/presentation/alahmadi (no DOI assigned).
Interview study of 21 SOC analysts quantifying the perceived false-positive burden and showing that alert volume, not detector accuracy alone, drives analyst attrition.
*Difference:* Paper 5 supplies the quantitative reduction/recall trade-off curve that this qualitative work motivates, in a police video-surveillance rather than SOC setting. **Axis 1, 7.**

**[sundaramurthy2015burnout]** *A Human Capital Model for Mitigating Security Analyst Burnout.* Sathya Chandran Sundaramurthy, Alexandru G. Bardas, Jacob Case, et al. 2015. Eleventh Symposium on Usable Privacy and Security (SOUPS 2015). https://www.usenix.org/conference/soups2015/proceedings/presentation/sundaramurthy (no DOI assigned).
Multi-year anthropological field study of SOCs producing a human-capital model of analyst burnout under sustained alert load.
*Difference:* Paper 5 measures operator-facing alert counts as a system output rather than studying operators; it offers no human-factors instrument. **Axis 1, 7.**

**[wang2016alarmoverview]** *An Overview of Industrial Alarm Systems: Main Causes for Alarm Overloading, Research Status, and Open Problems.* Jiandong Wang, Fan Yang, Tongwen Chen, Sirish L. Shah. 2016. IEEE Transactions on Automation Science and Engineering (T-ASE) 13(2):1045–1061. DOI 10.1109/TASE.2015.2464234.
Canonical review of alarm overloading causes and of the four standard suppression primitives — thresholds, deadbands, delay timers, and filtering — with their design criteria.
*Difference:* Paper 5's collapse predicate is a cross-modal entity-keyed deduplication rather than a univariate signal-conditioning primitive, and it operates on discrete detection events with no underlying continuous process variable. **Axis 1, 6.**

**[kondaveeti2012graphical]** *Graphical Tools for Routine Assessment of Industrial Alarm Systems.* Sandeep R. Kondaveeti, Iman Izadi, Sirish L. Shah, Tim Black, Tongwen Chen. 2012. Computers & Chemical Engineering (CACE) 46:39–47. DOI 10.1016/j.compchemeng.2012.06.042.
Introduces high-density alarm plots, alarm-similarity colour maps and run-length based visual diagnostics for routine alarm-system performance assessment.
*Difference:* Paper 5 reports a single-parameter reduction curve rather than a diagnostic visual toolkit, and its similarity notion is entity identity, not signal correlation. **Axis 1, 7.**

**[isa182]** *(NON-PAPER — STANDARD)* ANSI/ISA-18.2-2016, *Management of Alarm Systems for the Process Industries.* International Society of Automation, Research Triangle Park, NC, 2016. https://www.isa.org/standards-and-publications/isa-standards
Defines the alarm-management lifecycle, rationalisation, and the on-delay/off-delay timer and deadband suppression mechanisms plus performance-metric reporting.
*Difference:* Paper 5 provides an empirical basis for a suppression-window value in video analytics, a domain ISA-18.2 does not cover. **Axis 1, 6, 7.**

**[eemua191]** *(NON-PAPER — GUIDE)* EEMUA Publication 191, *Alarm Systems: A Guide to Design, Management and Procurement.* Engineering Equipment and Materials Users' Association, London. (Widely cited 3rd edition, 2013; a later edition exists — **verify the edition/year against a copy before citing**, I could not confirm it from an authoritative page.) https://www.eemua.org/products/publications/print/eemua-publication-191
Source of the industry operator-load targets (steady-state ~1 alarm per 10 minutes per operator; alarm flood defined as >10 alarms per 10 minutes per operator).
*Difference:* Paper 5 should use these as the external yardstick for its "alert fatigue reduction" claim rather than as a derivation of W. **Axis 1, 7.**

---

## Axis 2 — Event correlation and alert aggregation in intrusion detection

**[valdes2001probabilistic]** *Probabilistic Alert Correlation.* Alfonso Valdes, Keith Skinner. 2001. Recent Advances in Intrusion Detection (RAID 2001), LNCS 2212, pp. 54–68. Springer. DOI 10.1007/3-540-45474-8_4.
Fuses heterogeneous sensor alerts into meta-alerts using a similarity metric over a common alert attribute set with per-attribute expectation of similarity and a *minimum-similarity* fusion threshold.
*Difference:* Paper 5 replaces a tunable multi-attribute similarity score with one hard predicate (same camera ∧ same resolved entity ∧ Δt ≤ W); this is simpler and auditable but strictly less expressive. **Axis 2, 3.**

**[julisch2003clustering]** *Clustering Intrusion Detection Alarms to Support Root Cause Analysis.* Klaus Julisch. 2003. ACM Transactions on Information and System Security (TISSEC) 6(4):443–471. DOI 10.1145/950191.950192.
Attribute-oriented-induction clustering of alarms to find root causes, reporting roughly 87% alarm-load reduction on real IDS data.
*Difference:* Julisch reduces load by removing recurrent benign root causes offline; Paper 5 deduplicates online per incident and claims full incident recall, a stronger and more falsifiable guarantee. **Axis 2.**

**[debar2001aggregation]** *Aggregation and Correlation of Intrusion-Detection Alerts.* Hervé Debar, Andreas Wespi. 2001. Recent Advances in Intrusion Detection (RAID 2001), LNCS 2212, pp. 85–103. Springer. DOI 10.1007/3-540-45474-8_6.
Defines duplicate and consequence relations over a normalised alert schema and aggregates alerts into situations using explicit time windows.
*Difference:* This is the closest structural ancestor of Paper 5's collapse predicate; Paper 5's contribution must be the cross-modal entity resolution and the empirical window study, not the aggregation concept. **Axis 2, 4.**

**[ning2002constructing]** *Constructing Attack Scenarios through Correlation of Intrusion Alerts.* Peng Ning, Yun Cui, Douglas S. Reeves. 2002. Proc. 9th ACM Conference on Computer and Communications Security (CCS '02), pp. 245–254. DOI 10.1145/586110.586144.
Correlates alerts via prerequisite/consequence hyper-alert matching to reconstruct multi-step attack scenarios.
*Difference:* Paper 5 does not model causal chains; it collapses co-referent observations of the same entity, which is association, not scenario reconstruction. **Axis 2.**

**[salah2013modelbased]** *A Model-Based Survey of Alert Correlation Techniques.* Saeed Salah, Gabriel Macía-Fernández, Jesús E. Díaz-Verdejo. 2013. Computer Networks 57(5):1289–1317. DOI 10.1016/j.comnet.2012.10.022.
Taxonomy of alert correlation architectures separating normalisation, aggregation/fusion, and correlation stages.
*Difference:* Paper 5 instantiates exactly the normalise→fuse pipeline this survey describes, in video analytics; the survey's existence is why the pipeline itself cannot be claimed as novel. **Axis 2, 3.**

**[idmef2007]** *(NON-PAPER — IETF RFC)* *The Intrusion Detection Message Exchange Format (IDMEF).* Hervé Debar, David A. Curry, Benjamin S. Feinstein. 2007. RFC 4765, IETF. DOI 10.17487/RFC4765. https://www.rfc-editor.org/rfc/rfc4765.html
Standardises a single detector-agnostic alert record (source, target, classification, time, analyzer, confidence) so alerts from unrelated sensors are directly comparable.
*Difference:* This is prior art *against* Paper 5's schema claim — see section (C). **Axis 2, 3.**

---

## Axis 3 — Multi-sensor / multi-modal information fusion

**[steinberg1999jdl]** *Revisions to the JDL Data Fusion Model.* Alan N. Steinberg, Christopher L. Bowman, Franklin E. White. 1999. Proc. SPIE 3719, *Sensor Fusion: Architectures, Algorithms, and Applications III*, pp. 430–441. DOI 10.1117/12.341367.
The canonical fusion-level model; Level 0/1 explicitly require *common referencing* and normalisation of heterogeneous sensor reports before object refinement and data association.
*Difference:* Paper 5 is a JDL Level-1 instantiation for three video analytics; framing it as such is more honest than claiming the entity-agnostic record as new. **Axis 3.**

**[hall1997introduction]** *An Introduction to Multisensor Data Fusion.* David L. Hall, James Llinas. 1997. Proceedings of the IEEE 85(1):6–23. DOI 10.1109/5.554205.
Tutorial covering data association, gating, and identity fusion across dissimilar sensors.
*Difference:* Paper 5 uses identity keys (plate string, face ID) rather than kinematic gating, so association is exact rather than probabilistic. **Axis 3.**

**[khaleghi2013multisensor]** *Multisensor Data Fusion: A Review of the State-of-the-Art.* Bahador Khaleghi, Alaa Khamis, Fakhreddine O. Karray, Saiedeh N. Razavi. 2013. Information Fusion 14(1):28–44. DOI 10.1016/j.inffus.2011.08.001.
Review organised by data imperfection (uncertainty, ambiguity, conflict, correlation) rather than by sensor type.
*Difference:* Paper 5 assumes near-certain identity resolution and therefore sidesteps the conflict-management machinery this review centres on — a limitation worth stating. **Axis 3.**

**[dempster1967upper]** *Upper and Lower Probabilities Induced by a Multivalued Mapping.* Arthur P. Dempster. 1967. The Annals of Mathematical Statistics 38(2):325–339. DOI 10.1214/aoms/1177698950.
Foundation of Dempster-Shafer belief-function fusion for evidence from sources with differing frames of discernment.
*Difference:* Paper 5's collapse is Boolean and evidence-free; it does not combine detector confidences, which a reviewer may ask about. **Axis 3.**

**[barshalom1981tracktotrack]** *On the Track-to-Track Correlation Problem.* Yaakov Bar-Shalom. 1981. IEEE Transactions on Automatic Control (TAC) 26(2):571–572. DOI 10.1109/TAC.1981.1102635.
Derives the correlated-error track-to-track association test — a chi-square hypothesis test whose gate is set from a chosen significance level, not from geometry.
*Difference:* Paper 5 uses a fixed time gate; Bar-Shalom's precedent is precisely that association gates should come from a stated error model and false-association rate. **Axis 3, 4.**

---

## Axis 4 — Data association, deduplication, and temporal windowing

**[fellegi1969theory]** *A Theory for Record Linkage.* Ivan P. Fellegi, Alan B. Sunter. 1969. Journal of the American Statistical Association (JASA) 64(328):1183–1210. DOI 10.1080/01621459.1969.10501049.
The decision-theoretic foundation of record linkage: a likelihood-ratio score with two thresholds chosen to bound Type I and Type II linkage error rates.
*Difference:* Paper 5's linkage is deterministic on a key; but Fellegi–Sunter establishes the norm that a matching threshold is justified by *stated error rates*, which is what Paper 5's geometric derivation fails to do. **Axis 4.**

**[elmagarmid2007duplicate]** *Duplicate Record Detection: A Survey.* Ahmed K. Elmagarmid, Panagiotis G. Ipeirotis, Vassilios S. Verykios. 2007. IEEE Transactions on Knowledge and Data Engineering (TKDE) 19(1):1–16. DOI 10.1109/TKDE.2007.250581.
Surveys similarity metrics, blocking/windowing, and threshold selection for duplicate detection.
*Difference:* Paper 5's "blocking key" is (camera, entity) and its window is temporal rather than a sorted-neighbourhood window over a sort key. **Axis 4.**

**[akidau2015dataflow]** *The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing.* Tyler Akidau, Robert Bradshaw, Craig Chambers, et al. 2015. Proceedings of the VLDB Endowment (PVLDB) 8(12):1792–1803. DOI 10.14778/2824032.2824076.
Formalises fixed, sliding and **session** windows with a user-specified gap duration, and separates event time from processing time via watermarks and triggers.
*Difference:* Paper 5's collapse window *is* a keyed session window with gap W; the paper should adopt this vocabulary rather than present it as a new mechanism. **Axis 4.**

**[cugola2012processing]** *Processing Flows of Information: From Data Stream to Complex Event Processing.* Gianpaolo Cugola, Alessandro Margara. 2012. ACM Computing Surveys (CSUR) 44(3):Article 15, 1–62. DOI 10.1145/2187671.2187677.
Unifying survey of DSMS and CEP, including uniform event tuple models and temporal-window operators over heterogeneous event sources.
*Difference:* Paper 5's nine-field record and collapse rule are expressible as a single CEP pattern; the contribution has to be the empirical study, not the abstraction. **Axis 4, and see (C).**

**[catledge1995characterizing]** *Characterizing Browsing Strategies in the World-Wide Web.* Lara D. Catledge, James E. Pitkow. 1995. Computer Networks and ISDN Systems 27(6):1065–1073. DOI 10.1016/0169-7552(95)00043-7.
Origin of the 25.5-minute session timeout, obtained as mean + 1.5 standard deviations of the observed inter-event interval distribution.
*Difference:* Paper 5 needs exactly this move — a threshold read off the measured gap distribution — but should use a better estimator than mean+1.5σ on a heavy-tailed variable. **Axis 4, key for (B).**

**[jones2008beyond]** *Beyond the Session Timeout: Automatic Hierarchical Segmentation of Search Topics in Query Logs.* Rosie Jones, Kristina Lisa Klinkner. 2008. Proc. 17th ACM Conference on Information and Knowledge Management (CIKM '08), pp. 699–708. DOI 10.1145/1458082.1458176.
Shows empirically that **no single timeout value performs well** for session segmentation, and that a learned boundary classifier substantially outperforms the best fixed timeout.
*Difference:* This is the strongest cautionary result against Paper 5's single global W = 120 s; the paper must either report per-camera W or defend the global value against this. **Axis 4, key for (B).**

**[halfaker2015session]** *User Session Identification Based on Strong Regularities in Inter-activity Time.* Aaron Halfaker, Oliver Keyes, Daniel Kluver, et al. 2015. Proc. 24th International Conference on World Wide Web (WWW '15), pp. 410–418. DOI 10.1145/2736277.2741117. arXiv:1411.2878.
Fits a **two-component mixture to the log inter-activity-time distribution** across many datasets and derives the session threshold from where the within-session and between-session components separate; finds the regularity is stable across very different systems.
*Difference:* This is the principled replacement for Paper 5's geometric derivation; Paper 5 would apply it to same-camera same-entity inter-detection gaps. **Axis 4, THE key reference for (B).**

**[meiss2009session]** *What's in a Session: Tracking Individual Behavior on the Web.* Mark Meiss, John Duncan, Bruno Gonçalves, José J. Ramasco, Filippo Menczer. 2009. Proc. 20th ACM Conference on Hypertext and Hypermedia (HT '09), pp. 173–182. DOI 10.1145/1557914.1557946.
Shows session statistics are highly sensitive to the timeout choice and that inter-event times are broadly distributed rather than cleanly bimodal in some traffic.
*Difference:* Provides the sensitivity-analysis obligation Paper 5 currently discharges only informally. **Axis 4.**

**[gayoavello2009survey]** *A Survey on Session Detection Methods in Query Logs and a Proposal for Future Evaluation.* Daniel Gayo-Avello. 2009. Information Sciences 179(12):1822–1843. DOI 10.1016/j.ins.2009.01.026.
Surveys time-gap, content-based and hybrid session-detection methods and proposes an evaluation protocol against ground-truth segmentations.
*Difference:* Paper 5 has ground-truth incidents and can run precisely this evaluation, which would convert its window choice from assertion to measurement. **Axis 4.**

**[satopaa2011kneedle]** *Finding a "Kneedle" in a Haystack: Detecting Knee Points in System Behavior.* Ville Satopää, Jeannie Albrecht, David Irwin, Barath Raghavan. 2011. 31st International Conference on Distributed Computing Systems Workshops (ICDCSW 2011), pp. 166–171. DOI 10.1109/ICDCSW.2011.20.
A general, reproducible knee-detection algorithm (maximum curvature on a normalised difference curve, with an explicit sensitivity parameter S).
*Difference:* Paper 5 observed a knee at 15–30 s by inspection; Kneedle makes that knee a reported, reproducible statistic with a stated sensitivity. **Axis 4/7, key for (B).**

---

## Axis 5 — Multi-camera and multi-analytic surveillance

**[valera2005intelligent]** *Intelligent Distributed Surveillance Systems: A Review.* María Valera, Sergio A. Velastin. 2005. IEE Proceedings — Vision, Image and Signal Processing 152(2):192–204. DOI 10.1049/ip-vis:20041147.
Reviews third-generation distributed surveillance architectures, including sensor-fusion and multi-agent event-integration layers.
*Difference:* Paper 5 supplies deployment measurements (alert volumes, recall) that this architectural review does not report. **Axis 5.**

**[wang2013multicamera]** *Intelligent Multi-Camera Video Surveillance: A Review.* Xiaogang Wang. 2013. Pattern Recognition Letters (PRL) 34(1):3–19. DOI 10.1016/j.patrec.2012.07.005.
Reviews cross-camera calibration, topology inference, tracking and re-identification for multi-camera surveillance.
*Difference:* Paper 5 deduplicates *within* a camera across analytics, an orthogonal problem to the cross-camera association this review covers. **Axis 5.**

**[ye2022reid]** *Deep Learning for Person Re-Identification: A Survey and Outlook.* Mang Ye, Jianbing Shen, Gaojie Lin, et al. 2022. IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI) 44(6):2872–2893. DOI 10.1109/TPAMI.2021.3054775.
Comprehensive survey of person re-identification, i.e. the entity-resolution step that Paper 5 treats as a solved input.
*Difference:* Paper 5 consumes an identity decision and studies what to do with it downstream; it contributes nothing to re-ID accuracy. **Axis 5.**

**[tang2019cityflow]** *CityFlow: A City-Scale Benchmark for Multi-Target Multi-Camera Vehicle Tracking and Re-Identification.* Zheng Tang, Milind Naphade, Ming-Yu Liu, et al. 2019. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR 2019), pp. 8789–8798. DOI 10.1109/CVPR.2019.00900.
City-scale multi-camera vehicle benchmark with spatio-temporal association across 40 cameras.
*Difference:* CityFlow evaluates association accuracy; Paper 5 evaluates operator alert burden, and no public benchmark exists for the latter — a gap Paper 5 can claim. **Axis 5.**

---

## Axis 6 — Debouncing, chattering suppression, and how the timer is tuned

**[kondaveeti2013chatter]** *Quantification of Alarm Chatter Based on Run Length Distributions.* Sandeep R. Kondaveeti, Iman Izadi, Sirish L. Shah, David S. Shook, Ramesh Kadali, Tongwen Chen. 2013. Chemical Engineering Research and Design (ChERD) 91(12):2550–2558. DOI 10.1016/j.cherd.2013.02.028. (Earlier version: 49th IEEE CDC 2010, DOI 10.1109/CDC.2010.5718086.)
Defines a **chattering index** from the empirical run-length distribution of alarm states and uses it to decide whether and how much debouncing a tag needs.
*Difference:* Paper 5 has an exactly analogous statistic available (run-length of repeated same-entity detections) but does not compute one; adding it would strengthen the paper. **Axis 6.**

**[naghoosi2011estimation]** *Estimation of Alarm Chattering.* Elham Naghoosi, Iman Izadi, Tongwen Chen. 2011. Journal of Process Control (JPC) 21(9):1243–1249. DOI 10.1016/j.jprocont.2011.07.015.
Analytically estimates chattering frequency as a function of the signal statistics, so that a suppression parameter can be predicted rather than tuned by hand.
*Difference:* Paper 5's process is a discrete detection stream, not a noisy continuous variable, so this exact model does not transfer — but the *methodology* (predict chatter, then size the timer) does. **Axis 6.**

**[adnan2011detectiondelay]** *On Expected Detection Delays for Alarm Systems with Deadbands and Delay-Timers.* Naseeb Ahmed Adnan, Iman Izadi, Tongwen Chen. 2011. Journal of Process Control (JPC) 21(9):1318–1331. DOI 10.1016/j.jprocont.2011.06.019.
Derives closed-form expected detection delay as an explicit function of deadband width and delay-timer length, exposing the false-alarm/missed-alarm/latency three-way trade-off.
*Difference:* This is the formal statement of the cost Paper 5 pays at W = 120 s; Paper 5 currently reports masking empirically without a delay model. **Axis 6, key for (B).**

**[afzal2018timedeadbands]** *Analysis and Design of Time-Deadbands for Univariate Alarm Systems.* Muhammad Shahzad Afzal, Tongwen Chen, Ali Bandehkhoda, Iman Izadi. 2018. Control Engineering Practice (CEP) 71:96–107. DOI 10.1016/j.conengprac.2017.10.016.
Analyses *time*-deadbands (the direct analogue of a collapse window) and gives design procedures trading false-alarm rate against detection delay.
*Difference:* Paper 5's W is a time-deadband on an event stream keyed by entity; this paper shows such a parameter is designed from a rate/delay objective, never from geometry. **Axis 6, key for (B).**

**[wang2022delaytimers]** *Design of Delay Timers Based on Estimated Probability Mass Functions of Alarm Durations.* Jiandong Wang, Zhen Wang, Xuan Zhou, Fan Yang. 2022. Journal of Process Control (JPC) 110:154–165. DOI 10.1016/j.jprocont.2022.01.002.
Estimates the empirical PMF of alarm durations from historical data and **solves for the delay-timer length that meets a specified false-alarm-rate / missed-alarm-rate / expected-delay specification**.
*Difference:* This is the most directly transferable principled method for Paper 5, and it is the strongest single piece of prior art on "how the timer is tuned". **Axis 6, THE key reference for (B) alongside Halfaker.**

---

## Axis 7 — Evaluation metrics for alert systems

**[axelsson2000baserate]** *The Base-Rate Fallacy and the Difficulty of Intrusion Detection.* Stefan Axelsson. 2000. ACM Transactions on Information and System Security (TISSEC) 3(3):186–205. DOI 10.1145/357830.357849. (Earlier: CCS '99, DOI 10.1145/319709.319710.)
Shows that with a low incident base rate, Bayesian detection rate (precision) collapses even at excellent per-event false-positive rates — the mathematical reason alert fatigue is structural.
*Difference:* Paper 5 mitigates the *symptom* (volume) by collapsing co-referent alerts; it does not change the base rate, and should say so explicitly. **Axis 7.**

**[fawcett2006roc]** *An Introduction to ROC Analysis.* Tom Fawcett. 2006. Pattern Recognition Letters (PRL) 27(8):861–874. DOI 10.1016/j.patrec.2005.10.010.
Standard treatment of ROC curves, the convex hull, iso-performance lines, and cost-sensitive operating-point selection.
*Difference:* Paper 5 has a one-dimensional parameter sweep over W that can be plotted as an ROC-like curve; adopting this formalism converts "we picked 120 s" into "we picked the operating point implied by cost ratio r". **Axis 7, key for (B).**

**[ocsf]** *(NON-PAPER — OPEN SPECIFICATION)* *Open Cybersecurity Schema Framework (OCSF) Schema.* OCSF Project (originally AWS/Splunk et al.), continuously versioned. https://schema.ocsf.io/ and https://github.com/ocsf/ocsf-schema
A vendor-neutral, product-agnostic normalised event schema with a single base event class specialised by category — literally "one record shape for heterogeneous detectors".
*Difference:* Prior art against Paper 5's schema-novelty claim; see (C). **Axis 3, C.**

---

# (A) The five works a reviewer will say most anticipate Paper 5

### 1. Debar & Wespi (2001), *Aggregation and Correlation of Intrusion-Detection Alerts*
**Why it anticipates:** It already defines a *duplicate relation* over a normalised, detector-agnostic alert record and collapses duplicates within an explicit time window. That is Paper 5's mechanism, twenty-five years earlier, with the same justification (operator load).
**Strongest honest rebuttal:** Debar & Wespi's duplicates are alerts from *redundant sensors watching the same event of the same type*. Paper 5 collapses alerts of *different semantic types* (a plate read, a face match, an ROI occupancy) that resolve to the same physical entity — the equivalence class is defined by entity identity across modalities, not by alert-type equivalence, and no re-identification step exists in their pipeline. Paper 5 also reports incident-level recall against ground truth, which they do not.
**Strongest honest concession:** The collapse predicate, the normalised record, and the "aggregate within a window to fight operator overload" argument are all present in their paper. Paper 5 cannot claim any of the three as new. The honest framing is "we instantiate the Debar–Wespi duplicate relation for cross-modal video analytics and, for the first time, measure how the window length trades reduction against incident masking."

### 2. Valdes & Skinner (2001), *Probabilistic Alert Correlation*
**Why it anticipates:** Explicitly heterogeneous-sensor alert fusion into meta-alerts, with a common attribute vector and a similarity threshold — including a *time proximity* attribute.
**Strongest honest rebuttal:** Their fusion is a weighted multi-attribute similarity with hand-set expectation-of-similarity weights, which is unauditable in a policing context and has no incident-recall guarantee. Paper 5's single Boolean predicate is defensible in a chain-of-evidence setting precisely because it is not tunable per attribute, and Paper 5 quantifies the recall cost of that simplicity.
**Strongest honest concession:** Their "minimum similarity" threshold is functionally the same design knob as W, and they were already fusing across sensor modalities using a uniform record. Paper 5's "entity-agnostic, no union type" framing is an implementation-cleanliness claim, not a scientific advance over this.

### 3. Wang, Wang, Zhou & Yang (2022), *Design of Delay Timers Based on Estimated PMFs of Alarm Durations* (with Adnan et al. 2011 and Afzal et al. 2018 as the supporting line)
**Why it anticipates:** This is the exact problem — choosing a debounce/suppression time constant — solved *principledly*, from the empirical duration distribution against a stated false-alarm/missed-alarm/delay specification. A reviewer will say: the correct way to pick W has been known in process control for over a decade, and Paper 5's geometric derivation ignores it.
**Strongest honest rebuttal:** Their formulation assumes a univariate alarm variable with a well-defined alarm/normal binary state and (in the analytic versions) stationarity or known noise statistics. A cross-modal, entity-keyed event stream from three heterogeneous detectors on a city camera network satisfies none of that; the transfer is a genuine contribution, not a lookup.
**Strongest honest concession:** The transfer is straightforward and the method is superior to what Paper 5 currently does. **You should adopt it and cite it, not fight it.** The geometric derivation must be withdrawn.

### 4. Akidau et al. (2015), *The Dataflow Model*
**Why it anticipates:** Keyed session windows with a user-specified gap are a first-class, named primitive here. Paper 5's collapse is a session window keyed by (camera, entity) with gap W, plus a "take the first element" reduction.
**Strongest honest rebuttal:** Dataflow is a *systems* paper: it provides the mechanism and is explicit that the gap is a user parameter it does not help you choose. Paper 5's whole subject is how to choose it, on real incident ground truth. Also, Dataflow's sessions merge transitively on activity, whereas Paper 5's window is (presumably) anchored to the first observation — worth stating precisely, since the two give different results under sustained presence, and the 120 s figure means very different things under each.
**Strongest honest concession:** The window taxonomy and vocabulary are theirs. Paper 5 should use "keyed session window with gap W" as the description and stop implying the construct is novel.

### 5. Steinberg, Bowman & White (1999), *Revisions to the JDL Data Fusion Model* (with Hall & Llinas 1997)
**Why it anticipates:** JDL Level 0/1 mandates *common referencing* — normalising heterogeneous sensor reports into a shared representation — followed by data association and entity-state estimation. Paper 5's architecture is a textbook Level-1 pipeline.
**Strongest honest rebuttal:** JDL is a reference model, not a system or a result; it prescribes that you must normalise and associate, and says nothing about how to key or window the association for entity-agnostic video detections, nor does it produce operator-load numbers.
**Strongest honest concession:** "A single schema across modalities with no union type" is, in JDL terms, just common referencing. Claiming it as a contribution invites an easy reject. Reposition it as an engineering description within a JDL Level-1 framing.

---

# (B) DIRECT ANSWER — how the literature says to choose a deduplication / session window

**Short version: there is no geometric derivation anywhere in this literature. Every defensible method in the record is one of five families, all of which are (i) data-driven from the observed inter-event distribution, or (ii) chosen against an explicitly stated error/cost specification. Your measured 15–30 s knee is exactly what these methods would produce; your 120 s is not defensible and your FOV/speed derivation should be deleted, not repaired.**

### Method 1 (recommended primary) — Mixture-model crossover on the inter-observation-time distribution
**Halfaker et al. 2015 (WWW, DOI 10.1145/2736277.2741117).** Take all consecutive pairs of observations that resolve to the same entity at the same camera. Plot the distribution of log inter-observation time. Fit a two-component mixture (they use log-normals). One component is "same visit / same physical presence"; the other is "genuinely distinct return". Set W at the crossover point of the two densities, i.e. the time at which a gap becomes more likely to be a new presence than a continuation. Halfaker et al. show this regularity is strikingly stable across very different systems, and it gives a threshold with a stated misclassification interpretation rather than a convention.
**Why it fixes your problem:** it will produce something in the seconds-to-tens-of-seconds range for a fixed camera with a real dwell-time distribution — consistent with your 15–30 s knee — and it makes 120 s visibly indefensible, because the second mixture component (distinct incidents) will already dominate well before 120 s.
**Caveat to report:** Meiss et al. 2009 (DOI 10.1145/1557914.1557946) show the distribution is not always cleanly bimodal; report the fitted components and the separation, and if bimodality is weak, fall back to Method 3 or 4.

### Method 2 — Distribution-based timer design against a stated (FAR, MAR, delay) specification
**Wang et al. 2022 (JPC, DOI 10.1016/j.jprocont.2022.01.002)**, with **Adnan et al. 2011 (JPC, DOI 10.1016/j.jprocont.2011.06.019)** for the closed-form delay cost and **Afzal et al. 2018 (CEP, DOI 10.1016/j.conengprac.2017.10.016)** for the time-deadband case.
Estimate the empirical PMF/PDF of the relevant durations from historical logs, then *solve* for the timer that meets a specification you state up front — e.g. "≤ 1% of distinct incidents masked, subject to maximising duplicate suppression" or "expected added alerting delay ≤ 2 s". This is the process-control answer and it is the single most quotable rebuttal to a geometric derivation: the alarm-management field abandoned first-principles timer derivations in favour of duration-distribution-based design more than a decade ago.
**Practical form for you:** define missed-incident rate MIR(W) = fraction of ground-truth distinct incidents collapsed away, and duplicate-suppression rate DSR(W). Report W* = max{W : MIR(W) ≤ α} for a pre-registered α. That is a defensible sentence in a TCSVT paper. "FOV depth over permitted speed" is not.

### Method 3 — Knee / elbow criterion, made reproducible
**Satopää et al. 2011 (ICDCSW, DOI 10.1109/ICDCSW.2011.20).** You already have the reduction-vs-masking curve and you already see the knee at 15–30 s. Do not report it by eye. Run Kneedle on the normalised curve, report the detected knee and the sensitivity parameter S, and show the knee is stable across cameras and across a sensitivity sweep. This turns your strongest empirical finding into a citable, reproducible statistic and directly supports the claim that the deployed 120 s is on the wrong side of the knee.

### Method 4 — ROC-style operating-point selection with an explicit cost ratio
**Fawcett 2006 (PRL, DOI 10.1016/j.patrec.2005.10.010)**, with **Axelsson 2000 (TISSEC, DOI 10.1145/357830.357849)** for the base-rate argument and **Bar-Shalom 1981 (TAC, DOI 10.1109/TAC.1981.1102635)** / **Fellegi & Sunter 1969 (JASA, DOI 10.1080/01621459.1969.10501049)** for the precedent that association thresholds are set from stated error rates.
Sweep W, plot (incident-masking rate) against (redundant-alert rate), take the convex hull, and choose the point where the iso-performance line of slope r = cost(missed incident)/cost(redundant alert) is tangent. For policing, r is enormous, which pushes W small — this is the most honest way to publish a recommendation, because it makes the value judgement explicit and lets a different deployment pick a different W from the same curve. **This is the framing I would lead with in the paper**, with Method 1 or 2 supplying the point estimate.

### Method 5 (a warning you must engage with) — do not defend a single global W at all
**Jones & Klinkner 2008 (CIKM, DOI 10.1145/1458082.1458176)** demonstrated that *no* single timeout performs well for session segmentation and that a learned boundary classifier beats the best fixed timeout by a wide margin. **Gayo-Avello 2009 (Inf. Sci., DOI 10.1016/j.ins.2009.01.026)** gives the evaluation protocol for comparing session-detection methods against ground truth. A reviewer who knows this literature will ask why W is global rather than per-camera (FOV depth, traffic regime and dwell distribution all vary per camera) or learned from features. Your safest position: report a per-camera W fitted by Method 1, show the distribution of fitted W values across the estimate (which will itself be a nice result if it spans, say, 8–40 s), and report the global-W ablation as the deployment-simplicity baseline with its measured recall cost.

### On an entropy criterion — the honest answer
I searched for an information-theoretic (entropy / MDL) criterion for selecting a temporal aggregation window and **did not find one I can verify and recommend** in this literature. The alarm-flood segmentation work I could verify (e.g. Cheng, Izadi & Chen 2013, ChERD, DOI 10.1016/j.cherd.2012.11.001) inherits its flood boundary from the EEMUA 191 convention (>10 alarms per 10 min per operator) rather than deriving it. Do not claim an entropy criterion. The four defensible families are: mixture crossover, distribution-based specification design, knee detection, and cost-weighted ROC operating point.

### Where 120 s could still be defended (the one honest escape route)
If 120 s is not a *deduplication* window but a *case-grouping* window for the operator's incident view — i.e. the system alerts within seconds and separately groups related alerts into a case for the following two minutes — then a longer value is legitimate and the masking objection largely dissolves. That is a two-tier design (Debar & Wespi's duplicate relation at short W, consequence/situation relation at long W). If your deployment actually does this, say so; if it does not, this is the redesign the data is pointing at.

---

# (C) Is the "entity-agnostic single record schema across modalities" novel? — the truth

**No. It is standard practice, and has been for two decades. Do not claim it as a contribution.** A reviewer who works in either fusion or security operations will recognise it immediately, and the claim will cost you credibility on the parts of the paper that *are* defensible.

The precedents, in order of how damaging each is:

1. **IDMEF, RFC 4765 (2007, DOI 10.17487/RFC4765)** — a normative, detector-agnostic alert record with source, target, classification, analyzer, time, and confidence, explicitly designed so that alerts from unrelated and dissimilar detectors are directly comparable. This is a published IETF standard predating your work by ~19 years and is a near-exact conceptual match to a "nine-field entity-agnostic event record with no union type."
2. **OCSF (schema.ocsf.io)**, and its industrial predecessors ArcSight **CEF**, IBM QRadar **LEEF**, and MITRE **CEE** — all are, precisely, single normalised event schemas with a common base class specialised by category, adopted exactly so that heterogeneous detectors need no union type. This is a live, widely deployed industry norm.
3. **JDL Level 0/1 common referencing** — Steinberg, Bowman & White 1999 (DOI 10.1117/12.341367) and Hall & Llinas 1997 (DOI 10.1109/5.554205) make normalisation of heterogeneous sensor reports into a shared representation a *required stage* of the reference model, not an option.
4. **Alert correlation pipelines** — Salah et al. 2013 (DOI 10.1016/j.comnet.2012.10.022) taxonomises normalisation as the mandatory first stage of every alert correlation system surveyed; Debar & Wespi 2001 and Valdes & Skinner 2001 both operate over such a schema.
5. **CEP** — Cugola & Margara 2012 (DOI 10.1145/2187671.2187677): uniform event tuples over heterogeneous sources with temporal window operators is the defining abstraction of the field.
6. **Record linkage** — Fellegi & Sunter 1969 (DOI 10.1080/01621459.1969.10501049): the comparison-vector formulation is deliberately agnostic to what the records describe.

**What you can honestly claim.** Not the schema, and not the collapse predicate in the abstract. What is genuinely unclaimed in the verified literature is:

- an **empirical characterisation of the deduplication-window operating curve for cross-modal video analytics on a deployed municipal camera network**, with incident-level ground truth — I found no such measurement in surveillance, and no benchmark for it (CityFlow and the re-ID literature measure association accuracy, not operator alert burden);
- the **negative result** that a geometric FOV-depth/speed derivation of W is wrong by one to two orders of magnitude against the measured knee — this is a genuinely useful, publishable finding, and it is much stronger than the claim it replaces;
- the demonstration that **one entity-keyed collapse predicate suffices across three unrelated analytics** at a stated incident recall — an *empirical sufficiency result*, framed against Valdes–Skinner's multi-attribute similarity as the alternative.

Reframe the paper around those three and it survives review. Keep the geometric derivation and the schema-novelty claim, and both will be attacked, correctly.

---

# (D) BibTeX

```bibtex
% ===== Axis 1: alert fatigue, alarm flood, alarm management =====
@article{tariq2025alertfatigue,
  author  = {Tariq, Shahroz and Baruwal Chhetri, Mohan and Nepal, Surya and Paris, Cecile},
  title   = {Alert Fatigue in Security Operations Centres: Research Challenges and Opportunities},
  journal = {ACM Computing Surveys},
  volume  = {57}, number = {9}, pages = {1--38}, year = {2025},
  doi     = {10.1145/3723158}
}

@inproceedings{alahmadi2022falsepositives,
  author    = {Alahmadi, Bushra A. and Axon, Louise and Martinovic, Ivan},
  title     = {99\% False Positives: A Qualitative Study of {SOC} Analysts' Perspectives on Security Alarms},
  booktitle = {31st USENIX Security Symposium (USENIX Security 22)},
  publisher = {USENIX Association}, year = {2022},
  note      = {No DOI assigned},
  url       = {https://www.usenix.org/conference/usenixsecurity22/presentation/alahmadi}
}

@inproceedings{sundaramurthy2015burnout,
  author    = {Sundaramurthy, Sathya Chandran and Bardas, Alexandru G. and Case, Jacob and
               Ou, Xinming and Wesch, Michael and McHugh, John and Rajagopalan, S. Raj},
  title     = {A Human Capital Model for Mitigating Security Analyst Burnout},
  booktitle = {Eleventh Symposium on Usable Privacy and Security (SOUPS 2015)},
  publisher = {USENIX Association}, year = {2015},
  note      = {No DOI assigned},
  url       = {https://www.usenix.org/conference/soups2015/proceedings/presentation/sundaramurthy}
}

@article{wang2016alarmoverview,
  author  = {Wang, Jiandong and Yang, Fan and Chen, Tongwen and Shah, Sirish L.},
  title   = {An Overview of Industrial Alarm Systems: Main Causes for Alarm Overloading,
             Research Status, and Open Problems},
  journal = {IEEE Transactions on Automation Science and Engineering},
  volume  = {13}, number = {2}, pages = {1045--1061}, year = {2016},
  doi     = {10.1109/TASE.2015.2464234}
}

@article{kondaveeti2012graphical,
  author  = {Kondaveeti, Sandeep R. and Izadi, Iman and Shah, Sirish L. and Black, Tim and Chen, Tongwen},
  title   = {Graphical Tools for Routine Assessment of Industrial Alarm Systems},
  journal = {Computers \& Chemical Engineering},
  volume  = {46}, pages = {39--47}, year = {2012},
  doi     = {10.1016/j.compchemeng.2012.06.042}
}

@manual{isa182,
  title        = {{ANSI/ISA-18.2-2016}: Management of Alarm Systems for the Process Industries},
  organization = {International Society of Automation}, address = {Research Triangle Park, NC, USA},
  year         = {2016},
  note         = {Standard (non-paper reference)},
  url          = {https://www.isa.org/standards-and-publications/isa-standards}
}

@manual{eemua191,
  title        = {{EEMUA} Publication 191: Alarm Systems --- A Guide to Design, Management and Procurement},
  organization = {Engineering Equipment and Materials Users' Association}, address = {London, UK},
  edition      = {3rd}, year = {2013},
  note         = {Industry guide (non-paper reference); edition/year should be confirmed against
                  the copy used, as later editions exist},
  url          = {https://www.eemua.org/products/publications/print/eemua-publication-191}
}

% ===== Axis 2: IDS alert correlation and aggregation =====
@inproceedings{valdes2001probabilistic,
  author    = {Valdes, Alfonso and Skinner, Keith},
  title     = {Probabilistic Alert Correlation},
  booktitle = {Recent Advances in Intrusion Detection (RAID 2001)},
  series    = {Lecture Notes in Computer Science}, volume = {2212},
  pages     = {54--68}, publisher = {Springer}, year = {2001},
  doi       = {10.1007/3-540-45474-8_4}
}

@article{julisch2003clustering,
  author  = {Julisch, Klaus},
  title   = {Clustering Intrusion Detection Alarms to Support Root Cause Analysis},
  journal = {ACM Transactions on Information and System Security},
  volume  = {6}, number = {4}, pages = {443--471}, year = {2003},
  doi     = {10.1145/950191.950192}
}

@inproceedings{debar2001aggregation,
  author    = {Debar, Herv{\'e} and Wespi, Andreas},
  title     = {Aggregation and Correlation of Intrusion-Detection Alerts},
  booktitle = {Recent Advances in Intrusion Detection (RAID 2001)},
  series    = {Lecture Notes in Computer Science}, volume = {2212},
  pages     = {85--103}, publisher = {Springer}, year = {2001},
  doi       = {10.1007/3-540-45474-8_6}
}

@inproceedings{ning2002constructing,
  author    = {Ning, Peng and Cui, Yun and Reeves, Douglas S.},
  title     = {Constructing Attack Scenarios through Correlation of Intrusion Alerts},
  booktitle = {Proceedings of the 9th ACM Conference on Computer and Communications Security (CCS '02)},
  pages     = {245--254}, year = {2002},
  doi       = {10.1145/586110.586144}
}

@article{salah2013modelbased,
  author  = {Salah, Saeed and Maci{\'a}-Fern{\'a}ndez, Gabriel and D{\'i}az-Verdejo, Jes{\'u}s E.},
  title   = {A Model-Based Survey of Alert Correlation Techniques},
  journal = {Computer Networks},
  volume  = {57}, number = {5}, pages = {1289--1317}, year = {2013},
  doi     = {10.1016/j.comnet.2012.10.022}
}

@techreport{idmef2007,
  author      = {Debar, Herv{\'e} and Curry, David A. and Feinstein, Benjamin S.},
  title       = {The Intrusion Detection Message Exchange Format ({IDMEF})},
  number      = {RFC 4765}, institution = {IETF}, year = {2007},
  doi         = {10.17487/RFC4765},
  note        = {IETF RFC (non-paper reference)},
  url         = {https://www.rfc-editor.org/rfc/rfc4765.html}
}

% ===== Axis 3: multi-sensor / multi-modal fusion =====
@inproceedings{steinberg1999jdl,
  author    = {Steinberg, Alan N. and Bowman, Christopher L. and White, Franklin E.},
  title     = {Revisions to the {JDL} Data Fusion Model},
  booktitle = {Sensor Fusion: Architectures, Algorithms, and Applications III},
  series    = {Proceedings of SPIE}, volume = {3719}, pages = {430--441}, year = {1999},
  doi       = {10.1117/12.341367}
}

@article{hall1997introduction,
  author  = {Hall, David L. and Llinas, James},
  title   = {An Introduction to Multisensor Data Fusion},
  journal = {Proceedings of the IEEE},
  volume  = {85}, number = {1}, pages = {6--23}, year = {1997},
  doi     = {10.1109/5.554205}
}

@article{khaleghi2013multisensor,
  author  = {Khaleghi, Bahador and Khamis, Alaa and Karray, Fakhreddine O. and Razavi, Saiedeh N.},
  title   = {Multisensor Data Fusion: A Review of the State-of-the-Art},
  journal = {Information Fusion},
  volume  = {14}, number = {1}, pages = {28--44}, year = {2013},
  doi     = {10.1016/j.inffus.2011.08.001}
}

@article{dempster1967upper,
  author  = {Dempster, Arthur P.},
  title   = {Upper and Lower Probabilities Induced by a Multivalued Mapping},
  journal = {The Annals of Mathematical Statistics},
  volume  = {38}, number = {2}, pages = {325--339}, year = {1967},
  doi     = {10.1214/aoms/1177698950}
}

@article{barshalom1981tracktotrack,
  author  = {Bar-Shalom, Yaakov},
  title   = {On the Track-to-Track Correlation Problem},
  journal = {IEEE Transactions on Automatic Control},
  volume  = {26}, number = {2}, pages = {571--572}, year = {1981},
  doi     = {10.1109/TAC.1981.1102635}
}

@misc{ocsf,
  author       = {{OCSF Project}},
  title        = {Open Cybersecurity Schema Framework ({OCSF}) Schema},
  howpublished = {Open specification},
  note         = {Non-paper reference; continuously versioned},
  url          = {https://schema.ocsf.io/}
}

% ===== Axis 4: data association, deduplication, temporal windowing =====
@article{fellegi1969theory,
  author  = {Fellegi, Ivan P. and Sunter, Alan B.},
  title   = {A Theory for Record Linkage},
  journal = {Journal of the American Statistical Association},
  volume  = {64}, number = {328}, pages = {1183--1210}, year = {1969},
  doi     = {10.1080/01621459.1969.10501049}
}

@article{elmagarmid2007duplicate,
  author  = {Elmagarmid, Ahmed K. and Ipeirotis, Panagiotis G. and Verykios, Vassilios S.},
  title   = {Duplicate Record Detection: A Survey},
  journal = {IEEE Transactions on Knowledge and Data Engineering},
  volume  = {19}, number = {1}, pages = {1--16}, year = {2007},
  doi     = {10.1109/TKDE.2007.250581}
}

@article{akidau2015dataflow,
  author  = {Akidau, Tyler and Bradshaw, Robert and Chambers, Craig and Chernyak, Slava and
             Fern{\'a}ndez-Moctezuma, Rafael J. and Lax, Reuven and McVeety, Sam and Mills, Daniel and
             Perry, Frances and Schmidt, Eric and Whittle, Sam},
  title   = {The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in
             Massive-Scale, Unbounded, Out-of-Order Data Processing},
  journal = {Proceedings of the VLDB Endowment},
  volume  = {8}, number = {12}, pages = {1792--1803}, year = {2015},
  doi     = {10.14778/2824032.2824076}
}

@article{cugola2012processing,
  author  = {Cugola, Gianpaolo and Margara, Alessandro},
  title   = {Processing Flows of Information: From Data Stream to Complex Event Processing},
  journal = {ACM Computing Surveys},
  volume  = {44}, number = {3}, pages = {15:1--15:62}, year = {2012},
  doi     = {10.1145/2187671.2187677}
}

@article{catledge1995characterizing,
  author  = {Catledge, Lara D. and Pitkow, James E.},
  title   = {Characterizing Browsing Strategies in the World-Wide Web},
  journal = {Computer Networks and ISDN Systems},
  volume  = {27}, number = {6}, pages = {1065--1073}, year = {1995},
  doi     = {10.1016/0169-7552(95)00043-7}
}

@inproceedings{jones2008beyond,
  author    = {Jones, Rosie and Klinkner, Kristina Lisa},
  title     = {Beyond the Session Timeout: Automatic Hierarchical Segmentation of Search Topics in Query Logs},
  booktitle = {Proceedings of the 17th ACM Conference on Information and Knowledge Management (CIKM '08)},
  pages     = {699--708}, year = {2008},
  doi       = {10.1145/1458082.1458176}
}

@inproceedings{halfaker2015session,
  author    = {Halfaker, Aaron and Keyes, Oliver and Kluver, Daniel and Thebault-Spieker, Jacob and
               Nguyen, Tien and Shores, Kenneth and Uduwage, Anuradha and Warncke-Wang, Morten},
  title     = {User Session Identification Based on Strong Regularities in Inter-activity Time},
  booktitle = {Proceedings of the 24th International Conference on World Wide Web (WWW '15)},
  pages     = {410--418}, year = {2015},
  doi       = {10.1145/2736277.2741117},
  note      = {arXiv:1411.2878}
}

@inproceedings{meiss2009session,
  author    = {Meiss, Mark and Duncan, John and Gon{\c c}alves, Bruno and Ramasco, Jos{\'e} J. and Menczer, Filippo},
  title     = {What's in a Session: Tracking Individual Behavior on the Web},
  booktitle = {Proceedings of the 20th ACM Conference on Hypertext and Hypermedia (HT '09)},
  pages     = {173--182}, year = {2009},
  doi       = {10.1145/1557914.1557946}
}

@article{gayoavello2009survey,
  author  = {Gayo-Avello, Daniel},
  title   = {A Survey on Session Detection Methods in Query Logs and a Proposal for Future Evaluation},
  journal = {Information Sciences},
  volume  = {179}, number = {12}, pages = {1822--1843}, year = {2009},
  doi     = {10.1016/j.ins.2009.01.026}
}

@inproceedings{satopaa2011kneedle,
  author    = {Satop{\"a}{\"a}, Ville and Albrecht, Jeannie and Irwin, David and Raghavan, Barath},
  title     = {Finding a ``Kneedle'' in a Haystack: Detecting Knee Points in System Behavior},
  booktitle = {2011 31st International Conference on Distributed Computing Systems Workshops (ICDCSW)},
  pages     = {166--171}, year = {2011},
  doi       = {10.1109/ICDCSW.2011.20}
}

% ===== Axis 5: multi-camera / multi-analytic surveillance =====
@article{valera2005intelligent,
  author  = {Valera, Mar{\'i}a and Velastin, Sergio A.},
  title   = {Intelligent Distributed Surveillance Systems: A Review},
  journal = {IEE Proceedings --- Vision, Image and Signal Processing},
  volume  = {152}, number = {2}, pages = {192--204}, year = {2005},
  doi     = {10.1049/ip-vis:20041147}
}

@article{wang2013multicamera,
  author  = {Wang, Xiaogang},
  title   = {Intelligent Multi-Camera Video Surveillance: A Review},
  journal = {Pattern Recognition Letters},
  volume  = {34}, number = {1}, pages = {3--19}, year = {2013},
  doi     = {10.1016/j.patrec.2012.07.005}
}

@article{ye2022reid,
  author  = {Ye, Mang and Shen, Jianbing and Lin, Gaojie and Xiang, Tao and Shao, Ling and Hoi, Steven C. H.},
  title   = {Deep Learning for Person Re-Identification: A Survey and Outlook},
  journal = {IEEE Transactions on Pattern Analysis and Machine Intelligence},
  volume  = {44}, number = {6}, pages = {2872--2893}, year = {2022},
  doi     = {10.1109/TPAMI.2021.3054775}
}

@inproceedings{tang2019cityflow,
  author    = {Tang, Zheng and Naphade, Milind and Liu, Ming-Yu and Yang, Xiaodong and Birchfield, Stan and
               Wang, Shuo and Kumar, Ratnesh and Anastasiu, David and Hwang, Jenq-Neng},
  title     = {{CityFlow}: A City-Scale Benchmark for Multi-Target Multi-Camera Vehicle Tracking and Re-Identification},
  booktitle = {2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages     = {8789--8798}, year = {2019},
  doi       = {10.1109/CVPR.2019.00900}
}

% ===== Axis 6: debouncing, chattering suppression, timer tuning =====
@article{kondaveeti2013chatter,
  author  = {Kondaveeti, Sandeep R. and Izadi, Iman and Shah, Sirish L. and Shook, David S. and
             Kadali, Ramesh and Chen, Tongwen},
  title   = {Quantification of Alarm Chatter Based on Run Length Distributions},
  journal = {Chemical Engineering Research and Design},
  volume  = {91}, number = {12}, pages = {2550--2558}, year = {2013},
  doi     = {10.1016/j.cherd.2013.02.028}
}

@article{naghoosi2011estimation,
  author  = {Naghoosi, Elham and Izadi, Iman and Chen, Tongwen},
  title   = {Estimation of Alarm Chattering},
  journal = {Journal of Process Control},
  volume  = {21}, number = {9}, pages = {1243--1249}, year = {2011},
  doi     = {10.1016/j.jprocont.2011.07.015}
}

@article{adnan2011detectiondelay,
  author  = {Adnan, Naseeb Ahmed and Izadi, Iman and Chen, Tongwen},
  title   = {On Expected Detection Delays for Alarm Systems with Deadbands and Delay-Timers},
  journal = {Journal of Process Control},
  volume  = {21}, number = {9}, pages = {1318--1331}, year = {2011},
  doi     = {10.1016/j.jprocont.2011.06.019}
}

@article{afzal2018timedeadbands,
  author  = {Afzal, Muhammad Shahzad and Chen, Tongwen and Bandehkhoda, Ali and Izadi, Iman},
  title   = {Analysis and Design of Time-Deadbands for Univariate Alarm Systems},
  journal = {Control Engineering Practice},
  volume  = {71}, pages = {96--107}, year = {2018},
  doi     = {10.1016/j.conengprac.2017.10.016}
}

@article{wang2022delaytimers,
  author  = {Wang, Jiandong and Wang, Zhen and Zhou, Xuan and Yang, Fan},
  title   = {Design of Delay Timers Based on Estimated Probability Mass Functions of Alarm Durations},
  journal = {Journal of Process Control},
  volume  = {110}, pages = {154--165}, year = {2022},
  doi     = {10.1016/j.jprocont.2022.01.002}
}

% ===== Axis 7: evaluation metrics for alert systems =====
@article{axelsson2000baserate,
  author  = {Axelsson, Stefan},
  title   = {The Base-Rate Fallacy and the Difficulty of Intrusion Detection},
  journal = {ACM Transactions on Information and System Security},
  volume  = {3}, number = {3}, pages = {186--205}, year = {2000},
  doi     = {10.1145/357830.357849}
}

@article{fawcett2006roc,
  author  = {Fawcett, Tom},
  title   = {An Introduction to {ROC} Analysis},
  journal = {Pattern Recognition Letters},
  volume  = {27}, number = {8}, pages = {861--874}, year = {2006},
  doi     = {10.1016/j.patrec.2005.10.010}
}

% ===== supporting: alarm flood segmentation convention =====
@article{cheng2013smithwaterman,
  author  = {Cheng, Yue and Izadi, Iman and Chen, Tongwen},
  title   = {Pattern Matching of Alarm Flood Sequences by a Modified {Smith--Waterman} Algorithm},
  journal = {Chemical Engineering Research and Design},
  volume  = {91}, number = {6}, pages = {1085--1094}, year = {2013},
  doi     = {10.1016/j.cherd.2012.11.001}
}
```

---

## Bottom line for the paper

1. **Delete the geometric derivation.** It has no support in any of the seven literatures, and the alarm-management field (Adnan 2011, Afzal 2018, Wang 2022) explicitly designs these time constants from empirical duration distributions against a stated error specification. Your 1.3–9.6 s vs 15–30 s discrepancy is not a bug in your measurement; it is the derivation being the wrong kind of argument.
2. **Replace it with Halfaker-style mixture crossover on same-camera same-entity inter-detection gaps for the point estimate, Kneedle for the reproducible knee, and a Fawcett-style cost-weighted operating-point curve for the recommendation.** Cite Wang et al. 2022 as the domain precedent for the whole approach.
3. **Publish the 120 s failure as a finding.** "A widely-deployed 120 s collapse window masks distinct incidents; the data-derived window is 15–30 s" is a better paper than the one you set out to write.
4. **Drop the schema-novelty claim.** IDMEF, OCSF/CEF/LEEF, JDL common referencing, and CEP uniform event tuples all precede it. Reposition as a JDL Level-1 instantiation and put the novelty in the operating-point study.

Sources: [Valdes & Skinner (RAID 2001)](https://link.springer.com/chapter/10.1007/3-540-45474-8_4) · [Julisch (TISSEC 2003)](https://dl.acm.org/doi/10.1145/950191.950192) · [Wang et al. (T-ASE 2016)](https://ieeexplore.ieee.org/document/7270356/) · [Halfaker et al. (WWW 2015)](https://doi.org/10.1145/2736277.2741117) · [Alahmadi et al. (USENIX Sec 2022)](https://www.usenix.org/conference/usenixsecurity22/presentation/alahmadi) · [Sundaramurthy et al. (SOUPS 2015)](https://www.usenix.org/conference/soups2015/proceedings/presentation/sundaramurthy) · [RFC 4765 (IDMEF)](https://www.rfc-editor.org/rfc/rfc4765.html) · [OCSF](https://schema.ocsf.io/) · [ANSI/ISA-18.2-2016](https://webstore.ansi.org/standards/isa/ansiisa182016) · [EEMUA 191](https://www.eemua.org/products/publications/print/eemua-publication-191) · [Crossref REST API](https://api.crossref.org/)agentId: a6ef4747d48295519 (use SendMessage with to: 'a6ef4747d48295519', summary: '<5-10 word recap>' to continue this agent)
<usage>subagent_tokens: 139450
tool_uses: 66
duration_ms: 633514</usage>