# PRAHARI Research Promptbook: Quick Reference Card

## ONE-PAGE WORKFLOW

Print this. Tape it to your monitor. Use every day.

---

## PAPER WRITING CYCLE (12 Weeks Per Paper)

```
WEEK 1-2: PROBLEM FORMULATION
  ├─ Prompt 1.1: Literature Review (automated search, 30 papers)
  ├─ Prompt 1.2: Related Work (800 words, positioned)
  ├─ Prompt 2.1: Problem Definition (formal, no ambiguity)
  └─ Gate: Related work approved by Circle C (domain expert)

WEEK 3-4: ALGORITHM DESIGN
  ├─ Prompt 2.2: Pseudocode + Theorem (proven)
  ├─ Prompt 2.3: Claude Code (working implementation)
  ├─ Run unit tests (pytest; all pass)
  └─ Gate: Code reviewed by Circle B (systems)

WEEK 5-8: EXPERIMENTS
  ├─ Prompt 3.1: Experiment Design (4 experiments, protocols written)
  ├─ Prompt P-X.1: Run Experiments (collect data, log everything)
  ├─ Prompt 3.2: Results Analysis (figures, tables, section draft)
  └─ Gate: Results reviewed by Circle C (interpretable, honest)

WEEK 9-10: DRAFT PAPER
  ├─ Prompt 4.1: Abstract (exactly 50 words)
  ├─ Prompt 4.2: Full Paper Outline (all sections, ~4000 words)
  ├─ Paste into Google Doc; share for feedback
  └─ Gate: Internal review complete (no major rewrites needed)

WEEK 11-12: POLISH & SUBMIT
  ├─ Prompt 5.1: Consistency Check (claims vs. evidence)
  ├─ Prompt 5.2: No-AI Language Audit (human voice)
  ├─ Prompt 6.1: Anticipated Reviewer Questions (ready rebuttals)
  ├─ Finalize reproducibility package (GitHub, README, seeds)
  └─ SUBMIT TO VENUE
```

---

## KEY PROMPTS BY PURPOSE

### **When you need...**

| Need | Prompt | Time |
|------|--------|------|
| Literature review | 1.1 | 2 hrs |
| Related work section | 1.2 | 4 hrs |
| Problem definition | 2.1 | 2 hrs |
| Algorithm & proof | 2.2 | 3 hrs |
| Reference implementation | 2.3 | 4 hrs |
| Experiment design | 3.1 | 3 hrs |
| Results figures/tables | 3.2 | 4 hrs |
| Abstract | 4.1 | 1 hr |
| Full paper draft | 4.2 | 8 hrs |
| Consistency audit | 5.1 | 2 hrs |
| AI-language check | 5.2 | 2 hrs |
| Reviewer rebuttals | 6.1 | 3 hrs |

---

## CLAUDE CONVERSATION STRUCTURE

**For each paper, open ONE persistent Claude conversation.** Save all prompts there.

```
Conversation Title: "Paper 1: Provenance-Gated Inference — PRAHARI"

Message 1: Prompt 1.1 (Literature Review)
         ↓ Get results
         ↓ Iterate if needed

Message 2: Prompt 1.2 (Related Work)
         ↓ Get draft
         ↓ Iterate

...

Message 12: Prompt 6.1 (Reviewer Rebuttals)
          ↓ Export entire conversation to markdown
          ↓ Archive in project folder
```

**Why:** Single conversation preserves context. Claude remembers previous decisions.

---

## SKILL PROGRESSION PER PAPER

### Paper 1: FOUNDATION
- ✓ Learn literature review process
- ✓ Write first algorithm + proof
- ✓ Design first experiments
- **Focus:** Get one paper right (quality > speed)

### Paper 2: DEPTH
- ✓ Reuse infrastructure from Paper 1 (saves time)
- ✓ Deepen on one dimension (reproducibility)
- **Focus:** Make one thing perfect (reproducibility as experiment)

### Paper 3: BREADTH
- ✓ Cross-domain literature (3 communities)
- ✓ Real data collection (not just simulation)
- **Focus:** Synthesis; show paper is novel across domains

### Paper 4: RIGOR
- ✓ Systems benchmarking (latency, throughput)
- ✓ Baseline comparisons (not just your method)
- **Focus:** Quantify claims; prove mathematically

### Paper 5: INTEGRATION
- ✓ Multi-dimensional tradeoffs (accuracy vs. latency vs. complexity)
- ✓ Ablation studies (justify design choices)
- **Focus:** Show design is optimal given constraints

### Paper 6: SYSTEMS
- ✓ End-to-end validation on real deployment
- ✓ Operational metrics (time-to-deploy, RBAC correctness, audit completeness)
- **Focus:** System is not just research prototype; it's viable

---

## ANTI-PATTERN CHECKLIST

Before starting each week, ask:

