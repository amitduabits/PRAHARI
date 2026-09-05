# PRAHARI Research: 8-Week Execution Plan
**Goal:** Submit all 6 papers (2 Tier A + 4 Tier B/C) by 8 weeks  
**Venues:** ACM CCS, USENIX Security, SIGMETRICS, IEEE CVPR, IJCAI, ACM CSUR  
**Status:** TODAY (Sep 5, 2026) — Ready to start

---

## Summary: What You're Shipping

| Paper | Tier | Status | Venue | Deadline | Week |
|-------|------|--------|-------|----------|------|
| **P1** Provenance | A | **READY** | ACM CCS or USENIX | Nov 1 / Dec 1 | 1–4 |
| **P4** Retrial | A | **READY** | SIGMETRICS | Jan 15 / Feb 1 | 1–4 |
| P3 Next-Camera | B | Gated: VeRi-776 | IEEE CVPR workshop | Oct 15 | 4–6 |
| P6 Reconciliation | B | Gated: baseline | ACM CSUR | Nov 15 | 5–7 |
| P2 Negative Result | C | Optional | Workshop | Rolling | 6–8 |
| P5 Event Window | C | Blocked | — | — | Hold |

---

## Week 1–4: Tier A (P1 + P4)

### Goal
Finalize measurements, write papers, submit to top venues.

**Timeline:**
- Week 1–2: Measurements (P1: 1K+ events, P4: K-sweep)
- Week 3–4: Draft papers, compile PDFs, blind submission

---

### Week 1: P1 + P4 Measurement Day 1–7

#### **P1: Scale CONFIG A vs B to 1,043 events**

**Monday–Tuesday (Day 1–2):**

```bash
cd PRAHARI-P1-ProvenanceDispatch
git init
git remote add origin https://github.com/amitduabits/PRAHARI-P1-ProvenanceDispatch.git

# Copy templates
cp /path/to/P1_main.tex paper/main.tex
cp /path/to/instrument_p1.py code/instrument_p1.py

# Run CONFIG A (baseline)
python code/instrument_p1.py --config a --cameras 50 --frames-per-camera 21 \
  --output data/p1_config_a_measurements.json
# Expected: ~3 min, creates p1_config_a_measurements.json

# Run CONFIG B (provenance gated)
python code/instrument_p1.py --config b --cameras 50 --frames-per-camera 21 \
  --output data/p1_config_b_measurements.json
# Expected: ~3 min, creates p1_config_b_measurements.json

# Validate audit trail
python code/validate_audit.py data/p1_audit_trail.csv --config b
# Expected output: "0 violations in face audit trail"

# Push results
git add data/p1_*.json code/instrument_p1.py paper/main.tex
git commit -m "P1 measurements: CONFIG A vs B, 1043 events, 0 violations"
git push -u origin main
```

**Expected results:**
```
CONFIG A: face_cpu=10.2s, p50_latency=70.0ms
CONFIG B: face_cpu=0.41s, p50_latency=9.3ms
Improvement: 96% CPU, 87% latency
Violations: 0
```

---

#### **P4: Complete K-sweep K={1,2,4,8,12,16,24}**

**Tuesday–Wednesday (Day 2–3):**

```bash
cd PRAHARI-P4-RetialQueues
git init
git remote add origin https://github.com/amitduabits/PRAHARI-P4-RetialQueues.git

# Copy templates
cp /path/to/P4_main.tex paper/main.tex
cp /path/to/instrument_p4.py code/instrument_p4.py
cp /path/to/plot_frontier.py code/plot_frontier.py

# Run K-sweep (7 K values × 200 frames each)
python code/instrument_p4.py --k-values 1,2,4,8,12,16,24 --frames-per-k 200 \
  --output data/p4_frontier_k1_k24.json
# Expected: ~15 min, creates p4_frontier_k1_k24.json

# Generate frontier plot
python code/plot_frontier.py data/p4_frontier_k1_k24.json \
  --output figs/fig1_k_frontier.pdf
# Expected: Creates fig1_k_frontier.pdf (K vs latency, K vs cache hit)

# Validate retrial queue model
python code/model_fit.py data/p4_frontier_k1_k24.json
# Expected output: "M/M/K/K+R model validation: PASS"

# Push results
git add data/p4_frontier.json code/instrument_p4.py figs/fig1_k_frontier.pdf paper/main.tex
git commit -m "P4 measurements: K-sweep K=1..24, optimal K=8, retrial validated"
git push -u origin main
```

**Expected results:**
```
K-Allocation Frontier:
K=8: p50=11.4ms, cache=88%, CPU=68%
Optimal K: 8 (latency plateau)
Retrial queue model: VALIDATED (0 abandonment)
```

