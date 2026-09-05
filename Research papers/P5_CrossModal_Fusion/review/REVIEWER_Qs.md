# P5 anticipated reviewer questions

**Q1. IDMEF standardised a detector-agnostic alert record in 2007. Why is your
schema a contribution?**
It is not. Say so in the background section. — *answerable now, once the claim is dropped.*

**Q2. Debar and Wespi defined a duplicate relation over a normalised record with a
time window in 2001.**
Correct. Ours differs only in that the equivalence class is entity identity *across
modalities* rather than alert-type equivalence, and we report incident-level recall
where they do not. Concede the rest. — *answerable now.*

**Q3. This is a keyed session window with gap W. Dataflow named it in 2015.**
Yes. Use their vocabulary and stop implying the construct is new. — *answerable now.*

**Q4. Process control has picked debounce timers from duration distributions for
over a decade. Why did you derive yours from geometry?**
We should not have. The paper's finding is that the geometric derivation is wrong
by one to two orders of magnitude, and we adopt the distribution-based method
instead. — *answerable, and it becomes a strength once stated this way.*

**Q5. Why is W global rather than per-camera or learned?**
**Not answerable.** `jones2008beyond` shows no fixed timeout segments sessions well.
Fit W per camera, report the distribution, and keep global W as the
deployment-simplicity baseline with its measured cost.

**Q6. Is your window anchored to the first observation or does it merge on activity?**
**Not answerable** for the deployed matcher. Check `app/services/matcher.py` against
the research implementation and state the semantics precisely.

**Q7. Where is the Valdes-Skinner multi-attribute similarity baseline?**
Not implemented. It is the closest alternative design and must be in the table.

**Q8. Your incidents are synthetic, and your generator creates the revisits that
produce the masking you measure.**
Correct, and it is the paper's largest weakness. Needs a labelled window of real
detections with operator-marked incidents.

**Q9. You report alert reduction. What is the operator burden?**
Alerts per operator per hour, per `eemua191` and `wang2016alarmoverview`. Not yet
reported.

**Q10. Could 120 s be a case-grouping window rather than a deduplication window?**
**Check this before submitting.** If the deployment alerts within seconds and groups
into cases over two minutes, the masking objection largely dissolves and the paper
becomes a two-tier design description.
