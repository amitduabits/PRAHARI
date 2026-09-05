Research complete. All entries below were verified against Crossref, Scite, Consensus, or arXiv landing pages. **I dropped 6 candidates** whose DOIs I could not verify (Ellis/Makris/Black VS-PETS 2003 "Learning a multi-camera topology"; Chen et al. 2014 *Pattern Recognition* inter-camera transfer models; Newell 2013 SSRN ALPR paper; the 2019 AI City Challenge workshop paper; Huang et al. 2016 CNPR; Zou et al. 2007 ICIP).

---

# PRIOR ART: 33 VERIFIED ENTRIES

## Axis 1 — Cross-camera Re-ID with spatio-temporal / topology priors

**[javed2003tracking]** Tracking Across Multiple Cameras with Disjoint Views. Javed, Rasheed, Shafique, et al. 2003. *IEEE International Conference on Computer Vision* (ICCV), 952–957. `10.1109/iccv.2003.1238451`
Learns inter-camera topology and path probabilities with Parzen windows from unlabelled observations, then assigns correspondences by MAP — explicitly *without* inter-camera calibration.
*Difference:* Paper 3 outputs a ranked next-camera list rather than a correspondence assignment, and uses raw empirical counts rather than KDE.

**[javed2008modeling]** Modeling Inter-camera Space–Time and Appearance Relationships for Tracking Across Non-overlapping Views. Javed, Shafique, Rasheed, et al. 2008. *Computer Vision and Image Understanding* (CVIU) 109(2):146–162. `10.1016/j.cviu.2007.01.003`
Journal extension modelling entry/exit location, velocity and transition time as a joint density, plus a brightness-transfer subspace for appearance.
*Difference:* Paper 3 discards appearance entirely and assumes identity is given by the plate read.

**[wang2019streid]** Spatial-Temporal Person Re-Identification. Wang, Lai, Huang, et al. 2019. *AAAI Conference on Artificial Intelligence* (AAAI) 33:8933–8940. `10.1609/aaai.v33i01.33018933`
Estimates a camera-pair × transition-time histogram from training data and fuses it with visual similarity to prune the gallery; rank-1 98.1% on Market-1501.
*Difference:* Paper 3 uses the same empirical transition statistic as the *entire* model and as a forward predictor, not as a re-ranking prior.

**[lv2018tfusion]** Unsupervised Cross-dataset Person Re-identification by Transfer Learning of Spatial-Temporal Patterns. Lv, Chen, Li, et al. 2018. *IEEE/CVF Conference on Computer Vision and Pattern Recognition* (CVPR). arXiv:1803.07293
Learns the target camera network's spatio-temporal transition patterns unsupervised and fuses them with a transferred visual model via Bayesian fusion.
*Difference:* Paper 3 has no visual model to fuse and no transfer step.

**[shen2017vstpath]** Learning Deep Neural Networks for Vehicle Re-ID with Visual-spatio-Temporal Path Proposals. Shen, Xiao, Li, et al. 2017. *ICCV*, 1918–1927. `10.1109/iccv.2017.210`
Chain-MRF generates candidate visual-spatio-temporal paths through the camera network; a Siamese-CNN + Path-LSTM scores them.
*Difference:* Paper 3 predicts one step ahead with counts instead of scoring whole paths with a learned model.

**[zheng2021trajrecovery]** Towards Automated Spatio-Temporal Trajectory Recovery in Wide-Area Camera Networks. Zheng, Karanam, Radke, et al. 2021. *IEEE Transactions on Biometrics, Behavior, and Identity Science* (TBIOM) 3(1):59–71. `10.1109/tbiom.2020.3021655`
Reconstructs a person's time-stamped trajectory through a camera network using topology-informed transition-time modelling and candidate-space pruning; introduces the RPIfield dataset.
*Difference:* This is arguably the closest system-level prior work; Paper 3 differs mainly by using plates (no Re-ID uncertainty) and by ranking rather than reconstructing.

## Axis 2 — Camera network topology inference

**[makris2004bridging]** Bridging the Gaps Between Cameras. Makris, Ellis, Black. 2004. *CVPR* 2:205–210. `10.1109/cvpr.2004.1315165`
Unsupervised recovery of entry/exit zones and the links between them by accumulating temporal correlation of transitions across many observations, *without* solving correspondence; yields inter-camera transition-time distributions usable for predictive tracking.
*Difference:* Essentially none at the mechanism level (see section B).

**[tieu2005inference]** Inference of Non-overlapping Camera Network Topology by Measuring Statistical Dependence. Tieu, Dalley, Grimson. 2005. *ICCV* 2:1842–1849. `10.1109/iccv.2005.122`
Infers connectivity via non-parametric mutual information between cameras' observation streams with Bayesian integration over unknown correspondence; also recovers absolute camera locations from GPS side information.
*Difference:* Paper 3 assumes correspondence is solved (plates) and uses GPS as a fallback ranking rather than as a localisation target.

**[gilbert2006tracking]** Tracking Objects Across Cameras by Incrementally Learning Inter-camera Colour Calibration and Patterns of Activity. Gilbert, Bowden. 2006. *European Conference on Computer Vision* (ECCV), 125–136. `10.1007/11744047_10`
Incrementally and unsupervised learns posterior distributions of spatio-temporal links between uncalibrated non-overlapping cameras, improving online as evidence accumulates.
*Difference:* Paper 3's counting update is the same idea; Paper 3 adds no colour model.

**[marinakis2006practical]** A Practical Algorithm for Network Topology Inference. Marinakis, Dudek. 2006. *IEEE International Conference on Robotics and Automation* (ICRA), 3108–3115. `10.1109/robot.2006.1642174`
MCMC-based topology inference for a network of non-overlapping sensors from anonymous detection times alone.
*Difference:* Paper 3 uses frequency counts instead of sampling over correspondence hypotheses.

**[loy2010timedelayed]** Time-Delayed Correlation Analysis for Multi-Camera Activity Understanding. Loy, Xiang, Gong. 2010. *International Journal of Computer Vision* (IJCV) 90(1):106–129. `10.1007/s11263-010-0347-5`
Cross Canonical Correlation Analysis over 330 hours from 17 underground-station cameras infers spatial and temporal camera topology without any object tracking.
*Difference:* Paper 3 requires per-entity identity; Loy et al. deliberately do not.

**[cho2019joint]** Joint Person Re-identification and Camera Network Topology Inference in Multiple Cameras. Cho, Kim, Park, et al. 2019. *CVIU* 180:34–46. `10.1016/j.cviu.2019.01.003`
Unified framework that alternates Re-ID and topology inference online with minimal prior knowledge; releases the 9-camera SLP dataset.
*Difference:* Paper 3 solves only the topology/prediction half and does it offline from plate logs.

## Axis 3 — Next-location prediction and mobility predictability

**[gonzalez2008understanding]** Understanding Individual Human Mobility Patterns. González, Hidalgo, Barabási. 2008. *Nature* 453(7196):779–782. `10.1038/nature06958`
100k mobile-phone trajectories show strong spatial/temporal regularity and heavy return probability to a few frequented locations.
*Difference:* Paper 3 exploits this regularity operationally at camera granularity rather than characterising it.