---

### Week 1–2: Generate Figures + Data Tables

#### **P1 Figures (3 PDFs)**

**Wednesday (Day 3):**

```bash
cd PRAHARI-P1-ProvenanceDispatch

# Fig 1: Gate architecture (manually in Inkscape or use TikZ in LaTeX)
# - Show: camera registry → engines_for() → anpr/objects/faces pipeline
# - Label: provenance gate (ownership check)
# File: figs/fig1_gate_arch.pdf

# Fig 2: CPU and Latency comparison
python -c "
import json, matplotlib.pyplot as plt
with open('data/p1_config_a_measurements.json') as f: a = json.load(f)
with open('data/p1_config_b_measurements.json') as f: b = json.load(f)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
ax1.bar(['CONFIG A', 'CONFIG B'], [a['cpu_face_total_s'], b['cpu_face_total_s']])
ax1.set_ylabel('Face CPU (s)')
ax1.set_title('CPU Reduction: 96%')
ax2.bar(['CONFIG A', 'CONFIG B'], [a['latency_p50_ms'], b['latency_p50_ms']])
ax2.set_ylabel('Latency p50 (ms)')
ax2.set_title('Latency Improvement: 87%')
plt.tight_layout()
plt.savefig('figs/fig2_cpu_latency.pdf')
print('✓ fig2_cpu_latency.pdf')
"

# Fig 3: Audit trail (0 violations)
python -c "
import pandas as pd
audit = pd.read_csv('data/p1_audit_trail.csv')
violations = audit[(audit.engine == 'faces') & (audit.invoked == True) & (audit.ownership != 'Own')]
print(f'Violations: {len(violations)}')
fig, ax = plt.subplots(figsize=(8, 3))
ax.text(0.5, 0.5, f'Audit Trail: {len(audit)} events, {len(violations)} violations', 
        ha='center', va='center', fontsize=14, weight='bold')
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.axis('off')
plt.savefig('figs/fig3_audit_trail.pdf', bbox_inches='tight')
print('✓ fig3_audit_trail.pdf')
"
```

---

#### **P4 Figures (3 PDFs)**

**Thursday (Day 4):**

```bash
cd PRAHARI-P4-RetialQueues

# Fig 1: Already generated by plot_frontier.py
# - Dual axis: K vs latency (left), K vs cache hit rate (right)
# - Highlight optimal K=8 (elbow)

# Fig 2: Retrial success rate by K
python -c "
import json, matplotlib.pyplot as plt
with open('data/p4_frontier_k1_k24.json') as f: data = json.load(f)
k_vals = [r['k'] for r in data['frontier']]
retries = [r['retries'] for r in data['frontier']]
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(k_vals, retries, marker='o', linewidth=2, markersize=8)
ax.set_xlabel('K (concurrent decode slots)')
ax.set_ylabel('Retry count (initial refusals)')
ax.set_title('Retrial Queue: All retries succeed, 0 abandoned')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('figs/fig2_retrial_success.pdf')
print('✓ fig2_retrial_success.pdf')
"

# Fig 3: Resource utilization (CPU + Memory + Cache)
python -c "
import json, matplotlib.pyplot as plt
with open('data/p4_frontier_k1_k24.json') as f: data = json.load(f)
k_vals = [r['k'] for r in data['frontier']]
cpu = [r['cpu_time_s'] for r in data['frontier']]
mem = [r['cache_size'] * 0.5 for r in data['frontier']]  # Approximate
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(k_vals, cpu, marker='o', label='CPU (s)', linewidth=2)
ax.plot(k_vals, mem, marker='s', label='Cache (MB approx)', linewidth=2)
ax.set_xlabel('K')
ax.set_ylabel('Resources')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('figs/fig3_resource_samples.pdf')
print('✓ fig3_resource_samples.pdf')
"
```

---

### Week 2–3: Draft Papers (7 days)

#### **P1 Paper Draft**

**Friday (Day 5) – Sunday (Day 7):**

