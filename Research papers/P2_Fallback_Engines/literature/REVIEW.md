# P2 prior-art review: deterministic fallback engines and label-free accuracy estimation

32 verified entries. Three candidates dropped as unverifiable (a CODES+ISSS 2015
big/little DNN paper whose author list could not be confirmed; arXiv 2601.19862
"Calibration without Ground Truth", abstract confirmed but authors not
retrievable; a non-indexed Tesseract-vs-deep-OCR comparison).

Axes: (1) cascades and cross-class fallback, (2) label-free accuracy estimation,
(3) calibration / selective prediction / abstention, (4) reliability and safety
fallbacks, (5) reproducibility and nondeterminism, (6) provenance and production
ML monitoring, (7) ANPR/OCR pipelines mixing classical and deep methods.

---

## Axis 1 - Cascades, anytime inference, cross-class fallback

**viola2001rapid** — Rapid Object Detection Using a Boosted Cascade of Simple Features. Viola, Jones. 2001. CVPR.
Attentional cascade where early stages reject most windows cheaply.
*Differs:* P2's tiers are alternative complete engines each emitting a full record, not sequential filters on one decision.

**teerapittayanon2016branchynet** — BranchyNet: Fast Inference via Early Exiting from Deep Neural Networks. Teerapittayanon, McDanel, Kung. 2016. ICPR. arXiv:1709.01686
Side branches with entropy-thresholded early exits.
*Differs:* P2's fallback is a different algorithm class, triggered by exception/absence/empty result rather than a confidence threshold.

**wang2018idk** — IDK Cascades: Fast Deep Learning by Learning not to Overthink. Wang, Luo, Crankshaw et al. 2018. UAI. arXiv:1706.00885
Learns an explicit "I don't know" that routes hard inputs to a larger model.
*Differs:* P2 routes *downward* to a weaker but deterministic engine, and abstention is not learned.

**kang2017noscope** — NoScope: Optimizing Neural Network Queries over Video at Scale. Kang, Emmons, Abuzaid et al. 2017. PVLDB 10(11). doi:10.14778/3137628.3137664
Cascades a pixel-difference detector and a specialised CNN ahead of a full reference CNN under an accuracy target.
*Differs:* NoScope's cheap stages are filters calibrated against a labelled reference model; P2's secondary produces the answer of record and carries provenance forward. **The single most dangerous prior work for the fallback claim.**

**jiang2018chameleon** — Chameleon: Scalable Adaptation of Video Analytics. Jiang, Ananthanarayanan, Bodik et al. 2018. SIGCOMM. doi:10.1145/3230543.3230574
Re-picks NN configurations exploiting temporal and cross-camera correlation.
*Differs:* adaptation over configurations of one learned engine, not across algorithm classes.

**chen2023frugalgpt** — FrugalGPT. Chen, Zaharia, Zou. 2023. arXiv:2305.05176
LLM cascade with a learned scoring function deciding when a cheaper model suffices.
*Differs:* no learned router, and the second tier is not a smaller learned model.

## Axis 2 - Label-free accuracy estimation

**garg2022atc** — Leveraging Unlabeled Data to Predict Out-of-Distribution Performance. Garg, Balakrishnan, Lipton et al. 2022. ICLR. arXiv:2201.04234
ATC: fit a confidence threshold on labelled source data, predict target accuracy as the fraction above it; 2-4x better than prior estimators.
*Differs:* P2 fits the map per (path, entity class) stratum rather than one global threshold. **P2's closest competitor; per-stratum ATC is a three-line change.**

**baek2022agreement** — Agreement-on-the-Line. Baek, Jiang, Raghunathan, Kolter. 2022. NeurIPS. arXiv:2206.13089
ID-vs-OOD agreement between model pairs is linearly correlated with accuracy, giving label-free OOD accuracy from an ensemble.
*Differs:* P2 has a single deployed model and no ensemble; a deterministic classical engine has no meaningful agreement line.