**[song2010limits]** Limits of Predictability in Human Mobility. Song, Qu, Blumm, et al. 2010. *Science* 327(5968):1018–1021. `10.1126/science.1177170`
Entropy-rate + Fano analysis gives a 93% theoretical predictability ceiling for individual mobility.
*Difference:* Paper 3 should *use* this as its evaluation ceiling; it is not a competitor but a required yardstick.

**[lu2013approaching]** Approaching the Limit of Predictability in Human Mobility. Lu, Wetter, Bharti, et al. 2013. *Scientific Reports* 3:2923. `10.1038/srep02923`
Shows plain Markov-chain predictors reach 87–95% accuracy on 500k CDR trajectories, essentially saturating the entropy bound; higher-order chains add little.
*Difference:* This is the single most damaging baseline result for Paper 3's novelty — a first-order Markov chain on sparse traces is already known to be near-optimal.

**[gambs2012next]** Next Place Prediction Using Mobility Markov Chains. Gambs, Killijian, Núñez del Prado Cortez. 2012. *Workshop on Measurement, Privacy, and Mobility* (MPM), 1–6. `10.1145/2181196.2181199`
Defines the Mobility Markov Chain: cluster locations, count transitions, predict the next place by highest transition probability.
*Difference:* Paper 3's core mechanism is a Mobility Markov Chain where the states are cameras rather than clustered stay-points.

**[liu2016strnn]** Predicting the Next Location: A Recurrent Model with Spatial and Temporal Contexts. Liu, Wu, Wang, et al. 2016. *AAAI* 30(1). `10.1609/aaai.v30i1.9971`
ST-RNN adds time-interval-specific and distance-specific transition matrices to an RNN for next-location prediction.
*Difference:* Paper 3 is explicitly non-neural; ST-RNN is the obvious learned baseline a reviewer will demand.

**[feng2018deepmove]** DeepMove: Predicting Human Mobility with Attentional Recurrent Networks. Feng, Li, Zhang, et al. 2018. *The Web Conference* (WWW), 1459–1468. `10.1145/3178876.3186058`
Attentional recurrent network capturing multi-level periodicity from long, sparse, irregular mobility traces.
*Difference:* Same task, far heavier model; Paper 3's contribution can only be efficiency/interpretability, not accuracy.

**[yang2020flashback]** Location Prediction over Sparse User Mobility Traces Using RNNs: Flashback in Hidden States! Yang, Fankhauser, Rosso, et al. 2020. *International Joint Conference on Artificial Intelligence* (IJCAI), 2184–2190. `10.24963/ijcai.2020/302`
Searches past hidden states with similar spatio-temporal context; beats spatio-temporal RNNs by 15.9–27.6% on sparse traces.
*Difference:* Directly targets the sparsity regime Paper 3 claims as its niche, at IJCAI — the exact venue targeted.

**[ikanovic2017alternative]** An Alternative Approach to the Limits of Predictability in Human Mobility. Ikanovic, Mollgaard. 2017. *EPJ Data Science* 6(1). `10.1140/epjds/s13688-017-0107-7`
Shows the 90%+ predictability figures largely reflect stationarity of next-*bin* prediction; true next-*location* predictability is ~71%.
*Difference:* Paper 3 predicts next *camera* (a next-location task), so this is the correct ceiling to quote, not Song's 93%.

**[kulkarni2019examining]** Examining the Limits of Predictability of Human Mobility. Kulkarni, Mahalunkar, Garbinato, et al. 2019. *Entropy* 21(4):432. `10.3390/e21040432`
Argues the Fano-based upper bound is biased downward because mobility has long-range dependencies violating the Markov assumption; RNNs exceed it.
*Difference:* Directly attacks the assumption that a first-order transition table is near-optimal — cite it before a reviewer does.

## Axis 4 — Map inference and map matching (the alternative to assuming a road network)

**[newson2009hmm]** Hidden Markov Map Matching Through Noise and Sparseness. Newson, Krumm. 2009. *ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems* (SIGSPATIAL GIS), 336–343. `10.1145/1653771.1653818`
Canonical HMM map matcher; the standard "you have a road network, use it" method Paper 3 positions against.
*Difference:* Paper 3 needs no network; but note map matching degrades gracefully with sparsity, so this must be run as a real baseline.

**[biagioni2012inferring]** Inferring Road Maps from Global Positioning System Traces: Survey and Comparative Evaluation. Biagioni, Eriksson. 2012. *Transportation Research Record* (TRR) 2291(1):61–71. `10.3141/2291-08`
Surveys map-generation algorithms and gives the first automatic quantitative evaluation of inferred maps.
*Difference:* Establishes that "no road network" is solvable by *inferring* one; Paper 3 must argue why implicit transition counts beat inferring the map first.

**[ahmed2015comparison]** A Comparison and Evaluation of Map Construction Algorithms Using Vehicle Tracking Data. Ahmed, Karagiorgou, Pfoser, et al. 2015. *GeoInformatica* 19(3):601–632. `10.1007/s10707-014-0222-6`
Benchmarks seven map-construction algorithms on four datasets with four measures; open code and data at mapconstruction.org.
*Difference:* Supplies the evaluation methodology and the open baselines Paper 3's "no road network" claim needs to beat.

## Axis 5 — MTMC benchmarks and ALPR trajectory reconstruction

**[tang2019cityflow]** CityFlow: A City-Scale Benchmark for Multi-Target Multi-Camera Vehicle Tracking and Re-Identification. Tang, Naphade, Liu, et al. 2019. *CVPR*, 8789–8798. `10.1109/cvpr.2019.00900` / arXiv:1903.09254
40 cameras, 10 intersections, 2.5 km max separation, 229,680 boxes, 666 cross-camera vehicle identities, with homographies to a GPS-defined ground plane.
*Difference:* This is the dataset Paper 3 should be evaluated on, not a competitor.

**[ristani2016performance]** Performance Measures and a Data Set for Multi-target, Multi-camera Tracking. Ristani, Solera, Zou, et al. 2016. *ECCV Workshops*, 17–35. `10.1007/978-3-319-48881-3_2`
Introduces DukeMTMC (8 cameras, 2M frames, 2,700+ identities) and the ID-based IDF1/IDP/IDR measures.
*Difference:* Supplies the metric family a reviewer will expect; dataset is withdrawn (see section C).

**[zheng2015market1501]** Scalable Person Re-identification: A Benchmark. Zheng, Shen, Tian, et al. 2015. *ICCV*, 1116–1124. `10.1109/iccv.2015.133`
Market-1501: 6 cameras, 1,501 identities; defines the mAP + CMC protocol dominant in Re-ID.
*Difference:* No usable inter-camera geometry; only 6 cameras — too small to test Paper 3's topology claim.

**[zheng2017duke]** Unlabeled Samples Generated by GAN Improve the Person Re-identification Baseline in Vitro. Zheng, Zheng, Yang. 2017. *ICCV*, 3774–3782. `10.1109/iccv.2017.405`
The paper that introduced DukeMTMC-reID as a Re-ID benchmark split of DukeMTMC.
*Difference:* Provenance for the DukeMTMC-reID split, which carries the parent dataset's withdrawal problem.

