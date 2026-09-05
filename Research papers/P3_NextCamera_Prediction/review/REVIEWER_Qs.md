# P3 anticipated reviewer questions

**Q1. Makris et al. did this in 2004. What is new?**
The estimator is theirs. What is new is the regime characterisation and the
prospective ranking protocol. Say this in the first paragraph, or the review is
over. — *answerable, if the characterisation is actually delivered.*

**Q2. Gambs et al. call this a Mobility Markov Chain.**
Correct; cameras as places. Cite it. — *answerable now.*

**Q3. Lu et al. 2013 showed first-order Markov nearly saturates the entropy bound
on sparse traces. Your positive result is expected.**
Yes. That is why the paper is a characterisation, not a proposal. Their result is
on CDR traces with dense sampling and per-user models over months; camera estates
give far shorter per-plate histories and a larger, more irregular state space, so
it does not transfer without evidence. — *answerable now, and it must be said before
the reviewer says it.*

**Q4. Where is Flashback? Where is DeepMove?**
**Not answerable.** Not implemented. At IJCAI this alone is a reject.

**Q5. Does it beat a global popularity prior?**
**Not answerable.** Not implemented. This is the baseline that kills papers in this
genre and it must be run first, before anything else.

**Q6. Your data is synthetic.**
Currently yes, and the claim is about deployment irregularity — a property of real
estates that a generator cannot honestly produce, since we choose the irregularity
our method handles. VeRi-776 and CityFlow are obtainable in days.

**Q7. Random or temporal split?**
Temporal. State it in the setup, with the window boundaries.

**Q8. Qi et al. get 85% on real Ningbo ALPR with a road network. Why is your
number better?**
**Not answerable** until we run on comparable data. Match their experimental design
and either replicate or contradict their ~50% minimum-coverage finding.

**Q9. Micro or macro average?**
Both, with the macro number in the main table. A micro-average is dominated by hub
cameras.

**Q10. This makes suspect-vehicle interception cheaper. What about misuse?**
Answer with mechanism, not sentiment: transition tables inherit the spatial bias of
where cameras were installed (`lum2016predict`, `ensign2018runaway`), and ALPR
network analytics have a documented function-creep record (`pereira2022banal`).
State what we do not claim.