**deng2021autoeval** — Are Labels Always Necessary for Classifier Accuracy Evaluation? Deng, Zheng. 2021. CVPR. arXiv:2007.02915
Builds a meta-set of synthetically shifted datasets and regresses accuracy on a dataset-level distribution distance.
*Differs:* P2 estimates per-detection correctness and aggregates, with no meta-set.

**guillory2021doc** — Predicting with Confidence on Unseen Distributions. Guillory, Shankar, Ebrahimi et al. 2021. ICCV. arXiv:2107.03315
Difference-of-Confidences: predicts the accuracy drop from the drop in average confidence.
*Differs:* DoC is a global scalar correction; P2 conditions on a discrete provenance field.

**yu2022projnorm** — Predicting Out-of-Distribution Error with the Projection Norm. Yu, Yang, Wei et al. 2022. ICML PMLR 162. arXiv:2202.05834
Pseudo-labels the target, fine-tunes a copy, uses parameter distance as an accuracy proxy.
*Differs:* requires no retraining in P2, and ProjNorm is undefined for a non-differentiable classical engine.

**lu2023cot** — Characterizing Out-of-Distribution Error via Optimal Transport. Lu, Qin, Zhai et al. 2023. NeurIPS. arXiv:2305.15640
COT/COTT corrects the over-confidence bias of threshold methods via optimal transport against the estimated target label marginal.
*Differs:* OT over softmax vectors does not apply to a classical engine emitting a scalar match score.

**platanios2014estimating** — Estimating Accuracy from Unlabeled Data. Platanios, Blum, Mitchell. 2014. UAI.
Infers per-classifier error rates from agreement among several classifiers, with no labels at all.
*Differs:* P2 uses a small labelled reference set; note Platanios' setting is arguably *more* label-free than P2's.

**chen2021mandoline** — Mandoline: Model Evaluation under Distribution Shift. Chen, Goel, Sohoni et al. 2021. ICML PMLR 139. arXiv:2107.00643
Estimates target performance by reweighting a labelled validation set using user-written slicing functions.
*Differs:* only in the choice of slice. **The single most dangerous prior work for the stratification claim.**

**kivimaki2025confidence** — Confidence-based Estimators for Predictive Performance in Model Monitoring. Kivimäki, Nurminen, Białek, Kuberski. 2025. JAIR 82:209-240. doi:10.1613/jair.1.16709
Proves Average Confidence / CBPE is an unbiased, consistent accuracy estimator when the model is calibrated, derives confidence intervals, and shows the winner is use-case dependent.
*Differs:* not at all in kind. **This explains why our naive global-prior baseline beats our estimator: it is a theorem, not a bug.**

## Axis 3 - Calibration, selective prediction, abstention

**chow1970optimum** — On Optimum Recognition Error and Reject Tradeoff. Chow. 1970. IEEE Trans. Inf. Theory 16(1):41-46. doi:10.1109/TIT.1970.1054406
The optimal reject rule: abstain below a cost-derived threshold.
*Differs:* P2 *serves* the low-confidence region with a second engine rather than rejecting.

**geifman2017selective** — Selective Classification for Deep Neural Networks. Geifman, El-Yaniv. 2017. NeurIPS.
Selective classifier with a guaranteed risk bound at a chosen coverage.
*Differs:* P2's guarantees are about estimating batch accuracy post hoc, not bounding risk at prediction time.

**geifman2019selectivenet** — SelectiveNet. Geifman, El-Yaniv. 2019. ICML PMLR 97. arXiv:1901.09192
Joint prediction and selection heads for a target coverage.
*Differs:* no joint training; P2's fallback is an unmodified off-the-shelf classical algorithm.

**guo2017calibration** — On Calibration of Modern Neural Networks. Guo, Pleiss, Sun, Weinberger. 2017. ICML PMLR 70. arXiv:1706.04599
Modern DNNs are over-confident; temperature scaling largely fixes it.
*Differs:* P2 calibrates per stratum and must also calibrate a non-probabilistic classical score.