**[liu2016veri]** A Deep Learning-Based Approach to Progressive Vehicle Re-identification for Urban Surveillance. Liu, Liu, Mei, et al. 2016. *ECCV*, 869–884. `10.1007/978-3-319-46475-6_53`
Introduces VeRi-776: 50,000+ images of 776 vehicles from 20 cameras over 1 km², with plate strings, timestamps, and inter-camera distances.
*Difference:* This is the closest thing to Paper 3's actual data modality that is publicly obtainable.

**[chavdarova2018wildtrack]** WILDTRACK: A Multi-camera HD Dataset for Dense Unscripted Pedestrian Detection. Chavdarova, Baqué, Bouquet, et al. 2018. *CVPR*, 5030–5039. `10.1109/cvpr.2018.00528`
7 calibrated, synchronised, heavily *overlapping* HD cameras on unscripted pedestrians.
*Difference:* Overlapping views make camera-to-camera transitions near-trivial; unsuitable for Paper 3's claim.

**[chen2015nlprmct]** An Equalised Global Graphical Model-Based Approach for Multi-camera Object Tracking. Chen, Cao, Chen, et al. 2015. arXiv:1502.03532
Method paper accompanying the NLPR_MCT benchmark and its MCTA metric for non-overlapping multi-camera tracking.
*Difference:* Provides the MCTA protocol and a small non-overlapping benchmark Paper 3 can use.

**[qi2021alprtraj]** Vehicle Trajectory Reconstruction on Urban Traffic Network Using Automatic License Plate Recognition Data. Qi, Ji, Li, et al. 2021. *IEEE Access* 9:49110–49120. `10.1109/access.2021.3068964`
Reconstructs sparse ALPR trajectories via space-time-prism K-shortest-paths plus an auto-encoder; 85% accuracy in Ningbo; identifies a ~50% minimum ALPR coverage rate.
*Difference:* This is the road-network camp on Paper 3's exact data type; Paper 3 must beat it, and this paper has real city data.

**[tong2021vetrac]** Large-Scale Vehicle Trajectory Reconstruction with Camera Sensing Network. Tong, Li, Li, et al. 2021. *ACM International Conference on Mobile Computing and Networking* (MobiCom), 188–200. `10.1145/3447993.3448617`
VeTrac: 7M+ vehicle snapshots from 1,000+ traffic cameras; fuses mobility correlation with vision and a graph-convolution identity-consistency step; 89% in complex urban settings.
*Difference:* Uses far more machinery and does align to a road network, but demonstrates the real-data scale Paper 3 currently lacks.

## Axis 6 — Kalman / constant-velocity tracking baselines

**[bewley2016sort]** Simple Online and Realtime Tracking. Bewley, Ge, Ott, et al. 2016. *IEEE International Conference on Image Processing* (ICIP), 3464–3468. `10.1109/icip.2016.7533003` / arXiv:1602.00763
Kalman filter + Hungarian assignment at 260 Hz; the canonical constant-velocity motion-model tracker.
*Difference:* SORT is a within-view tracker; extending it across non-overlapping views is exactly where the linear-motion assumption dies.

**[wojke2017deepsort]** Simple Online and Realtime Tracking with a Deep Association Metric. Wojke, Bewley, Paulus. 2017. *ICIP*, 3645–3649. `10.1109/icip.2017.8296962` / arXiv:1703.07402
Adds a learned appearance metric to SORT, cutting ID switches 45% and surviving longer occlusions.
*Difference:* Its gain comes from appearance, tacitly conceding the Kalman motion model fails over long gaps — cite this as evidence for Paper 3's premise.

**[zhang2022bytetrack]** ByteTrack: Multi-Object Tracking by Associating Every Detection Box. Zhang, Sun, Jiang, et al. 2022. *ECCV*. arXiv:2110.06864
Associates low-confidence boxes too; 80.3 MOTA / 77.3 IDF1 on MOT17, still on a Kalman motion prior.
*Difference:* Current strong motion-model baseline; Paper 3 needs it in the comparison table to make the "no Kalman" claim credible.

## Axis 7 — Predictive policing and ANPR analytics/ethics

**[perry2013predictive]** Predictive Policing: The Role of Crime Forecasting in Law Enforcement Operations. Perry, McInnis, Price, et al. 2013. RAND Corporation. `10.7249/rr233`
Foundational survey of crime-forecasting methods and their operational pitfalls, including the "focus on prediction accuracy instead of tactic" failure mode.
*Difference:* Frames why a top-k next-camera ranking is not automatically an operational good.

**[lum2016predict]** To Predict and Serve? Lum, Isaac. 2016. *Significance* 13(5):14–19. `10.1111/j.1740-9713.2016.00960.x`
Shows PredPol trained on police-recorded data diverges from true crime rates, repeatedly re-targeting the same neighbourhoods.
*Difference:* Direct analogue: transition frequencies learned from where cameras happen to be will reproduce the deployment's existing biases.

**[ensign2018runaway]** Runaway Feedback Loops in Predictive Policing. Ensign, Friedler, Neville, et al. 2018. *Conference on Fairness, Accountability and Transparency* (FAT*). arXiv:1706.09847
Urn-model proof that discovery-driven allocation converges to over-policing one region, with proposed corrective interventions.
*Difference:* Gives Paper 3 a formal, citable mechanism for its limitations section.

**[pereira2022banal]** From Banal Surveillance to Function Creep: Automated License Plate Recognition (ALPR) in Denmark. Pereira, Raetzsch. 2022. *Surveillance & Society* 20(3):265–280. `10.24908/ss.v20i3.15000`
Ethnography of ALPR across parking, environmental zoning and policing; documents dragnet expansion with little public oversight and argues function creep is embedded in the infrastructure.
*Difference:* The strongest available citation for "this method makes plate-network analytics cheaper, which is itself the risk."

**[hadavi2020anpr]** Analyzing Passenger and Freight Vehicle Movements from Automatic-Number Plate Recognition Camera Data. Hadavi, Buldeo Rai, Verlinde, et al. 2020. *European Transport Research Review* (ETRR) 12(1). `10.1186/s12544-020-00405-x`
Methodology for turning raw ANPR logs from 122 cameras over two weeks into movement/stop knowledge, validated against HGV GPS.
*Difference:* Establishes the ANPR-network analytics genre and, usefully, the validation-against-GPS pattern Paper 3 could copy.

---

# (A) THE FIVE WORKS A REVIEWER WILL SAY ANTICIPATE THIS

### 1. Makris, Ellis & Black 2004 — *Bridging the Gaps Between Cameras*
**Rebuttal:** Makris et al. solve *structure recovery* — they output a topology graph and transition-time distributions as the end product, evaluated by whether recovered links match ground-truth adjacency. Paper 3 solves a *decision* problem: given a live last-seen event, produce a ranked list of cameras with an operational latency budget and a cold-start policy. They never evaluate top-k next-camera accuracy, and they have no fallback for a camera with zero outgoing history.
**Concession:** The estimator is the same object. If you strip the framing, "accumulate transitions out of camera *i*, normalise, rank" is precisely what their link-strength accumulation computes. Claiming the *mechanism* as novel is not defensible; only the task framing and the fallback are.

