# Claim-to-evidence table (template)

One row per claim that appears in the abstract or introduction. A claim with no row
does not go in the abstract. Copy this into `<paper>/experiments/EXPERIMENTS.md`.

| # | Claim (as it appears in the abstract) | Experiment | Figure / table | Data: real or synthetic | Status |
|---|---|---|---|---|---|
| C1 | | | | | supported / refuted / not run |

Status vocabulary, used consistently across all six papers:

- **supported** — the experiment ran and the result holds. Say in the next column whether the data was real or generated.
- **refuted** — the experiment ran and contradicts the claim. Keep the row. Change the claim, not the row.
- **definitional** — the result follows from the design and is not evidence. Present it as an invariant with a proof, never as a finding.
- **not run** — no evidence exists. It may not appear in the abstract.
