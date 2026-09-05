# P4 — Decoder admission and probe coverage under one budget

**Working title.** One Budget, Two Jobs: Allocating Concurrency Between Decoding
and Health Probing in Large Camera Estates.

**Target venue.** IEEE TMM or ACM TOMM. A systems venue (Middleware, SEC, or the
ICPE/ATC industrial track) is also plausible and possibly a better fit.

**Status.** Simulator and four experiments run (`09_Research/prresearch/p4_admission`).
Literature review complete. **Reframed: the admission policy is not the
contribution.** Blocked on multi-resource measurements.

## The claim, as it must now be stated

Not "refuse at the bound gives a flat tail" — that is Erlang-B, 1917, and a
multimedia reviewer will know it. The claim is:

> When one concurrency bound K serves both decoder admission and the reachability
> sweep, the refusal probability B(K,a) and the coverage interval ⌈n/K⌉·T become
> functions of the same parameter, so the operator faces a real allocation problem
> between detection latency and session refusal. We characterise that frontier and
> derive the three-strike constant from a target false-alarm rate rather than
> asserting it.

**What would refute it.** A measurement showing the frontier is flat over the
operating range — that any split of K between decode and probe gives
indistinguishable outcomes. Then the allocation problem is not real.

## The honest position

**Refuse-at-the-bound with no queue is the M/M/c/c loss system.** Consequences the
paper must accept, not argue with:

- "Peak envelope is exactly K, independent of estate size" is **definitional**. The
  state space is {0,…,K} by construction and n enters only through λ. Demonstrating
  it at 800 and 80,000 cameras shows the semaphore has no bug, nothing more.
  Present it as an invariant with a one-paragraph proof, never as a finding.
- "p99 flat across load" is **definitional** too. In a loss system there is no
  waiting time, so an admitted session's sojourn is its own service time. A flat
  p99 measures the service-time distribution.
- `sevastyanov1957` insensitivity is the theorem that makes any of this rigorous
  for real, wildly non-exponential decoder sessions. Cite it as our proof device.
- `das2002swim` already gives round-robin probing at bounded rate plus multi-strike
  hysteresis. The health half of the paper is SWIM unless the coupling is the story.

**The sharpest attack, which must be pre-empted: we may not have a loss system at
all.** A refused session retried on the next sweep is a *retrial (orbit) queue*.
The queue has not been eliminated, it has been moved into the sweep and made
invisible to our instrumentation. Under that model the blocking probability is not
Erlang-B and "no queue" is false as stated. Either prove refusals are never
retried, or model the retrial queue and report orbit occupancy.

## Files

`literature/REVIEW.md` (31 works; sections B, C and D are the important ones —
the Erlang verdict, the four propositions to prove, and the 24 measurements a
systems reviewer will demand), `literature/matrix.md`,
`experiments/EXPERIMENTS.md`, `paper/outline.md`, `review/REVIEWER_Qs.md`.