**lakshminarayanan2017deepensembles** — Deep Ensembles. Lakshminarayanan, Pritzel, Blundell. 2017. NeurIPS. arXiv:1612.01474
Independently trained ensembles give calibrated uncertainty and OOD robustness.
*Differs:* P2 uses one primary and one deterministic secondary, for cost and determinism rather than uncertainty quality.

**ovadia2019trust** — Can You Trust Your Model's Uncertainty? Ovadia, Fertig, Ren et al. 2019. NeurIPS. arXiv:1906.02530
Post-hoc calibration degrades badly under shift; ensembles hold up best.
*Differs:* motivation for per-stratum recalibration, and a threat to any single global calibration map.

**angelopoulos2021conformal** — A Gentle Introduction to Conformal Prediction. Angelopoulos, Bates. 2021. arXiv:2107.07511
Distribution-free prediction sets with finite-sample coverage from a calibration set.
*Differs:* P2 targets a batch accuracy point estimate. A reviewer will ask why conformal risk control was not used to put an interval on it.

**madras2018defer** — Predict Responsibly: Learning to Defer. Madras, Pitassi, Zemel. 2018. NeurIPS. arXiv:1711.06664
Learns when to defer to a downstream decision-maker, accounting for its error profile.
*Differs:* P2's deferral is reactive, not learned, and the downstream stage is an algorithm.

## Axis 4 - Reliability, graceful degradation, safety fallbacks

**phan2020neuralsimplex** — Neural Simplex Architecture. Phan, Paoletti, Zhang et al. 2020. NASA Formal Methods. doi:10.1007/978-3-030-55754-6_6
Pairs a learned neural controller with a verified classical baseline and a decision module that switches on imminent safety violation.
*Differs:* P2 switches on engine failure rather than a reachability check, and contributes accuracy accounting, not safety guarantees. **The clearest published cross-algorithm-class two-tier fallback.**

**ferreira2024safetymonitoring** — Safety Monitoring of Machine Learning Perception Functions: A Survey. Ferreira, Guérin, Delmas et al. 2025. Computational Intelligence. doi:10.1111/coin.70032
Surveys runtime safety monitors across threat identification, failure detection, reaction and evaluation.
*Differs:* P2 contributes an estimator, not a monitor; the survey's "reaction" taxonomy already covers degraded-mode fallback.

**daftry2016introspective** — Introspective Perception: Learning to Predict Failures in Vision Systems. Daftry, Zeng, Bagnell, Hebert. 2016. IROS. arXiv:1607.08665
Trains a model to predict when a vision system will fail.
*Differs:* P2 uses the recorded provenance and confidence of the executed path, not a separate learned failure predictor.

## Axis 5 - Reproducibility and nondeterminism

**chen2022reproducible** — Towards Training Reproducible Deep Learning Models. Chen, Wen, Shi et al. 2022. ICSE. doi:10.1145/3510003.3510163
Systematises software randomness and hardware nondeterminism; record-and-replay and profile-and-patch.
*Differs:* P2 uses non-reproducibility of the learned tier as motivation rather than trying to fix it.

**shanmugavelu2024fpna** — Impacts of Floating-Point Non-Associativity on Reproducibility. Shanmugavelu, Taillefumier, Culver et al. 2024. SC24 Workshops. doi:10.1109/SCW63240.2024.00028
Quantifies run-to-run variability from atomics and reduction order; evaluates PyTorch deterministic modes.
*Differs:* the evidence base for P2's determinism claim — **and also shows the primary can be made deterministic at a cost, which undercuts the claim as stated.**

## Axis 6 - Provenance, observability, production ML monitoring

**breck2017mltestscore** — The ML Test Score. Breck, Cai, Nielsen, Salib, Sculley. 2017. IEEE Big Data.
28-point production-readiness rubric.
*Differs:* P2 proposes an estimator, not a checklist — but the rubric already prescribes monitoring served predictions without labels.