### 2. Gambs, Killijian & Núñez del Prado Cortez 2012 — *Next Place Prediction Using Mobility Markov Chains*
**Rebuttal:** MMC operates on GPS stay-points clustered into places, where the state space is discovered and per-user. Paper 3's states are physically fixed sensors with known coordinates and a *global* (not per-entity) transition table, which changes the data regime: cold-start is a camera property, not a user property, and the GIS fallback has no MMC analogue.
**Concession:** "Count transitions between discretised locations, rank the next one by frequency" is verbatim the MMC algorithm. A reviewer can fairly say Paper 3 = MMC with cameras as places. The honest positioning is "MMC applied to a sensor network", not "a new model."

### 3. Lu, Wetter, Bharti et al. 2013 — *Approaching the Limit of Predictability in Human Mobility*
**Rebuttal:** Their 87–95% figures are on CDR traces with dense temporal sampling and per-user models trained on months of history; camera estates give far shorter per-plate histories and a much larger, more irregular state space. Their result does not transfer without evidence.
**Concession:** They already showed that a first-order Markov chain essentially saturates the entropy bound and that higher order buys nothing. This is the strongest evidence that Paper 3's central positive result is *expected*, not surprising. If Paper 3 reports "frequency counting works well," the response is "yes, we knew that since 2013."

### 4. Cho, Kim, Park et al. 2019 — *Joint Person Re-ID and Camera Network Topology Inference*
**Rebuttal:** Cho et al. need topology inference because Re-ID is uncertain — the two problems are coupled and solved jointly, which is expensive and requires appearance models. Paper 3's setting (plate reads) decouples them, which is a genuinely different and much cheaper regime, and permits deployment on estates where no Re-ID model has been trained.
**Concession:** They explicitly state topology "is also difficult to automatically estimate" and then estimate it from transitions with minimal prior knowledge — the same claim of "no calibration, no map, no prior connectivity" Paper 3 makes. The "unknown connectivity" novelty framing is already taken.

### 5. Zheng, Karanam & Radke 2021 — *Towards Automated Spatio-Temporal Trajectory Recovery in Wide-Area Camera Networks*
**Rebuttal:** They reconstruct a *complete past* trajectory offline for forensic review; Paper 3 ranks the *next* camera for prospective interception. Their evaluation metrics are trajectory-recovery metrics, not top-k ranking metrics, and their candidate pruning presumes a topology supplied rather than learned from scratch.
**Concession:** They already combine "topology-informed transition time modelling" with "candidate space pruning" and motivate it exactly as Paper 3 does — an operator following a person of interest through a network. The gap between "recover the trajectory" and "rank the next camera" is thin, and a reviewer can reasonably call it an evaluation-protocol difference rather than a contribution.

---

# (B) IS CAMERA-TOPOLOGY INFERENCE FROM TRANSITION FREQUENCY ALREADY PUBLISHED?

**Yes. Unambiguously. Your suspicion is correct, and the papers are older and closer than you fear.** As a mechanism it is a solved problem with a twenty-year literature. Here is exactly what was done:

- **Makris, Ellis & Black (CVPR 2004)** automatically extract entry/exit zones per camera view, then establish links between them by *accumulating evidence from many trajectory observations* of temporal co-occurrence. Their stated benefit is that the method "doesn't rely on establishing correspondence between trajectories," and the by-product is "a measure of inter-camera transition times, which can be used to support predictive tracking across the camera network." That last clause is Paper 3's thesis, published in 2004.

- **Tieu, Dalley & Grimson (ICCV 2005)** generalise this: two cameras are connected iff departures from one statistically depend on arrivals at the other, measured by non-parametric mutual information with Bayesian marginalisation over unknown correspondence. They explicitly note prior work "assumed restricted parametric transition distributions" — i.e. the frequency/histogram approach was already the thing being generalised in 2005. They *also* fold in GPS side information to recover absolute camera locations.

- **Javed et al. (ICCV 2003; CVIU 2008)** learn inter-camera space-time relationships as a probability density over entry/exit location, velocity and transition time from unlabelled training video, with no calibration, and use it predictively for correspondence.

- **Gilbert & Bowden (ECCV 2006)** do it *incrementally and online*, so the transition posteriors improve as evidence accumulates — the "learn from the stream, no batch training" property.

- **Marinakis & Dudek (ICRA 2006)** infer network topology from anonymous detection times alone via MCMC.

- **Loy, Xiang & Gong (IJCV 2010)** do it at scale (17 cameras, 330 hours) with cross-canonical correlation and no tracking at all.

- **Cho et al. (CVIU 2019)** and **Chen et al. (Pattern Recognition, 2014 line of work)** carry it into the deep-Re-ID era.

- Separately, **Gambs et al. (2012)** publish the identical estimator under the name Mobility Markov Chain in the mobility community, and **Lu et al. (2013)** show it is near information-theoretically optimal on sparse traces.

**What is left as novel — honestly:**

1. **Nothing at the mechanism level.** "Rank next camera by empirical transition frequency out of the last-seen camera" is prior art in at least two independent literatures. Do not claim it as the contribution. If the paper's stated contribution is the mechanism, it will be desk-rejected or shredded by any reviewer who knows the Makris/Tieu line.

2. **The great-circle fallback is a small, honest engineering contribution** — I found no paper that specifies and evaluates a distance-based cold-start policy for zero-history cameras as an explicit, ablated component. This is a paragraph, not a paper.

3. **The task framing is defensible but thin.** Prospective top-k next-camera ranking, evaluated with ranking metrics under a deployment-realistic temporal split, is not a standard task with a standard benchmark. Formalising it and releasing a protocol is a real (if modest) contribution — but only if you release the protocol and real data.

4. **The empirical claim is the only thing that can carry the paper.** "On irregular deployments this beats road-network and motion-model methods" is a falsifiable, non-obvious, *useful* claim. But it is currently supported by synthetic traces, which is worth zero. Against Qi et al. 2021 (real Ningbo ALPR, 85%) and Tong et al. 2021 (real 1,000-camera deployment, 89%), a synthetic-trace result will not be believed.

5. **A genuinely novel angle you have not claimed but could:** a *characterisation* result — identify the deployment-geometry regime (camera density, road-network irregularity, coverage rate) in which the implicit transition model provably or empirically dominates map-based reconstruction, and where it collapses. That reframes the paper from "we propose a method" (indefensible) to "we establish when the simple method is sufficient" (defensible, and a genuine IJCAI/AAMAS-shaped contribution). Lu et al. and Kulkarni et al. give you the theoretical scaffolding; Ahmed et al. gives you the map-inference baselines.

**Bottom line:** reposition the paper as an empirical study with a strong-baseline-beats-complex-machinery result plus a regime characterisation, on real data, and cite Makris/Tieu/Javed/Gambs in the *first paragraph* as what you are reproducing at scale rather than in a related-work paragraph as what you differ from. If the paper claims mechanism novelty, it will not survive review.

---

# (C) REAL PUBLIC DATASETS YOU COULD USE INSTEAD OF SYNTHETIC TRACES

Ranked by fitness for this specific task.

