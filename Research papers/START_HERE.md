# PRAHARI Research Program: START HERE

Welcome to the complete guide for writing 6 high-impact research papers from your patent portfolio.

## WHAT YOU HAVE

Four comprehensive documents:

### 📋 **1. PRAHARI_Research_Program_Summary.md** (Executive Overview)
- **Start here** if you're new to this program
- 10-page summary of entire effort
- Budget, timeline, risks, success metrics
- FAQ section
- **Read time: 30 minutes**

### 🎯 **2. PRAHARI_Research_Strategy.md** (Strategic Roadmap)
- Deep dive into 6 papers + venues + team composition
- Why each paper matters; novelty positioning
- Publication timeline; success metrics
- Go-to-market strategy (papers → partnerships)
- **Read time: 1–2 hours** (reference material)

### 👥 **3. PRAHARI_Research_Team_Playbook.md** (Hiring Guide)
- Detailed job descriptions (7 positions)
- Red flags vs. green flags per role
- Interview questions that matter
- How circles integrate + work together
- **Read time: 1–2 hours** (reference material)

### 🔧 **4. PRAHARI_Research_Promptbook.md** (The Tool)
- **Your daily companion**
- 18 numbered prompts (Prompt 1.1 → 6.1)
- Complete guide to writing each paper
- Skill progression framework
- Anti-patterns + recovery strategies
- **Read time: 2–3 hours on first read; use as reference**

### 📇 **5. PRAHARI_Quick_Reference.md** (Print This)
- One-page workflows
- All prompts at a glance with time estimates
- Red flags checklist
- Weekly standup template
- **Print this. Tape to your monitor. Refer to daily.**

---

## GETTING STARTED (THIS WEEK)

### **Monday: Orientation (1 hour)**
1. Read `PRAHARI_Research_Program_Summary.md` (this file)
2. Skim `PRAHARI_Research_Strategy.md` (highlights only)
3. Print `PRAHARI_Quick_Reference.md`

### **Tuesday: Team Planning (2 hours)**
1. Review `PRAHARI_Research_Team_Playbook.md`
2. Identify candidates for Circle A1 (Principal Researcher)
3. Identify candidates for Circle B1 (Senior Systems Researcher)
4. Identify candidates for Circle C1 (Domain Expert)

### **Wednesday: Infrastructure Setup (2 hours)**
1. Create GitHub org: `PRAHARI-Research`
2. Create Slack channel: `#research-papers`
3. Set up Google Drive folder (for shared docs)
4. Schedule Friday standup (recurring, 15 min)

### **Friday: Paper 1 Kickoff (3 hours)**
1. Open Claude conversation: "Paper 1: Provenance-Gated Inference — PRAHARI"
2. Paste Prompt 1.1 (Literature Review) from `PRAHARI_Research_Promptbook.md`
3. Get results; spend 30 min reading abstracts
4. Share output with Circle C lead (domain expert)
5. Block calendar: Paper 1 Weeks 1–4 (12 weeks total)

---

## PAPER WRITING ROADMAP

```
OCT 2026: Paper 1 starts
  Week 1-2:  Problem formulation (Prompts 1.1, 1.2, 2.1)
  Week 3-4:  Algorithm design (Prompts 2.2, 2.3)
  Week 5-8:  Experiments (Prompts 3.1, 3.2)
  Week 9-10: Draft paper (Prompts 4.1, 4.2)
  Week 11-12: Polish & submit (Prompts 5.1, 5.2, 6.1)
  → SUBMIT to CVPR

DEC 2026: Paper 2 starts (parallel with Paper 1 revisions)
  Same structure, faster (reuse infrastructure from Paper 1)
  → SUBMIT to ICCV

FEB 2027: Papers 3 & 4 start (parallel tracks)
MAY 2027: Papers 5 & 6 start (parallel tracks)

SEP 2027: All papers submitted

OCT 2027 - JUN 2028: Revisions + acceptances + publications
```

---

## USING THE PROMPTBOOK