- [ ] Am I starting experiments before problem is defined? → STOP. Do Prompt 2.1 first.
- [ ] Do all my results look perfect? → SUSPICIOUS. Find an ablation that's not perfect.
- [ ] Am I still looking for citations? → TOO LATE. Should be done by Week 1. Do Prompt 1.1.
- [ ] Is my code messy but my paper says it's clean? → Refactor code. Paper must match code.
- [ ] Am I deferring reproducibility until submission? → DO IT NOW. 1 day per paper.
- [ ] Does my paper sound like ChatGPT? → Read it aloud. Do Prompt 5.2.
- [ ] Are there orphaned figures (not referenced in text)? → Delete or integrate.
- [ ] Is any claim not backed by results? → Rewrite or run experiment.

---

## RED FLAGS (STOP & REPLAN)

| Flag | What It Means | Fix |
|------|---------------|-----|
| "I've been on Prompt 2.1 for >1 week" | Problem isn't clear | Simplify; reduce scope |
| "Experiments not done yet, but drafting paper" | No data to write about | Pause drafting; finish experiments |
| "All 4 experiments worked perfectly" | Suspicious; no real research | Find failure case; ablate more |
| "I can't explain my results" | Design might be broken | Go back to theory; check proofs |
| "Reproducibility is 'TODO'" | Never gets done | Do it this week; block calendar |
| "Related work section is 300 words" | Skipped important papers | Redo Prompt 1.1; find 20+ papers |
| "I don't have fixed random seeds" | Results aren't reproducible | Add seed control; re-run experiments |
| "My paper reads like a manual" | Too much implementation detail | Focus on insights, not code |

---

## WEEKLY STANDUP TEMPLATE

Use this every Friday with your team (Circle A, B, C):

```
FRIDAY STANDUP (15 min)

Paper 1 Status:
  ✓ Completed: Problem formulation + algorithm design
  ⏳ In progress: Experiments (Exp 1-2 done; Exp 3-4 this week)
  ⚠️ Blockers: Need more PRAHARI data for Exp 3
  📅 On track: Yes / No / Needs help

Skill Progress:
  This week: Learned [what]
  Next week: Will focus on [what]
  Help needed: [from whom]

Reproducibility:
  Code on GitHub: ✓ / ✗
  Tests passing: ✓ / ✗
  Seeds fixed: ✓ / ✗
  README updated: ✓ / ✗
```

---

## GITHUB REPO STRUCTURE

```
PRAHARI_Research/
├── Paper1_ProvGating/
│   ├── README.md (how to reproduce)
│   ├── src/
│   │   ├── algorithm.py (Prompt 2.3 code)
│   │   ├── tests.py (unit tests)
│   │   └── requirements.txt
│   ├── experiments/
│   │   ├── run_experiments.py
│   │   └── results/
│   │       ├── exp1_latency.csv
│   │       ├── exp2_compliance.csv
│   │       └── figures/ (PDF, PNG)
│   ├── paper/
│   │   ├── paper1.md (markdown version)
│   │   ├── paper1.pdf (submitted version)
│   │   └── figures/ (editable source)
│   └── REPRODUCIBILITY.md (data dictionary)
│
├── Paper2_FallbackEngines/
│   ├── [same structure as Paper1]
│
... (Papers 3-6)
```

**Commit message template:**
```
Paper 1: Add Exp 2 reproducibility audit

- Fixed random seed (seed=42 in dispatch.py)
- Re-ran experiments 3x; all results identical
- Generates exp2_compliance.csv deterministically
- Closes issue #3 (reproducibility)
```

---

## PROMPT QUICK-FIRE REFERENCE

### Literature Review (Prompt 1.1)
```
Search: [keywords]
Expected: 30 papers
Output: Literature matrix (Paper | Year | Relevance | Gap)
Time: 2 hours
```

### Related Work (Prompt 1.2)
```
Input: Literature matrix from 1.1
Expected: 800 words, 5 subsections
Output: Ready-to-paste Related Work section
Time: 4 hours
```

### Problem Formulation (Prompt 2.1)
```
Inputs: Core claim from paper
Expected: Formal problem + Theorem + Complexity
Output: 2-3 page Methods section fragment
Time: 2 hours
```

### Algorithm Design (Prompt 2.2)
```
Input: Problem from 2.1
Expected: Pseudocode + Proof + Comparison
Output: Algorithm section (1-2 pages)
Time: 3 hours
```

### Reference Implementation (Prompt 2.3)
```
Input: Algorithm from 2.2
Expected: Working Python code, tests pass
Output: GitHub-ready code + README
Time: 4 hours
```

### Experiment Design (Prompt 3.1)
```
Input: Algorithm from 2.3
Expected: 4 experiments, each with hypothesis + method + metrics
Output: Experiment protocol (2-3 pages)
Time: 3 hours
```

### Results Analysis (Prompt 3.2)
```
Input: Raw experiment data (CSV)
Expected: Figures + Tables + Results section
Output: Figures (PDF/PNG) + Results text (500 words)
Time: 4 hours
```

### Abstract (Prompt 4.1)
```
Input: Full paper draft
Expected: Exactly 50 words, problem → result
Output: Copy-paste into paper
Time: 1 hour
```