### 1. CityFlow / CityFlowV2 — **best fit**
- **Contains:** 40 cameras across 10 intersections, >3 hours synchronised 1080p, 229,680 boxes, 666 vehicle identities each crossing ≥2 cameras, max inter-camera separation 2.5 km.
- **Camera GPS:** **Yes.** The paper provides "homography matrices between the 2D image plane and the ground plane defined by GPS coordinates based on the flat-earth approximation," with landmark GPS taken from Google Maps. This gives you real camera coordinates for your great-circle fallback — no synthesis needed.
- **Cross-camera transitions:** **Yes**, explicitly — identities are defined as crossing at least two cameras, and per-video start-time offsets are given for synchronisation.
- **Access:** AI City Challenge dataset request form plus a per-track data licence agreement; research use, no redistribution. Historically requires an institutional email and signed agreement.
- **Caveat:** 40 cameras at 10 intersections is a *regular* grid-like deployment — the opposite of the irregular estates the paper claims to serve. It tests the mechanism but not the claim. Use it as your primary quantitative benchmark and be explicit that it is a hard case for your thesis.

### 2. VeRi-776 — **best fit for the plate modality**
- **Contains:** 50,000+ images of 776 vehicles from 20 real surveillance cameras over a 1.0 km² area in 24 hours, with vehicle type/colour/brand, **licence plate bounding boxes and plate strings**, and — critically — **timestamps and distances between neighbouring cameras**.
- **Camera GPS:** Not distributed as raw lat/long, but inter-camera **distances** are provided, which is sufficient to instantiate a distance-based fallback ranking (and arguably a better test of it than GPS, since it removes great-circle-vs-road-distance confounding).
- **Cross-camera transitions:** **Yes** — this is the design purpose; vehicles are observed across 2–18 cameras.
- **Access:** Email request to the maintainer with full name and affiliation; **non-commercial research only, no redistribution to third parties, no public reposting**.
- **Why it matters:** 20 cameras with real plate strings and real transition times is the closest public analogue to your actual operational data. This should be your headline dataset.

### 3. NLPR_MCT
- **Contains:** Four non-overlapping multi-camera sub-datasets (3–5 cameras each) with cross-camera person trajectories; ships with the MCTA metric.
- **Camera GPS:** No.
- **Cross-camera transitions:** Yes, non-overlapping by construction — the topology-relevant property.
- **Access:** Publicly distributed for research via the benchmark site; the accompanying method paper is arXiv:1502.03532.
- **Caveat:** Very small (≤5 cameras). Useful only as a sanity check, not for a topology claim.

### 4. DukeMTMC / DukeMTMC-reID — **do not use, and say why in the paper**
- **Contains:** 8 cameras, 2M+ frames at 1080p/60fps, 2,700+ identities over 85 minutes, fully calibrated with a ground plane.
- **Camera GPS:** Ground-plane calibration, campus-local, not global GPS.
- **Cross-camera transitions:** Yes, and very well annotated.
- **Access:** **Withdrawn.** Duke University terminated the dataset in June 2019 after Financial Times and Exposing.ai reporting that it had been used by Chinese military-linked institutions and surveillance vendors for Uyghur monitoring. The official site is down; mirrors circulate but there is no valid licence.
- **Recommendation:** Do not evaluate on it. Given that Paper 3 is a police-surveillance method with a misuse section, using a dataset withdrawn *for surveillance misuse* would be a self-inflicted wound in review. Cite Ristani et al. for the IDF1 metric only, and state explicitly that you declined to use the data.

### 5. WILDTRACK — poor fit
- **Contains:** 7 synchronised, calibrated HD cameras, unscripted dense pedestrian scenes.
- **Camera GPS:** Full extrinsic/intrinsic calibration, single scene.
- **Cross-camera transitions:** Heavily **overlapping** fields of view — there are no meaningful blind-gap transitions.
- **Access:** Public via EPFL for research.
- **Verdict:** Skip. Overlapping FOVs make the prediction task degenerate.

### 6. Market-1501 — poor fit
- 6 cameras, 1,501 identities, no usable inter-camera geometry, single campus location. Too few cameras to say anything about topology. Useful only if you want to reproduce the st-ReID spatio-temporal-prior result as a sanity check.

### 7. mapconstruction.org (Ahmed et al.)
- Not a camera dataset, but the **open GPS-trace datasets, ground-truth maps, and seven implemented map-construction algorithms** you need to run a credible "road-network method" baseline rather than a strawman.

### 8. Additional real-data option worth pursuing
- The **ALPR trajectory-reconstruction papers** (Qi et al. 2021, Ningbo; Rao et al. 2018, Kunshan; Tong et al. 2021, VeTrac) use real city ALPR feeds. Those datasets are generally not public, but the papers report enough network statistics (camera counts, coverage rates, accuracy vs coverage curves) that you can (a) match their experimental design and (b) contact the authors. Qi et al.'s finding of a ~50% minimum ALPR coverage rate is a specific number you should replicate or contradict.

**Blunt assessment:** synthetic traces are fatal here, because the entire claim is about *deployment irregularity* — a property of real estates that a generative model cannot honestly produce, since you would be choosing the irregularity that your method handles. CityFlow + VeRi-776 are both obtainable within days by email/form. There is no defensible reason to submit this on synthetic data.

---

# (D) METRICS AND EVALUATION PROTOCOL A REVIEWER WILL EXPECT

**Primary metrics (ranking task).** Report all of:
- **Top-k accuracy / Hit@k** for k ∈ {1, 3, 5} — k=3 and k=5 matter operationally because an interception team can cover a few cameras.
- **MRR (mean reciprocal rank)** — the single number that will be compared across papers.
- **Mean rank** and **median rank**, plus the full CMC-style curve over all cameras.
- **Macro-average over cameras**, not just micro-average over events. A micro-average is dominated by a few busy cameras and will flatter the method; a reviewer who has read Lum & Isaac will ask for the per-camera breakdown.

**Secondary / diagnostic.**
- **Negative log-likelihood or perplexity** of the true next camera under the predicted distribution — this tests calibration, not just ranking, and distinguishes you from a system that gets rank-1 right by luck on a few hub cameras.
- **Normalised predictability vs. the entropy bound.** Compute the Fano-style upper bound on your camera-sequence data (Song et al. 2010 method) and report how close you get, but use the **next-location** framing not next-bin (Ikanovic & Mollgaard 2017), and acknowledge the long-range-dependency critique (Kulkarni et al. 2019). Reviewers in the mobility community will insist on this; it is also your best defence of "why a simple counter suffices."
- **Cold-start rate:** fraction of queries that hit the GIS fallback, and top-k accuracy conditioned on fallback vs non-fallback. Without this the fallback is unevaluated.
- **Time-to-next-observation calibration** if you predict timing at all.

**If you frame any part as tracking or Re-ID, expect additionally:**
- **IDF1 / IDP / IDR** (Ristani et al. 2016) — now the default for MTMC.
- **MOTA / MOTP / ID switches** for the single-camera components.
- **MCTA** (NLPR_MCT) for non-overlapping cross-camera tracking.
- **mAP and CMC rank-1/rank-5** if you touch Re-ID at all.