**sculley2015debt** — Hidden Technical Debt in Machine Learning Systems. Sculley, Holt, Golovin et al. 2015. NeurIPS.
Names the maintenance anti-patterns of ML systems.
*Differs:* P2's shared record schema is a concrete answer to one anti-pattern, not a taxonomy.

**mitchell2019modelcards** — Model Cards for Model Reporting. Mitchell, Wu, Zaldivar et al. 2019. FAT*. arXiv:1810.03993
Documentation reporting performance disaggregated by group.
*Differs:* P2 disaggregates by inference path and estimates without labels at inference time.

**rabanser2019failingloudly** — Failing Loudly. Rabanser, Günnemann, Lipton. 2019. NeurIPS. arXiv:1810.11953
Benchmarks dimensionality reduction plus two-sample testing for shift detection.
*Differs:* P2 estimates how much accuracy was lost, not merely that shift occurred.

**gama2014drift** — A Survey on Concept Drift Adaptation. Gama, Žliobaitė, Bifet et al. 2014. ACM CSUR 46(4). doi:10.1145/2523813
Canonical taxonomy of drift detection and adaptation.
*Differs:* P2 assumes labels are unavailable; most detectors surveyed assume delayed-but-arriving labels.

## Axis 7 - ANPR / OCR mixing classical and deep

**vedhaviyassh2022easyocr** — Comparative Analysis of EasyOCR and TesseractOCR for ALPR. Vedhaviyassh, Sudhan, Saranya et al. 2022. ICECA.
YOLOv5 plate detection then Tesseract (~90%) vs EasyOCR (~95%) on the same crops.
*Differs:* P2 runs both as a fallback pair in one pipeline with a shared schema rather than choosing offline.

**hegghammer2022ocr** — OCR with Tesseract, Amazon Textract, and Google Document AI. Hegghammer. 2022. J. Computational Social Science 5(1):861-882. doi:10.1007/s42001-021-00149-1
18,568-document benchmark: Tesseract degrades far more than server OCR under injected noise.
*Differs:* P2 quantifies that gap in situ as the cost of the fallback path; this is the evidence the classical tier is materially weaker.

---

## (A) Closest prior art: the five a reviewer will raise

**1. kang2017noscope.** *Rebuttal:* NoScope's cheap stages are pure filters deciding whether to invoke the reference NN; they never produce the answer of record, are tuned against a labelled reference model, and the accuracy guarantee comes from held-out labels, not from unlabelled production data. *Concession:* NoScope already cascades a non-learned detector with learned CNNs under one output schema and an explicit accuracy budget. Cross-algorithm-class cascade in video analytics with a uniform output contract is materially present there, and P2 cannot claim it.

**2. chen2021mandoline.** *Rebuttal:* Mandoline needs a labelled validation set and estimates aggregate performance by density-ratio reweighting under a slice-based shift model; it does not calibrate a per-stratum confidence-to-correctness map, and its guarantees assume the slices capture the shift. *Concession:* slicing functions are arbitrary functions of input or prediction. "Which engine produced this record" is a legal slicing function. If a reviewer instantiates Mandoline that way, P2's stratification is a special case, and the honest framing is "we instantiate slice-based estimation with a provenance slice".

**3. garg2022atc.** *Rebuttal:* ATC is a single global threshold on one model's softmax; undefined for a deterministic engine with no probabilistic output, and with no mechanism for pooling heterogeneous confidence semantics. *Concession:* per-stratum ATC is a three-line change and is exactly P2's estimator in the learned-primary case. P2 must report it as a baseline; if it matches, the method contribution collapses to the provenance plumbing.

**4. kivimaki2025confidence.** *Rebuttal:* their unbiasedness result is conditional on calibration, and a mixture of two differently calibrated confidence sources violates the single-model assumption analysed. *Concession:* the paper proves Average Confidence is unbiased and consistent under calibration. That is exactly why our naive baseline wins at batch level. Any claim that stratification improves *batch-level* estimation must explain why, since stratification helps variance and conditional validity, not bias.