The `PRAHARI_Research_Promptbook.md` is your daily guide.

**How to use it:**

1. **Open ONE persistent Claude conversation per paper**
   - Title: "Paper 1: Provenance-Gated Inference — PRAHARI"
   - Keep this conversation open for all 12 weeks of Paper 1

2. **Follow prompts sequentially**
   - Start with Prompt 1.1 (Literature Review)
   - Get output; iterate if needed
   - Move to Prompt 1.2 (Related Work)
   - Continue through Prompt 6.1 (Reviewer Rebuttals)

3. **Each prompt produces a tangible deliverable**
   - Prompt 1.1 → Literature matrix (30 papers)
   - Prompt 1.2 → Related work section (800 words)
   - Prompt 2.1 → Problem formulation (2–3 pages)
   - ... and so on

4. **Share each output with your team (Circle A/B/C)**
   - Get feedback before moving to next prompt
   - Iterate based on feedback
   - Only move forward when sign-off is received

5. **At week 12, you have a complete paper ready to submit**

---

## WHO DOES WHAT

### **Hari Om Bansal (You)**
- Co-author on all 6 papers
- Decide final direction (which papers to prioritize, etc.)
- Liaison between team and external stakeholders
- Quality gate at key milestones

### **Circle A (Vision & AI, 2.5 FTE)**
- Lead Papers 1, 2, 5
- Design algorithms + prove theorems
- Run computer vision experiments

### **Circle B (Systems & Infrastructure, 2.5 FTE)**
- Lead Papers 3, 4, 6
- Design systems experiments
- Benchmark latency / throughput
- Maintain reproducibility infrastructure

### **Circle C (Domain & Deployment, 1.5 FTE)**
- Support all papers (reality check)
- Ensure experiments are grounded in PRAHARI deployment
- Validate assumptions with operators
- Prevent over-claims

### **Circle D (Legal & Policy, 0.5 FTE advisory)**
- Review every draft for compliance (Section 64)
- Flag over-stated claims
- Advise on policy positioning

---

## QUICK WINS (DO THESE FIRST)

### **Week 1: Literature Review (Prompt 1.1)**
- Search for 30 papers
- Takes 2 hours
- Output: Literature matrix showing novelty of your work
- **Why:** Proves you're not reinventing the wheel

### **Week 2: Algorithm & Proof (Prompts 2.2)**
- Write pseudocode
- Prove one theorem
- Takes 3 hours
- Output: Algorithm section (1 page) + Proof
- **Why:** Proves your approach is sound

### **Week 3-4: Reference Implementation (Prompt 2.3)**
- Implement algorithm in Python
- Run tests
- Takes 4 hours
- Output: Working code + README
- **Why:** Proves you can build it (not just theory)

### **Week 5-6: Experiments (Prompt 3.1)**
- Design 4 experiments
- Run them
- Takes 8 hours
- Output: Figure + table
- **Why:** Proves your claims with data

By end of week 6, you have:
- Literature review (novelty proven)
- Algorithm (correctness proven)
- Code (implementation proven)
- Experiments (empirical validation)

Weeks 7–12 are writing + polishing.

---

## RED FLAGS (STOP IF YOU SEE THESE)

1. **"I've been on Prompt 2.1 for 2 weeks"**
   - Problem not clear enough
   - Simplify scope; move forward

2. **"Experiments not done yet, but I'm drafting the paper"**
   - You have no results to write about
   - Pause writing; finish experiments first

3. **"All my experiments worked perfectly"**
   - Suspicious
   - Find one ablation that didn't work; explain why
   - Papers need honest results, not perfect results

4. **"I don't have fixed random seeds in my code"**
   - Results aren't reproducible
   - Fix this week; re-run experiments
   - Don't move forward without it

5. **"My paper sounds like ChatGPT wrote it"**
   - Read it out loud
   - Do Prompt 5.2 (AI-language audit)
   - Rewrite in human voice

---

## SUCCESS FORMULA

**Paper Quality = Literature Review (40%) + Algorithm (20%) + Experiments (30%) + Writing (10%)**