**Baselines a reviewer will demand — you must include all six tiers:**
1. Uniform random over cameras (floor).
2. **Global popularity prior** — rank by each camera's marginal detection frequency, ignoring the last-seen camera entirely. This is the baseline that most often kills transition-model papers; if your method does not clearly beat it, there is no paper.
3. **Distance-only** — great-circle ranking with no transition history (your fallback used alone). Isolates how much the transition table actually adds.
4. **First-order and second-order Markov / MMC** (Gambs et al.), including a smoothed variant (Laplace / Kneser-Ney) — because raw counts on sparse data are a known failure mode and a reviewer will ask why you didn't smooth.
5. **Learned sequence models** — ST-RNN (Liu et al. 2016), DeepMove (Feng et al. 2018), Flashback (Yang et al. 2020). At IJCAI, omitting Flashback in particular is not survivable: it targets sparse traces, it is your venue, and it is the obvious "but a neural model does better" question.
6. **Road-network / motion-model methods** — HMM map matching (Newson & Krumm) on an OSM network, plus a constant-velocity/Kalman predictor (SORT-style) extended across views, plus at least one map-*inference*-then-match pipeline from Ahmed et al.'s open implementations. Your headline claim is that you beat these; a strawman version will be spotted.

**Protocol requirements:**
- **Temporal split, never random.** Train on an earlier window, test on a strictly later one. Random splits leak the transition table into the test set and are the single most common fatal flaw in this genre.
- **Report coverage/sparsity sweeps.** Subsample detections to simulate 20/40/60/80/100% camera coverage and plot accuracy vs coverage — Qi et al. found a ~50% cliff; either you have one too, or your robustness claim is a real finding.
- **Stratify by camera history depth.** Accuracy on cameras with <10, 10–100, >100 outgoing observations. The whole cold-start argument lives or dies here.
- **Stratify by deployment regularity.** This is the paper's actual claim. You need at least two estates (or two sub-regions) that differ measurably in regularity, with a stated quantitative measure of irregularity (e.g. deviation of camera adjacency from road-network adjacency, or entropy of the transition matrix).
- **Ablate the fallback.** With/without GIS fallback, and with alternative fallbacks (popularity prior, nearest-neighbour-only).
- **Statistical significance.** Bootstrap CIs over test events, and a paired test against the strongest baseline. Reviewers at AAMAS in particular will ask.
- **Runtime and memory**, since "simple beats complex" is half your argument.
- **Reproducibility:** release the transition tables and evaluation code even if the raw plate data cannot be released.

---

# (E) BIBTEX