**5. phan2020neuralsimplex.** *Rebuttal:* Simplex switches on a safety condition to preserve an invariant and makes no claim about estimating accuracy of a mixed-provenance output stream; its baseline controller is verified, not merely deterministic. *Concession:* "learned primary, classical secondary, shared interface, explicit switch, and the secondary is the one you can reason about" is the entire Simplex idea, published since 1998 in control and 2020 for neural controllers. P2's architectural claim is a port of Simplex to perception and should be positioned as such.

---

## (B) Blunt verdict

**(i) Two-tier fallback across algorithm classes with a shared record schema: anticipated.** Not by one paper matching every detail, but the substance is published in at least three places — NoScope, the Simplex family, and the degraded-mode reaction type catalogued in Ferreira et al.'s survey. Do not claim it as novel. What is not published is the specific combination of (a) three heterogeneous entity types each with a classical counterpart, (b) fallback triggered by absence and empty result as well as exception, and (c) a per-detection provenance field carried into downstream analytics. That is an engineering contribution and a reviewer will call it that.

**(ii) Label-free accuracy estimation stratified by inference path: no exact prior work, but the gap is thin.** Mandoline already does slice-conditioned reweighted evaluation with arbitrary slicing functions; ATC, DoC, AC and COT are all trivially fittable per stratum. The stratified machinery exists and is general; "stratify by which engine ran" is a new instantiation, not a new estimator. Honest read: **not defensible as a methodological contribution at ICCV.** It is defensible as an empirical finding only if per-stratum calibration beats global calibration on a metric where it should — conditional error, or calibration error within the fallback stratum — not on batch accuracy, where the AC theorem says you should not expect to win.

**(iii) Unsolicited but load-bearing:** the bit-for-bit reproducibility claim is not novel either. That classical CV is deterministic and GPU DL inference is not is established (chen2022reproducible; shanmugavelu2024fpna), and the latter shows the primary *can* be made deterministic at a modest cost, which undercuts "the learned primary is not reproducible" as stated. Soften to "reproducible without the throughput cost of deterministic kernels" and cite the measurement.

---

## (C) The real state of the art in label-free accuracy estimation

There is no undisputed champion, and the picture is uncomfortable for P2.

**Tier 1, what we must beat and probably cannot at batch level:**
- **Average Confidence / CBPE** (kivimaki2025confidence). Our "naive global-prior baseline" in disguise, provably unbiased and consistent under calibration, with derived confidence intervals. Cite it, reproduce it, do not frame it as a strawman.
- **ATC** (garg2022atc). The strongest simple confidence method, 2-4x better than DoC/AC-style baselines across standard shifts. The default baseline every reviewer expects.

**Tier 2, genuine SOTA under higher assumptions:**
- **COT / COTT** (lu2023cot). Strongest recent single-model method; explicitly corrects ATC's over-confidence failure mode.
- **Agreement-on-the-Line** (baek2022agreement). Often the most accurate when an ensemble is affordable and the correlation holds.
- **Projection Norm** (yu2022projnorm). Competitive, uses a genuinely different (parameter-space) signal, but needs pseudo-label fine-tuning per batch and is impossible for the classical engine.

**Tier 3, closest to the stratified idea:**
- **Mandoline** (chen2021mandoline), run with the provenance field as a slicing function.
- **AutoEval** and **DoC**, historically important but now consistently outperformed by ATC/COT.

**Comparison table P2 must report:** AC/CBPE with JAIR confidence intervals, global ATC, per-stratum ATC, DoC, COT, and Mandoline-with-provenance-slices. If our estimator does not beat per-stratum ATC and AC, withdraw the estimator claim and reposition the paper around the systems contribution, with the estimation section reframed as a negative diagnostic result — which, given kivimaki2025confidence, is defensible and honest in its own right.