- **Skip lit review?** Reviewers will find prior art you missed. Desk rejection.
- **Skip algorithm proof?** "I don't believe your approach is correct." Rejection.
- **Skip experiments?** "Where's your evidence?" Rejection.
- **Poor writing?** Harder to understand your contribution. Lower scores.

**Do all four.** The Promptbook guides you through all four.

---

## TIMELINE (REALISTIC)

| Paper | Venue | Duration | Difficulty | Status |
|-------|-------|----------|-----------|--------|
| 1 | CVPR | 12 weeks | High | Foundation |
| 2 | ICCV | 8 weeks | High | Reuse + deepen |
| 3 | IJCAI | 8 weeks | Medium | Cross-domain |
| 4 | IEEE Trans MM | 8 weeks | Medium | Benchmarking |
| 5 | IEEE Trans CSVT | 8 weeks | Medium | Ablations |
| 6 | IEEE Trans Emerging | 8 weeks | Low | Systems review |
| **Total** | — | **52 weeks** | — | **On track for 2028** |

**Can we do this in 24 months?** Yes, if:
- Papers overlap (1–2, 3–4, 5–6 in parallel)
- Teams reuse infrastructure
- Prompts are followed faithfully (not reinventing)

---

## WHAT'S IN THE OUTPUT FOLDER

You should have these files downloaded:

```
D:\1_Projects\Research_Ongoing\CDRF_hari_om_bansal_sir\
├── PRAHARI_Research_Program_Summary.md  ← START HERE
├── PRAHARI_Research_Strategy.md         ← Strategic overview
├── PRAHARI_Research_Team_Playbook.md    ← Hiring guide
├── PRAHARI_Research_Promptbook.md       ← Daily work tool
├── PRAHARI_Quick_Reference.md           ← Print this
└── START_HERE.md                        ← This file
```

---

## GETTING HELP

### **"How do I use the Promptbook?"**
→ Read the Promptbook itself (section: "How to Use This Promptbook")
→ Look at the example: "Week 1–2 Example: Paper 1, Week 1"

### **"What if I get stuck on a specific prompt?"**
→ Check the Promptbook's "Anti-Patterns & Recovery" section
→ Escalate to Hari Om Bansal or the relevant Circle lead

### **"Can I skip a prompt?"**
→ No. All 18 prompts build on each other.
→ Skip one, you'll regret it at paper-writing time.

### **"What if experiments fail?"**
→ See "Anti-Patterns: All Results Are Positive"
→ Report negative results honestly; that's publishable too

### **"How do I handle reviewer feedback?"**
→ See Promptbook: "Phase 6: Revision (Post-Feedback)"
→ See Prompt 6.1 (Anticipated Reviewer Questions)

---

## FINAL CHECKLIST (BEFORE YOU START)

- [ ] Read PRAHARI_Research_Program_Summary.md (30 min)
- [ ] Skim PRAHARI_Research_Strategy.md (1 hour, highlights only)
- [ ] Skim PRAHARI_Research_Team_Playbook.md (1 hour, highlights only)
- [ ] Skim PRAHARI_Research_Promptbook.md (2 hours, understand structure)
- [ ] Print PRAHARI_Quick_Reference.md (tape to monitor)
- [ ] Share all documents with team (Slack, Google Drive)
- [ ] Schedule kickoff meeting (Friday)
- [ ] Identify 3 candidates for Circle A1, B1, C1 leads
- [ ] Reserve calendar: Paper 1 = Oct 2026 – Feb 2027

If all checks pass: **YOU'RE READY TO GO. Let's write great papers.** 🚀

---

**Next Step:** Open the Promptbook. Start with Prompt 1.1 (Literature Review).

**Questions?** Escalate to Hari Om Bansal.

**Good luck.** 🚀

---

**Prepared by:** Alex Harmozi Research Framework  
**For:** Hari Om Bansal, CDRF, Yushu Excellence  
**Date:** September 5, 2026  
**Status:** Ready for Execution