```bibtex
@inproceedings{javed2003tracking,
  author    = {Javed, Omar and Rasheed, Zeeshan and Shafique, Khurram and Shah, Mubarak},
  title     = {Tracking Across Multiple Cameras with Disjoint Views},
  booktitle = {Proceedings of the Ninth IEEE International Conference on Computer Vision (ICCV)},
  pages     = {952--957},
  year      = {2003},
  doi       = {10.1109/ICCV.2003.1238451}
}

@article{javed2008modeling,
  author  = {Javed, Omar and Shafique, Khurram and Rasheed, Zeeshan and Shah, Mubarak},
  title   = {Modeling Inter-camera Space--Time and Appearance Relationships for Tracking Across Non-overlapping Views},
  journal = {Computer Vision and Image Understanding (CVIU)},
  volume  = {109},
  number  = {2},
  pages   = {146--162},
  year    = {2008},
  doi     = {10.1016/j.cviu.2007.01.003}
}

@inproceedings{wang2019streid,
  author    = {Wang, Guangcong and Lai, Jianhuang and Huang, Peigen and others},
  title     = {Spatial-Temporal Person Re-Identification},
  booktitle = {Proceedings of the AAAI Conference on Artificial Intelligence (AAAI)},
  volume    = {33},
  number    = {01},
  pages     = {8933--8940},
  year      = {2019},
  doi       = {10.1609/aaai.v33i01.33018933}
}

@inproceedings{lv2018tfusion,
  author    = {Lv, Jianming and Chen, Weihang and Li, Qing and others},
  title     = {Unsupervised Cross-dataset Person Re-identification by Transfer Learning of Spatial-Temporal Patterns},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year      = {2018},
  eprint    = {1803.07293},
  archivePrefix = {arXiv},
  doi       = {10.48550/arXiv.1803.07293}
}

@inproceedings{shen2017vstpath,
  author    = {Shen, Yantao and Xiao, Tong and Li, Hongsheng and others},
  title     = {Learning Deep Neural Networks for Vehicle Re-ID with Visual-spatio-Temporal Path Proposals},
  booktitle = {Proceedings of the IEEE International Conference on Computer Vision (ICCV)},
  pages     = {1918--1927},
  year      = {2017},
  doi       = {10.1109/ICCV.2017.210}
}

@article{zheng2021trajrecovery,
  author  = {Zheng, Meng and Karanam, Srikrishna and Radke, Richard J. and others},
  title   = {Towards Automated Spatio-Temporal Trajectory Recovery in Wide-Area Camera Networks},
  journal = {IEEE Transactions on Biometrics, Behavior, and Identity Science (TBIOM)},
  volume  = {3},
  number  = {1},
  pages   = {59--71},
  year    = {2021},
  doi     = {10.1109/TBIOM.2020.3021655}
}

@inproceedings{makris2004bridging,
  author    = {Makris, Dimitrios and Ellis, Tim and Black, James},
  title     = {Bridging the Gaps Between Cameras},
  booktitle = {Proceedings of the IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR)},
  volume    = {2},
  pages     = {205--210},
  year      = {2004},
  doi       = {10.1109/CVPR.2004.1315165}
}

@inproceedings{tieu2005inference,
  author    = {Tieu, Kinh and Dalley, Gerald and Grimson, W. Eric L.},
  title     = {Inference of Non-overlapping Camera Network Topology by Measuring Statistical Dependence},
  booktitle = {Proceedings of the Tenth IEEE International Conference on Computer Vision (ICCV)},
  volume    = {2},
  pages     = {1842--1849},
  year      = {2005},
  doi       = {10.1109/ICCV.2005.122}
}

@inproceedings{gilbert2006tracking,
  author    = {Gilbert, Andrew and Bowden, Richard},
  title     = {Tracking Objects Across Cameras by Incrementally Learning Inter-camera Colour Calibration and Patterns of Activity},
  booktitle = {Proceedings of the European Conference on Computer Vision (ECCV)},
  pages     = {125--136},
  year      = {2006},
  doi       = {10.1007/11744047_10}
}

@inproceedings{marinakis2006practical,
  author    = {Marinakis, Dimitri and Dudek, Gregory},
  title     = {A Practical Algorithm for Network Topology Inference},
  booktitle = {Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)},
  pages     = {3108--3115},
  year      = {2006},
  doi       = {10.1109/ROBOT.2006.1642174}
}

@article{loy2010timedelayed,
  author  = {Loy, Chen Change and Xiang, Tao and Gong, Shaogang},
  title   = {Time-Delayed Correlation Analysis for Multi-Camera Activity Understanding},
  journal = {International Journal of Computer Vision (IJCV)},
  volume  = {90},
  number  = {1},
  pages   = {106--129},
  year    = {2010},
  doi     = {10.1007/s11263-010-0347-5}
}

@article{cho2019joint,
  author  = {Cho, Yeong-Jun and Kim, Su-A and Park, Jae-Han and others},
  title   = {Joint Person Re-identification and Camera Network Topology Inference in Multiple Cameras},
  journal = {Computer Vision and Image Understanding (CVIU)},
  volume  = {180},
  pages   = {34--46},
  year    = {2019},
  doi     = {10.1016/j.cviu.2019.01.003}
}

@article{gonzalez2008understanding,
  author  = {Gonz{\'a}lez, Marta C. and Hidalgo, C{\'e}sar A. and Barab{\'a}si, Albert-L{\'a}szl{\'o}},
  title   = {Understanding Individual Human Mobility Patterns},
  journal = {Nature},
  volume  = {453},
  number  = {7196},
  pages   = {779--782},
  year    = {2008},
  doi     = {10.1038/nature06958}
}

@article{song2010limits,
  author  = {Song, Chaoming and Qu, Zehui and Blumm, Nicholas and Barab{\'a}si, Albert-L{\'a}szl{\'o}},
  title   = {Limits of Predictability in Human Mobility},
  journal = {Science},
  volume  = {327},
  number  = {5968},
  pages   = {1018--1021},
  year    = {2010},
  doi     = {10.1126/science.1177170}
}

@article{lu2013approaching,
  author  = {L{\"u}, Xin and Wetter, Erik and Bharti, Nita and others},
  title   = {Approaching the Limit of Predictability in Human Mobility},
  journal = {Scientific Reports},
  volume  = {3},
  number  = {1},
  pages   = {2923},
  year    = {2013},
  doi     = {10.1038/srep02923}
}

@inproceedings{gambs2012next,
  author    = {Gambs, S{\'e}bastien and Killijian, Marc-Olivier and N{\'u}{\~n}ez del Prado Cortez, Miguel},
  title     = {Next Place Prediction Using Mobility Markov Chains},
  booktitle = {Proceedings of the First Workshop on Measurement, Privacy, and Mobility (MPM)},
  pages     = {1--6},
  year      = {2012},
  doi       = {10.1145/2181196.2181199}
}

@inproceedings{liu2016strnn,
  author    = {Liu, Qiang and Wu, Shu and Wang, Liang and Tan, Tieniu},
  title     = {Predicting the Next Location: A Recurrent Model with Spatial and Temporal Contexts},
  booktitle = {Proceedings of the AAAI Conference on Artificial Intelligence (AAAI)},
  volume    = {30},
  number    = {1},
  year      = {2016},
  doi       = {10.1609/aaai.v30i1.9971}
}

@inproceedings{feng2018deepmove,
  author    = {Feng, Jie and Li, Yong and Zhang, Chao and Sun, Funing and Meng, Fanchao and Guo, Ang and Jin, Depeng},
  title     = {DeepMove: Predicting Human Mobility with Attentional Recurrent Networks},
  booktitle = {Proceedings of the 2018 World Wide Web Conference (WWW)},
  pages     = {1459--1468},
  year      = {2018},
  doi       = {10.1145/3178876.3186058}
}

@inproceedings{yang2020flashback,
  author    = {Yang, Dingqi and Fankhauser, Benjamin and Rosso, Paolo and others},
  title     = {Location Prediction over Sparse User Mobility Traces Using RNNs: Flashback in Hidden States!},
  booktitle = {Proceedings of the Twenty-Ninth International Joint Conference on Artificial Intelligence (IJCAI)},
  pages     = {2184--2190},
  year      = {2020},
  doi       = {10.24963/ijcai.2020/302}
}

@article{ikanovic2017alternative,
  author  = {Ikanovic, Edin Lind and Mollgaard, Anders},
  title   = {An Alternative Approach to the Limits of Predictability in Human Mobility},
  journal = {EPJ Data Science},
  volume  = {6},
  number  = {1},
  year    = {2017},
  doi     = {10.1140/epjds/s13688-017-0107-7}
}

@article{kulkarni2019examining,
  author  = {Kulkarni, Vaibhav and Mahalunkar, Abhijit and Garbinato, Beno{\^i}t and others},
  title   = {Examining the Limits of Predictability of Human Mobility},
  journal = {Entropy},
  volume  = {21},
  number  = {4},
  pages   = {432},
  year    = {2019},
  doi     = {10.3390/e21040432}
}

@inproceedings{newson2009hmm,
  author    = {Newson, Paul and Krumm, John},
  title     = {Hidden Markov Map Matching Through Noise and Sparseness},
  booktitle = {Proceedings of the 17th ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems (SIGSPATIAL GIS)},
  pages     = {336--343},
  year      = {2009},
  doi       = {10.1145/1653771.1653818}
}

@article{biagioni2012inferring,
  author  = {Biagioni, James and Eriksson, Jakob},
  title   = {Inferring Road Maps from Global Positioning System Traces: Survey and Comparative Evaluation},
  journal = {Transportation Research Record (TRR)},
  volume  = {2291},
  number  = {1},
  pages   = {61--71},
  year    = {2012},
  doi     = {10.3141/2291-08}
}

@article{ahmed2015comparison,
  author  = {Ahmed, Mahmuda and Karagiorgou, Sophia and Pfoser, Dieter and Wenk, Carola},
  title   = {A Comparison and Evaluation of Map Construction Algorithms Using Vehicle Tracking Data},
  journal = {GeoInformatica},
  volume  = {19},
  number  = {3},
  pages   = {601--632},
  year    = {2015},
  doi     = {10.1007/s10707-014-0222-6}
}

@inproceedings{tang2019cityflow,
  author    = {Tang, Zheng and Naphade, Milind and Liu, Ming-Yu and others},
  title     = {CityFlow: A City-Scale Benchmark for Multi-Target Multi-Camera Vehicle Tracking and Re-Identification},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages     = {8789--8798},
  year      = {2019},
  doi       = {10.1109/CVPR.2019.00900}
}

@inproceedings{ristani2016performance,
  author    = {Ristani, Ergys and Solera, Francesco and Zou, Roger S. and Cucchiara, Rita and Tomasi, Carlo},
  title     = {Performance Measures and a Data Set for Multi-target, Multi-camera Tracking},
  booktitle = {Computer Vision -- ECCV 2016 Workshops},
  pages     = {17--35},
  year      = {2016},
  doi       = {10.1007/978-3-319-48881-3_2}
}

@inproceedings{zheng2015market1501,
  author    = {Zheng, Liang and Shen, Liyue and Tian, Lu and others},
  title     = {Scalable Person Re-identification: A Benchmark},
  booktitle = {Proceedings of the IEEE International Conference on Computer Vision (ICCV)},
  pages     = {1116--1124},
  year      = {2015},
  doi       = {10.1109/ICCV.2015.133}
}

@inproceedings{zheng2017duke,
  author    = {Zheng, Zhedong and Zheng, Liang and Yang, Yi},
  title     = {Unlabeled Samples Generated by GAN Improve the Person Re-identification Baseline in Vitro},
  booktitle = {Proceedings of the IEEE International Conference on Computer Vision (ICCV)},
  pages     = {3774--3782},
  year      = {2017},
  doi       = {10.1109/ICCV.2017.405}
}

@inproceedings{liu2016veri,
  author    = {Liu, Xinchen and Liu, Wu and Mei, Tao and others},
  title     = {A Deep Learning-Based Approach to Progressive Vehicle Re-identification for Urban Surveillance},
  booktitle = {Proceedings of the European Conference on Computer Vision (ECCV)},
  pages     = {869--884},
  year      = {2016},
  doi       = {10.1007/978-3-319-46475-6_53}
}

@inproceedings{chavdarova2018wildtrack,
  author    = {Chavdarova, Tatjana and Baqu{\'e}, Pierre and Bouquet, St{\'e}phane and others},
  title     = {WILDTRACK: A Multi-camera HD Dataset for Dense Unscripted Pedestrian Detection},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages     = {5030--5039},
  year      = {2018},
  doi       = {10.1109/CVPR.2018.00528}
}

@article{chen2015nlprmct,
  author  = {Chen, Weihua and Cao, Lijun and Chen, Xiaotang and others},
  title   = {An Equalised Global Graphical Model-Based Approach for Multi-camera Object Tracking},
  journal = {arXiv preprint arXiv:1502.03532},
  year    = {2015},
  doi     = {10.48550/arXiv.1502.03532}
}

@article{qi2021alprtraj,
  author  = {Qi, Xinyi and Ji, Yanjie and Li, Wenhao and others},
  title   = {Vehicle Trajectory Reconstruction on Urban Traffic Network Using Automatic License Plate Recognition Data},
  journal = {IEEE Access},
  volume  = {9},
  pages   = {49110--49120},
  year    = {2021},
  doi     = {10.1109/ACCESS.2021.3068964}
}

@inproceedings{tong2021vetrac,
  author    = {Tong, Panrong and Li, Mingqian and Li, Mo and others},
  title     = {Large-scale Vehicle Trajectory Reconstruction with Camera Sensing Network},
  booktitle = {Proceedings of the 27th Annual International Conference on Mobile Computing and Networking (MobiCom)},
  pages     = {188--200},
  year      = {2021},
  doi       = {10.1145/3447993.3448617}
}

@inproceedings{bewley2016sort,
  author    = {Bewley, Alex and Ge, Zongyuan and Ott, Lionel and Ramos, Fabio and Upcroft, Ben},
  title     = {Simple Online and Realtime Tracking},
  booktitle = {Proceedings of the IEEE International Conference on Image Processing (ICIP)},
  pages     = {3464--3468},
  year      = {2016},
  doi       = {10.1109/ICIP.2016.7533003}
}

@inproceedings{wojke2017deepsort,
  author    = {Wojke, Nicolai and Bewley, Alex and Paulus, Dietrich},
  title     = {Simple Online and Realtime Tracking with a Deep Association Metric},
  booktitle = {Proceedings of the IEEE International Conference on Image Processing (ICIP)},
  pages     = {3645--3649},
  year      = {2017},
  doi       = {10.1109/ICIP.2017.8296962}
}

@inproceedings{zhang2022bytetrack,
  author    = {Zhang, Yifu and Sun, Peize and Jiang, Yi and Yu, Dongdong and Weng, Fucheng and Yuan, Zehuan and Luo, Ping and Liu, Wenyu and Wang, Xinggang},
  title     = {ByteTrack: Multi-Object Tracking by Associating Every Detection Box},
  booktitle = {Proceedings of the European Conference on Computer Vision (ECCV)},
  year      = {2022},
  eprint    = {2110.06864},
  archivePrefix = {arXiv},
  doi       = {10.48550/arXiv.2110.06864}
}

@techreport{perry2013predictive,
  author      = {Perry, Walter L. and McInnis, Brian and Price, Carter C. and others},
  title       = {Predictive Policing: The Role of Crime Forecasting in Law Enforcement Operations},
  institution = {RAND Corporation},
  year        = {2013},
  doi         = {10.7249/RR233}
}

@article{lum2016predict,
  author  = {Lum, Kristian and Isaac, William},
  title   = {To Predict and Serve?},
  journal = {Significance},
  volume  = {13},
  number  = {5},
  pages   = {14--19},
  year    = {2016},
  doi     = {10.1111/j.1740-9713.2016.00960.x}
}

@inproceedings{ensign2018runaway,
  author    = {Ensign, Danielle and Friedler, Sorelle A. and Neville, Scott and others},
  title     = {Runaway Feedback Loops in Predictive Policing},
  booktitle = {Proceedings of the Conference on Fairness, Accountability and Transparency (FAT*)},
  year      = {2018},
  eprint    = {1706.09847},
  archivePrefix = {arXiv},
  doi       = {10.48550/arXiv.1706.09847}
}

@article{pereira2022banal,
  author  = {Pereira, Gabriel and Raetzsch, Christoph},
  title   = {From Banal Surveillance to Function Creep: Automated License Plate Recognition (ALPR) in Denmark},
  journal = {Surveillance \& Society},
  volume  = {20},
  number  = {3},
  pages   = {265--280},
  year    = {2022},
  doi     = {10.24908/ss.v20i3.15000}
}

@article{hadavi2020anpr,
  author  = {Hadavi, Sheida and Buldeo Rai, Heleen and Verlinde, Sara and others},
  title   = {Analyzing Passenger and Freight Vehicle Movements from Automatic-Number Plate Recognition Camera Data},
  journal = {European Transport Research Review (ETRR)},
  volume  = {12},
  number  = {1},
  year    = {2020},
  doi     = {10.1186/s12544-020-00405-x}
}
```