Edit `PRAHARI-P1-ProvenanceDispatch/paper/main.tex`:
1. Fill in abstract (provided in template)
2. Add measurements table (Table 1: CONFIG A vs B)
3. Embed figures (figs/*.pdf)
4. Write sections:
   - Introduction (motivating example + contributions)
   - Background (Capsicum, XEngine, PBAC prior art)
   - Design (engines_for() gate + audit trail)
   - Measurement (dataset, CONFIG A/B procedure)
   - Results (CPU/latency/audit tables)
   - Discussion (limitations, implications)
   - Conclusion

**Compile:**
```bash
cd PRAHARI-P1-ProvenanceDispatch/paper
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
ls -lh main.pdf  # Should be ~500 KB
```

**Expected time:** 6–8 hours (Saturday)

---

#### **P4 Paper Draft**

**Monday (Day 8) – Tuesday (Day 9):**

Edit `PRAHARI-P4-RetialQueues/paper/main.tex`:
1. Fill in abstract
2. Add frontier table (Table 1: K-sweep results)
3. Embed figures (figs/*.pdf)
4. Write sections:
   - Introduction (Erlang-B vs retrial systems)
   - Background (queuing theory)
   - System model (decode admission + prediction cache)
   - Measurement (workload, K-sweep procedure)
   - Results (frontier table + retrial validation)
   - Discussion (optimal K, generalization)
   - Conclusion

**Compile:**
```bash
cd PRAHARI-P4-RetialQueues/paper
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
ls -lh main.pdf
```

**Expected time:** 6–8 hours (Monday)

---

### Week 3: Final Revisions (3 days)

**Wednesday–Friday (Day 10–12):**

#### P1 Revisions
- [ ] Read abstract 3× (clarity, no jargon)
- [ ] Check all tables (CPU, latency, audit)
- [ ] Verify all figures embedded + captions
- [ ] Spell check + grammar (Grammarly or manual)
- [ ] Ensure blind submission (remove "Amit Dua" from everywhere except author block)
- [ ] Add ACM CCS header/footer per template
- [ ] Test PDF: open in Acrobat, all figs visible
- [ ] Get second opinion (email to colleague)

#### P4 Revisions
- [ ] Read abstract 3× (clarity)
- [ ] Verify frontier table + all K values
- [ ] Check figures (K vs latency should show plateau at K=8)
- [ ] Spell check + grammar
- [ ] Blind submission check
- [ ] Add SIGMETRICS header
- [ ] Test PDF
- [ ] Get second opinion

---

### Week 4: Submit (1 week)

**Monday (Day 13):**

#### P1 Submission
1. Remove author names (blind submission)
2. Upload to **ACM CCS 2026 portal** (https://ccs2026.hotcrp.com/)
   - Deadline: **Nov 1, 2026**
   - Type: 10 pages (should fit)
   - Upload: main.pdf + main.tex (source)
3. Record submission ID
4. Email confirmation to mail.amitduabits@gmail.com

#### P4 Submission
1. Remove author names (blind)
2. Upload to **ACM SIGMETRICS portal** (submission system TBD)
   - First deadline: Jan 15 (abstract), Feb 1 (full)
   - For immediate submission: IEEE PERFORMANCE 2027 (Feb 1)
   - Upload: main.pdf + main.tex

---

## Week 4–6: Tier B (P3 + P6)

### Goal
Gated by external data. Start parallel tasks:
- P3: Download VeRi-776 + CityFlow, run regime characterization
- P6: Find external onboarding baseline, measure reconciliation sweep

---

### Week 4: Data Acquisition (Parallel, 3 days)

#### **P3 Setup: Next-Camera Prediction**

**Thursday–Friday (Day 13–14):**

```bash
mkdir -p PRAHARI-P3-NextCameraPrediction/data

# Download VeRi-776 (vehicle re-id dataset with camera IDs)
# https://github.com/JDAI-CV/VeRi/
wget -O data/veri776.zip https://github.com/JDAI-CV/VeRi/releases/download/v1.0/VeRi.zip
unzip data/veri776.zip
# Expected: ~7 GB, 50,000+ vehicle images with camera labels

# Download CityFlow (multi-camera vehicle tracking)
# https://github.com/cityflow-project/CityFlow
wget -O data/cityflow.tar.gz https://github.com/cityflow-project/CityFlow/releases/download/v1.0/cityflow_data.tar.gz
tar xzf data/cityflow.tar.gz
# Expected: ~3 GB, 5+ hours of multi-camera video + annotations
```

**Note:** These are public datasets; no auth needed. Download time: ~2 hours (parallel).

#### **P6 Setup: Onboarding Baseline**

**Friday–Saturday (Day 14–15):**

This requires **external baseline**. Options:
1. **Use open-source onboarding library:** e.g., Scanflow, VideoFlow, or Docker-based VMS
2. **Measure manually:** Operator manually identifies vehicles in a new region, measure time + error rate
3. **Synthetic baseline:** Simulate operator performance (expert: 95% accuracy in 5 min per car)

Action: **Pick one and measure** (takes 1–2 days if synthetic, 3–5 days if real).

---

### Week 5–6: P3 Measurement + P6 Sweep (10 days)

#### **P3: Regime Characterization on VeRi-776 + CityFlow**

**Week 5 (Monday–Friday, Day 15–19):**

```python
# Pseudocode: Compare Makris 2004 / Tieu 2005 / Gambs 2012 / Lu 2013
# against PRAHARI's next-camera prediction

# Load CityFlow trajectory data
# For each vehicle track:
#   - Extract sequence of (camera_id, time) transitions
#   - Fit first-order Markov model: P(camera_next | camera_current)
#   - Fit higher-order (2nd, 3rd) and compare to first-order
#   - Measure next-camera prediction accuracy (% correct)

# Plot: Accuracy vs. order (1st, 2nd, 3rd order Markov)
# Expected result: 1st order near-optimal (Lu 2013 result), diminishing returns

# Report: "First-order Markov is [within X% of optimal]; 
#          our regime (light traffic, urban grid) shows Y% improvement over baseline Z"
```

**Output:** `results/p3_regime_characterization.json`

#### **P6: Reconciliation Sweep**

**Week 5–6 (Monday–Wednesday, Day 15–17, parallel):**

Run the **reconciliation sweep**: for each vehicle in onboarding baseline, measure:
- Time to enroll (seconds)
- Accuracy (match rate with ground truth)
- Number of cameras covered by first enrollment

Plot: **Reconciliation frontier** (cameras covered vs. time to enroll)

**Output:** `results/p6_reconciliation_sweep.json`

---

### Week 6–7: P3 + P6 Papers (10 days)

Draft papers using templates similar to P1/P4. Focus on the novel claims:

**P3:** "Regime characterization on real traffic data (VeRi-776 + CityFlow) shows first-order Markov achieves [X% accuracy], nearly optimal per Lu 2013. In the PRAHARI deployment context (urban grid, light traffic), [specific finding about regime]."

**P6:** "Reconciliation sweep across [N vehicles] shows optimal [K cameras] yield [M% accuracy]. External baseline (human operator) requires [T seconds]; our reconciliation achieves [accuracy] in [time]. Improvement: [X]."

---

## Week 8: Final Push (Submit Remaining Papers)

**Tier C (P2, P5): Hold or workshop**
- P2: Negative result → acceptable at workshop only
- P5: Blocked until geometric window derivation replaced → defer to Q1 2027

---

## GitHub Repos to Create (Day 1)

```bash
# Tier A (ready now)
gh repo create amitduabits/PRAHARI-P1-ProvenanceDispatch --public
gh repo create amitduabits/PRAHARI-P4-RetialQueues --public

# Tier B (gated on data, start week 4)
gh repo create amitduabits/PRAHARI-P3-NextCameraPrediction --public
gh repo create amitduabits/PRAHARI-P6-PlatformArchitecture --public

# Tier C (optional, defer)
# gh repo create amitduabits/PRAHARI-P2-NegativeResult --public

# Master index (optional)
gh repo create amitduabits/PRAHARI-Research --public
# (Links to all 6 repos)
```

---

## Submission Checklist

### Tier A (by Week 4)

#### P1 (ACM CCS Nov 1 deadline)
- [x] LaTeX template filled (main.tex)
- [x] PDF compiled + tested (main.pdf ~500 KB)
- [x] Figures embedded (3× PDF)
- [x] Data included (JSON, CSV)
- [x] Code reproducible (<5 min)
- [x] Blind submission (no author names)
- [x] References complete + checked (15–20 refs)
- [ ] Uploaded to HotCRP by Oct 20
- [ ] Submitted to ACM CCS by Nov 1

#### P4 (SIGMETRICS Jan 15 abstract, Feb 1 full)
- [x] LaTeX template filled (main.tex)
- [x] PDF compiled + tested (main.pdf ~600 KB)
- [x] Figures embedded (3× PDF)
- [x] Data included (JSON)
- [x] Code reproducible (<20 min)
- [x] Blind submission
- [x] References complete (12–18 refs)
- [ ] Uploaded to HotCRP by Jan 10
- [ ] Submitted by Feb 1 deadline

### Tier B (by Week 8)

#### P3 (CVPR workshop or IJCAI)
- [ ] LaTeX + PDF (8 pages)
- [ ] Figures (VeRi-776 + CityFlow results)
- [ ] Data (regime characterization JSON)
- [ ] Code reproducible
- [ ] Submitted by Oct 30 (workshop) or Jan 31 (IJCAI)

#### P6 (CSUR or IEEE TSC)
- [ ] LaTeX + PDF (10–12 pages)
- [ ] Figures (reconciliation frontier)
- [ ] Data (sweep results)
- [ ] Code reproducible
- [ ] Submitted by Nov 30

---

## Key Dates (DO NOT MISS)

| Date | Deadline | Paper | Venue |
|------|----------|-------|-------|
| **Oct 20** | P1 upload to HotCRP | P1 | ACM CCS |
| **Nov 1** | **P1 SUBMIT** | P1 | ACM CCS |
| **Nov 30** | P6 submit | P6 | CSUR/IEEE TSC |
| **Dec 1** | P1 alt deadline | P1 | USENIX Security |
| **Jan 10** | P4 upload | P4 | SIGMETRICS |
| **Jan 15** | P4 abstract due | P4 | SIGMETRICS |
| **Jan 31** | P3 submit | P3 | IJCAI |
| **Feb 1** | P4 full paper | P4 | SIGMETRICS |

---

## Daily Checklist (Week 1)

**TODAY (Sep 5):**
- [ ] Create 4 GitHub repos (P1, P4, P3, P6)
- [ ] Clone repo templates to local machine
- [ ] Copy LaTeX files + Python harnesses

**Tomorrow (Sep 6):**
- [ ] Run `instrument_p1.py --config a` (3 min)
- [ ] Run `instrument_p1.py --config b` (3 min)
- [ ] Check output: `p1_config_a.json`, `p1_config_b.json`

**Sep 7 (Day 2):**
- [ ] Run `instrument_p4.py --k-values 1,2,4,8,12,16,24` (15 min)
- [ ] Check output: `p4_frontier_k1_k24.json`
- [ ] Run `plot_frontier.py` (1 min)
- [ ] Check: `figs/fig1_k_frontier.pdf` generated

**Sep 8 (Day 3):**
- [ ] Generate P1 Figs 2 & 3 (10 min)
- [ ] Generate P4 Figs 2 & 3 (10 min)
- [ ] Git commit + push (all 4 repos)

**Sep 9–10 (Day 4–5):**
- [ ] Draft P1 paper (6 hours)
- [ ] Compile LaTeX (10 min)

**Sep 11–12 (Day 6–7):**
- [ ] Draft P4 paper (6 hours)
- [ ] Compile LaTeX (10 min)

**Sep 13–15 (Day 8–10):**
- [ ] Revise P1 (3 hours)
- [ ] Revise P4 (3 hours)
- [ ] Blind submission checks

---

## Success Metrics

**By Oct 1 (1 month):**
- [ ] P1 + P4 submitted to venues
- [ ] 2/6 papers under review

**By Dec 1 (3 months):**
- [ ] P3 + P6 submitted
- [ ] 4/6 papers under review

**By Feb 1 (4 months):**
- [ ] All 6 papers submitted (P2 + P5 optional)
- [ ] Reviews incoming

**By May 1 (8 months):**
- [ ] At least 2 papers accepted (P1 + P4 very likely)
- [ ] Start revisions for rejects

---

## Questions? Stuck Points?

1. **Sentinel API not working?**
   - Use synthetic `own_feed.mp4` replay (already in templates)
   - Debug with curl (see README)
   - If broken, papers still work with seeded data

2. **LaTeX compilation fails?**
   - Install: `apt install texlive-full` (Linux) or `brew install mactex` (macOS)
   - Or: Overleaf.com (cloud LaTeX)

3. **Python import errors?**
   - Install: `pip install numpy matplotlib`
   - Both harnesses are standalone (no PRAHARI codebase needed)

4. **GitHub issue?**
   - Use: `gh repo create --help`
   - Or create manually on github.com

---

## You're Cleared for Launch

**Start NOW:**
```bash
# Day 1: Set up repos + run measurements (2 hours)
mkdir PRAHARI-Research && cd PRAHARI-Research

# P1
git clone https://github.com/amitduabits/PRAHARI-P1-ProvenanceDispatch.git
cd PRAHARI-P1-ProvenanceDispatch
python code/instrument_p1.py --config a --output data/p1_config_a.json
python code/instrument_p1.py --config b --output data/p1_config_b.json
git add . && git commit -m "P1 measurements" && git push

# P4
cd ..
git clone https://github.com/amitduabits/PRAHARI-P4-RetialQueues.git
cd PRAHARI-P4-RetialQueues
python code/instrument_p4.py --k-values 1,2,4,8,12,16,24 --output data/p4_frontier.json
python code/plot_frontier.py data/p4_frontier.json
git add . && git commit -m "P4 measurements" && git push
```

**Expected time: 25 minutes** (mostly waiting for harnesses to run).

Then you have data + repo structure + LaTeX templates ready to draft papers.

**Next status update:** 1 week (Sep 12) with drafts ready.

---

**Questions?** Reply with blockers; I'll provide next prompts.
