# P2 literature matrix

## Part 1 — the fallback architecture

| Work | Second tier is a *different algorithm class* | Second tier produces the *answer of record* | Trigger is *failure*, not confidence | Shared record schema across tiers | Per-record provenance carried downstream |
|---|---|---|---|---|---|
| **This work** | yes | yes | yes | yes | yes |
| kang2017noscope | yes | no — filter only | no — accuracy target | yes | no |
| phan2020neuralsimplex | yes | yes | yes — safety violation | yes | no |
| viola2001rapid | no | no | no | n/a | no |
| teerapittayanon2016branchynet | no — same net | yes | no — entropy threshold | yes | partly (exit id) |
| wang2018idk | no — larger model | yes | no — learned abstention | yes | no |
| chen2023frugalgpt | no | yes | no — learned router | yes | no |
| ferreira2024safetymonitoring | catalogued as a reaction type | varies | yes | varies | no |

Only two rows come close, and between them they cover four of the five columns.
The fifth — provenance carried into downstream analytics — is what is left, and it
is plumbing.

## Part 2 — label-free accuracy estimation

| Method | Needs labels at target | Needs an ensemble | Needs retraining per batch | Works on a non-probabilistic classical score | Conditions on provenance |
|---|---|---|---|---|---|
| **Ours (per-stratum bins)** | no | no | no | yes | yes |
| Average Confidence / CBPE (kivimaki2025confidence) | no | no | no | no | no |
| ATC (garg2022atc) | no | no | no | no | no — but trivially could |
| Agreement-on-the-Line (baek2022agreement) | no | **yes** | no | no | no |
| COT/COTT (lu2023cot) | no | no | no | no | no |
| Projection Norm (yu2022projnorm) | no | no | **yes** | **no** | no |
| DoC (guillory2021doc) | no | no | no | no | no |
| AutoEval (deng2021autoeval) | needs a meta-set | no | no | no | no |
| Mandoline (chen2021mandoline) | **yes, a labelled validation set** | no | no | yes | **yes, via slicing functions** |
| Platanios (platanios2014estimating) | no | yes (multiple classifiers) | no | yes | no |

**Read the last two columns together.** We are the only row with a tick in both,
but Mandoline gets there with one line of user-supplied code, and every
confidence-based method in the table can be fitted per stratum without
modification. The column that is genuinely ours — "works on a non-probabilistic
classical score" combined with provenance conditioning — is narrow.

## The gap, in one sentence

*Estimating the accuracy of a production detection stream whose records were
produced by engines with incommensurable confidence semantics, without labels,
requires conditioning on which engine ran — and no published estimator does that,
though several could be made to.*

That sentence is honest and it is thin. It is a workshop contribution.

## Reading order

1. `kivimaki2025confidence` — in full, first. It explains our own negative result.
2. `garg2022atc`, `chen2021mandoline` — in full.
3. `kang2017noscope`, `phan2020neuralsimplex` — in full.
4. `lu2023cot`, `baek2022agreement` — for the SOTA table.
5. `shanmugavelu2024fpna` — for the reproducibility claim, which it partly refutes.