---

## Three things I would do before writing another line of this paper

1. **Change the claim.** The mechanism is 2004 prior art. Reframe as an empirical regime-characterisation study ("when does the counting baseline suffice, and when does it fail") and put Makris/Tieu/Javed/Gambs in your opening paragraph as what you are re-testing, not what you differ from.
2. **Get VeRi-776 and CityFlow this week.** Both are a form/email away, both have real cross-camera transitions, and VeRi-776 has real plate strings plus inter-camera distances. Synthetic traces will not survive review for a paper whose entire claim is about real deployment geometry.
3. **Add Flashback, ST-RNN and a popularity prior to the baseline table.** The popularity prior is the one most likely to be within noise of your method — find out now, not from Reviewer 2.

Sources: [Consensus](https://consensus.app), [scite](https://scite.ai), [Crossref](https://api.crossref.org), [arXiv](https://arxiv.org), [Exposing.ai: Duke MTMC](https://exposing.ai/duke_mtmc/), [VeRi dataset](https://github.com/JDAI-CV/VeRidataset), [CityFlow (ar5iv)](https://ar5iv.arxiv.org/html/1903.09254), [AI City Challenge](https://www.aicitychallenge.org/2024-data-and-evaluation/)

Upgrade to Consensus Pro to return 20 results per search instead of 10, and include more data like study design and key takeaways for every result.: https://consensus.app/pricing/?utm_source=claude_desktopagentId: ab5139d623db7d457 (use SendMessage with to: 'ab5139d623db7d457', summary: '<5-10 word recap>' to continue this agent)
<usage>subagent_tokens: 219207
tool_uses: 48
duration_ms: 611058</usage>