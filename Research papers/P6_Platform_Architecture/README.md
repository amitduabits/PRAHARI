# P6 — Multi-authority video analytics platform

**Working title.** Descriptor-First Federation for Live Camera Estates: Onboarding
Cost, Transport Reality, and the Reconciliation Loop.

**Target venue.** IEEE TETC. Alternatives: IEEE TSC, ACM TOIT, or a systems venue
(Middleware, SEC, EuroSys industrial track). **ACM Computing Surveys is not
achievable for this artefact** — see the review's section D. A separate survey of
cross-authority video federation *is* publishable at CSUR and does not exist yet,
but it is a different paper.

**Status.** Platform model and four experiments run
(`09_Research/prresearch/p6_platform`). Literature review complete.
Blocked on an external baseline and on the transport-failure distribution.

## The claim, as it must now be stated

Not "registry rows instead of federation APIs" — that pattern has four names and is
34 years old. The claim must be falsifiable and quantitative:

> Descriptor-first federation and broker-based federation trade integration cost
> against liveness fidelity. Below X cameras per contributing authority, running a
> broker never pays back, and the crossover can be located. The cost of deferring
> integration is a reconciliation loop — a bounded sweep that reconciles registry
> rows against physical reality — whose coverage interval is the price of the
> pattern.

**What would refute it.** A measured onboarding cost for NGSI-LD registration or
ONVIF auto-onboard that is comparable to bulk CSV import at every scale. Then there
is no crossover and no design tension.

## The honest position

**"Registry rows instead of federation APIs" is a known pattern under four names:**
mediated integration over autonomous sources (`wiederhold1992mediators`,
`lenzerini2002dataintegration`), pay-as-you-go dataspace integration
(`franklin2005dataspaces`, 2005 — the closest match, and the most dangerous),
catalogue/metadata-only federation (OAI-PMH, open-data portals, NGSI-LD context
source registration), and registry/broker patterns in enterprise integration.

What is genuinely ours, framed correctly:

1. **The domain is physical, live and adversarial to metadata.** A camera row makes
   a claim about a device we do not own, that may be off, moved, re-IP'd or
   replaced. Dataspaces never had to reconcile descriptors against physical
   reality. **The sweep is that reconciliation, and it has no analogue in that
   literature. This is the defensible novel component.**
2. **The unit of contribution is legally, not technically, motivated.** Authorities
   contribute rows because rows carry no operational obligation and no uptime
   liability. No published federation design has *the contributor's unwillingness
   to operate anything* as its binding constraint, with cost evidence.
3. **Transport negotiation is the deferred-integration step**, and the resulting
   transport-mix distribution — including the ONVIF-conformance-versus-reality gap
   at 80k scale — is new and nobody has published it.

A reviewer who finds Franklin et al. themselves will reject. One who sees us
position against it in the first three pages will not.

## What makes this publishable rather than an engineering report

From the review's section B, and this is the bar:

- a stated design tension with a **falsifiable** position, including where our
  choice is the *wrong* one;
- an **external** baseline, not a three-way A/B of our own onboarding UI;
- generality that survives deleting our deployment — invariants and what breaks
  when each is dropped;
- scale claims that are load-bearing: what fails at 8,000 and what change made
  80,000 possible, reported as a knee, not a headline;
- **negative results** — the ONVIF conformance gap, the file-drop tail, the rows
  that never resolved to a live device;
- ethics with mechanism, not citation: subscriber scoping, provenance-derived
  access, tamper-evident audit, retention derived from the log-growth measurement.

Templates that cleared this bar: `verma2015borg` (one deployment, a decade of
quantitative behaviour, and the decisions they regretted) and, structurally closest,
`tang2015config` (provisioning cost as a first-class measured property).

## Files

`literature/REVIEW.md` (32 works plus standards; sections B, C and D are the
important ones), `literature/matrix.md`, `experiments/EXPERIMENTS.md`,
`paper/outline.md`, `review/REVIEWER_Qs.md`.