### Full Paper Outline (Prompt 4.2)
```
Input: All previous prompts (1.1 - 4.1)
Expected: 4000-word complete draft
Output: Google Doc ready for peer review
Time: 8 hours
```

### Consistency Check (Prompt 5.1)
```
Input: Full paper draft
Expected: Checklist of consistency issues
Output: Marked-up draft with fixes
Time: 2 hours
```

### AI Language Audit (Prompt 5.2)
```
Input: Full paper draft
Expected: Risky phrases flagged + rewrites
Output: Human-voice version of paper
Time: 2 hours
```

### Reviewer Rebuttals (Prompt 6.1)
```
Input: Full paper draft
Expected: 5-10 anticipated questions + responses
Output: Rebuttal strategy document
Time: 3 hours
```

---

## PAPER TIMELINE (6 PAPERS IN 12 MONTHS)

```
Oct 2026: Paper 1 starts (Prompts 1.1 - 2.1)
Nov 2026: Paper 1 continues (Prompts 2.2 - 3.2)
Dec 2026: Paper 1 finalized (Prompts 4.1 - 6.1); Paper 2 starts
Jan 2027: Paper 2 running parallel with Paper 1 revision
Feb 2027: Paper 1 submitted; Paper 2 near completion
Mar 2027: Paper 2 submitted; Paper 3 + 4 start (parallel tracks)
Apr 2027: Papers 3 & 4 experiments
May 2027: Papers 3 & 4 drafting; Paper 5 starts
Jun 2027: Papers 3 & 4 submitted; Paper 5 experiments
Jul 2027: Paper 5 drafting; Paper 6 starts
Aug 2027: Paper 5 submitted; Paper 6 experiments
Sep 2027: Paper 6 drafting + submission
Oct 2027: Revisions on Papers 1-3 (feedback from reviewers)
Nov 2027: Papers 4-6 revisions begin
Dec 2027 - Jun 2028: Camera-ready versions; publications
```

---

## RESOURCE LINKS (SAVE THESE)

- **Claude Conversations:** Use persistent chat; export to markdown weekly
- **GitHub:** Create one repo per paper (or monorepo with folders per paper)
- **Overleaf:** If submitting to CVPR/ICCV, use Overleaf for LaTeX; git integration
- **Slack:** Daily progress updates in #research-papers channel
- **Google Drive:** Share drafts with Circle A/B/C for async review

---

## SUCCESS CRITERIA (GATE EACH PAPER)

Before you submit a paper to a venue, verify:

**Paper Readiness Checklist:**
- [ ] All prompts 1.1 - 6.1 are complete
- [ ] Internal review (Circle A/B/C) approved
- [ ] No claims without evidence (Prompt 5.1 audit)
- [ ] No AI-speak (Prompt 5.2 audit)
- [ ] Reproducibility complete (code + data + README)
- [ ] Figures are publication-quality (PDF, high res, captions)
- [ ] Page count within venue limits
- [ ] References formatted correctly
- [ ] Abstract exactly 50 words
- [ ] Author list / affiliations finalized

**Only after all boxes checked: SUBMIT**

---

## WHEN YOU GET STUCK

| Problem | Solution |
|---------|----------|
| "I don't know where to start" | Do Prompt 1.1 (literature review); it clarifies the problem |
| "My algorithm isn't working" | Go back to Prompt 2.1 (problem formulation); maybe you misunderstood |
| "Experiments take forever" | Reduce scope; one small experiment beats no experiment |
| "I can't write clearly" | Read Prompt 4.2 examples; they show structure |
| "Reviewers will hate this" | Do Prompt 6.1 (anticipate objections); address them proactively |
| "Paper sounds like AI" | Do Prompt 5.2 (language audit); rewrite risky sections |
| "I'm behind schedule" | Papers 2-6 are faster (reuse infrastructure); 8 weeks each, not 12 |

---

## FINAL CHECKLIST (BEFORE HITTING "SUBMIT")

```
✓ Read the abstract out loud (sounds like human?)
✓ Check: All 4+ experiments are done and logged
✓ Verify: No claims in paper exceed experiment evidence
✓ Confirm: Random seeds are fixed (reproducible)
✓ Ensure: GitHub repo is public + README is clear
✓ Count: All figures are referenced in text
✓ Review: Discussion acknowledges limitations
✓ Double-check: All 20+ citations are correctly formatted
✓ Proof-read: No typos; run spell-check
✓ Time-check: Paper length is within venue limits
✓ Final read: Does paper flow? Are transitions clear?

If all ✓: SUBMIT
If any ✗: Fix before submitting
```

---

**Print this. Keep it handy. Reference it daily.**

**You've got this. 🚀**

---

**Prepared by:** Alex Harmozi Framework  
**For:** Hari Om Bansal & CDRF Team  
**Date:** September 5, 2026  
**Location:** `D:\1_Projects\Research_Ongoing\CDRF_hari_om_bansal_sir\`
