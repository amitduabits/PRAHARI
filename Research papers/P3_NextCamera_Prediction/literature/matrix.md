# P3 literature matrix

| Work | Estimator | Learns topology from data | Predicts *next* vs recovers *past* | Needs appearance model | Needs road network | Cold-start policy |
|---|---|---|---|---|---|---|
| **This work** | empirical counts | yes | next, top-k | no | no | **great-circle, ablated** |
| makris2004bridging | accumulated transition evidence | yes | topology as output | no | no | none |
| tieu2005inference | mutual information, Bayesian | yes | topology as output | no | no | none |
| javed2003tracking | Parzen density over space-time | yes | correspondence | yes (CVIU version) | no | none |
| gilbert2006tracking | incremental posteriors | yes, online | correspondence | yes (colour) | no | none |
| loy2010timedelayed | cross canonical correlation | yes | topology as output | no | no | none |
| cho2019joint | joint Re-ID + topology | yes | correspondence | yes | no | none |
| gambs2012next | Mobility Markov Chain | yes | next place | n/a | no | none |
| liu2016strnn / feng2018deepmove / yang2020flashback | learned RNN/attention | yes | next location | n/a | no | learned |
| zheng2021trajrecovery | topology-informed transition times | partly | **recovers past** | yes | no | none |
| qi2021alprtraj | space-time prism + K-shortest-path | no | recovers past | no | **yes** | n/a |
| tong2021vetrac | mobility correlation + GCN | partly | recovers past | yes | **yes** | n/a |
| newson2009hmm | HMM map matching | no | matches to network | no | **yes** | n/a |
| bewley2016sort / zhang2022bytetrack | Kalman constant velocity | no | next position | no/yes | no | n/a |

The first eight rows share our estimator. The distinguishing columns are
"predicts next, top-k" and "cold-start policy", and neither is a paper on its own.

## The gap, in one sentence

*The deployment regimes in which a first-order camera-transition table suffices —
and those in which it fails — have never been characterised, even though the
estimator has been published since 2004 and shown near-optimal on mobility traces
since 2013.*

## Reading order

1. `makris2004bridging`, `tieu2005inference`, `gambs2012next` — in full, first. They own the mechanism.
2. `lu2013approaching`, `ikanovic2017alternative`, `kulkarni2019examining` — the predictability ceiling and the two critiques of it.
3. `yang2020flashback` — the IJCAI sparse-trace baseline we cannot omit.
4. `qi2021alprtraj`, `tong2021vetrac` — the road-network camp on our exact data type, with real city data.
5. `tang2019cityflow`, `liu2016veri` — the datasets we must use.
6. `lum2016predict`, `ensign2018runaway`, `pereira2022banal` — for the limitations section, which is not optional here.
