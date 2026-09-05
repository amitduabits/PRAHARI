# P1 literature matrix

Columns are the four properties that separate the proposed method from everything
else found. A tick means the work has the property; a cross means it does not.

| Work | Decision made *before* inference | Enforced by *absence* of the callee | Input is *device provenance* | Domain is *ML model dispatch* |
|---|---|---|---|---|
| **This work** | yes | yes | yes | yes |
| roesner2014wdac | no — detectors run per frame to find the policy | no | yes (world-attached) | partly |
| bagdasaryan2019ancile | no — interpreted per operation | no — module resident | no (data-attached) | yes |
| watson2010capsicum | yes | yes | no (no provenance) | no (OS objects) |
| liu2008xengine | yes (compiled) | no — decision returned per request | no | no |
| park2012pbac | no — runtime DAG query per access | no | yes | no |
| romero2021infaas | no | n/a — lazy load is for cost | no (SLO) | yes |
| yip2009resin | no — checked at output boundary | no | no | no |
| myers1997difc | yes (static labels) | no — constrains flow, not instantiation | no | no |
| cangialosi2022privid | no | no — model runs on raw pixels | no | yes |
| poddar2020visor | n/a — hides pixels from operator, runs all models | no | no | yes |
| jana2013darkly | no | no — degrades input for all apps | no | partly |
| kim2023erebus | no | no — recognizers still run | no | yes |
| aditya2016ipic | no — face matching per frame | no | no (subject consent) | partly |
| byun2008purpose | no — per query | no | yes (purpose) | no (relational) |
| mitchell2019modelcards | n/a — prose only | no | yes (documentation) | yes |

**Rows 3, 4 and 5 are where the argument lives.** Capsicum has the enforcement
discipline but no provenance and no models. XEngine has the compilation but still
evaluates per request. Ancile has provenance-that-gates but keeps the forbidden
module resident. No row has all four ticks except ours.

## The gap, in one sentence

*No published system derives, at device-enrollment time and from the device's own
provenance, a static set of inference engines that may ever run on its frames, and
enforces it by never constructing the excluded engines — so the distinction
between a model being invoked and its output being released has never been
measured.*

Read that aloud to someone who has read Capsicum, XEngine and Ancile. If they say
"so it is Capsicum for model registries", they are right about the mechanism, and
the answer must be the measurement, not a denial.

## Reading order

1. `roesner2014wdac`, `bagdasaryan2019ancile`, `watson2010capsicum` — in full, first.
2. `liu2008xengine`, `cangialosi2022privid` — in full.
3. `park2012pbac`, `romero2021infaas`, `kim2023erebus` — in full.
4. Everything else from the abstract until it matters.
