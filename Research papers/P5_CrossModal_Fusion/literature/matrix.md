# P5 literature matrix

| Work | Normalised cross-detector record | Collapse within a time window | Window chosen from data | Cross-*modal* entity keying | Incident-level recall reported |
|---|---|---|---|---|---|
| **This work (reframed)** | yes (not novel) | yes (not novel) | **yes — the contribution** | yes | **yes — the contribution** |
| debar2001aggregation | yes | yes | no — convention | no, same alert type | no |
| valdes2001probabilistic | yes | yes (time proximity attr.) | no — hand-set weights | yes | no |
| julisch2003clustering | yes | clustering, not windowed | n/a | no | no |
| idmef2007 (RFC 4765) | **yes, normative** | n/a | n/a | n/a | n/a |
| ocsf / CEF / LEEF | **yes, industry norm** | n/a | n/a | n/a | n/a |
| steinberg1999jdl | **yes, mandated (common referencing)** | association stage | no | yes in principle | no |
| akidau2015dataflow | yes | **yes, named: keyed session window** | **no — explicitly a user parameter** | n/a | n/a |
| halfaker2015session | n/a | yes | **yes — mixture crossover** | n/a | n/a |
| wang2022delaytimers | n/a | yes (delay timer) | **yes — from the duration PMF against a spec** | n/a | n/a |
| jones2008beyond | n/a | yes | **learned boundary beats any fixed timeout** | n/a | yes |
| satopaa2011kneedle | n/a | n/a | **yes — reproducible knee detection** | n/a | n/a |
| fawcett2006roc | n/a | n/a | **yes — cost-weighted operating point** | n/a | n/a |
| barshalom1981tracktotrack | n/a | association gate | yes, from stated error rates | yes | n/a |
| fellegi1969theory | comparison vector | n/a | yes, from stated error rates | yes | n/a |

Read the columns: the first two are taken, twice over. **Column three is where the
paper lives, and the literature already supplies four methods for it — we simply
were not using any of them.** Column five is genuinely unmeasured in surveillance.

## The gap, in one sentence

*The operating curve of a cross-modal alert-deduplication window — duplicate
suppression against distinct-incident masking, with incident-level ground truth on
a real camera estate — has never been measured, and the window has been chosen by
convention or by first principles where the alarm-management literature has used
duration-distribution design for over a decade.*

## The five methods for choosing W, from section B of the review

1. **Mixture-model crossover** (`halfaker2015session`) — fit a two-component
   log-normal mixture to same-entity same-camera inter-observation times; W is the
   crossover where a gap becomes more likely a new presence than a continuation.
   **Recommended primary.** Caveat: `meiss2009session` shows bimodality is not
   always clean; report the fitted components and their separation.
2. **Distribution-based timer design against a stated (FAR, MAR, delay) spec**
   (`wang2022delaytimers`, `adnan2011detectiondelay`, `afzal2018timedeadbands`) —
   define MIR(W) and DSR(W) from the logs and report W* = max{W : MIR(W) ≤ α} for a
   pre-registered α.
3. **Reproducible knee detection** (`satopaa2011kneedle`) — run Kneedle on the
   normalised curve we already have; report the knee, the sensitivity S, and its
   stability across cameras. Turns our strongest empirical finding into a citable
   statistic.
4. **Cost-weighted ROC operating point** (`fawcett2006roc`, with `axelsson2000baserate`
   on base rates and `barshalom1981tracktotrack` / `fellegi1969theory` as
   precedent) — sweep W, plot masking against redundancy, take the convex hull, and
   choose where the iso-performance line of slope r = cost(missed)/cost(redundant)
   is tangent. For policing r is large, pushing W small. **Lead with this framing;**
   it makes the value judgement explicit and lets another deployment pick a
   different point from the same curve.
5. **The warning: do not defend a single global W** (`jones2008beyond`,
   `gayoavello2009survey`) — no single timeout segments sessions well, and a learned
   boundary beats the best fixed one. Report a **per-camera** W fitted by Method 1,
   show its distribution across the estate, and keep global W as the
   deployment-simplicity baseline with its measured recall cost.

**On an entropy criterion:** none was found that could be verified. Do not claim one.

## The one honest escape route for 120 s

If 120 s is not a *deduplication* window but a *case-grouping* window — the system
alerts within seconds and separately groups related alerts into a case over the
following two minutes — then a longer value is legitimate and the masking objection
dissolves. That is a two-tier design: Debar-Wespi's duplicate relation at short W,
and a consequence relation at long W. **Check whether the deployment actually does
this.** If it does, say so. If it does not, this is the redesign the data points at.
