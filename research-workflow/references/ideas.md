# Idea assessment

Use this page for a proposed machine learning algorithm, a novelty question, or a stalled research direction.
The output should help the author decide what to test or write next; a brainstorm alone does not authorise
training.

## Define the proposal

1. State the task, modality, data, target metric, and actual bottleneck in the author's terms. Keep a changed
   task or modality explicit rather than silently substituting one from an older plan.
2. Explain the mechanism: what state or computation changes, where it enters the existing method, and which
   behavior should improve. Separate the core method from optional implementation tricks.
3. Search the closest open-source paper in the same research field. Read its paper and code, clone its
   repository, and inspect its experimental framework. Use that framework and its strongest relevant baseline
   for the first validation rather than designing a new benchmark or overall experiment framework. If the
   closest same-field work has no usable code, adapt a general baseline framework from the next broader field.
   Reproduce a baseline when its behavior or measurement is uncertain and affects the proposed gain.
4. Judge novelty against current work in the same field. Name the overlap precisely: same problem, same
   mechanism, same setting, or only similar vocabulary. For a similar method in another field, alert the
   author and explain the connection; do not add it to the baseline or Related Work without the author's
   direction. If omitting a materially relevant source would mislead the paper, surface that conflict.

Classify the contribution before naming it: a new objective, a new inference or training mechanism, an
extension to a new setting, or a better implementation of an established mechanism need different evidence.
For a systems optimization, a quality-preserving speed gain can be valuable, but it should be described as
such. For a new learning objective, speed alone cannot validate the central claim.

## Make the idea falsifiable

For each proposed contribution, write a predicted observable effect, a plausible competing explanation, and
the smallest experiment that distinguishes them. Include a quality or correctness check when speed alone could
hide changed behavior. An ablation should remove one contribution at a time while preserving the same backbone
and measurement protocol.

For an explanatory insight, ask what would be observable if its account of the problem were correct, and what
would contradict it. Separate evidence for that mechanism from evidence that the method improves an outcome.
An improved benchmark score may justify practical interest, but cannot by itself establish why the method
works. Hyperparameter search can refine a method under a fair protocol; it cannot replace a testable research
claim or rescue an explanation contradicted by diagnostic evidence.

Build an evidence ladder, choosing the cheapest rung that could rule out the idea:

1. **Analytical or code check:** confirm the proposed state transition is possible, that it reaches the
   claimed bottleneck, and that the baseline is represented accurately.
2. **Small diagnostic:** measure the mechanism's direct signal, such as an error pattern, calibration,
   convergence, or resource use. State why this proxy should predict the final metric.
3. **Matched outcome test:** run the strongest relevant baseline and the new method on the same workload, then
   check the claimed benefit and any quality or correctness trade-off.
4. **Generality test:** vary the model, dataset, batch, length, or task only where the paper intends to claim
   generality. A second setting does not repair an invalid primary comparison.

The next rung is justified by the observation, not by a fixed rule to run every stage. If a negative result
has several explanations, use a discriminating test before changing many design choices at once.

Judge separately whether the idea is technically executable, empirically promising, novel relative to the
closest work in its field, and substantial enough for the intended paper. To reject an idea, give persuasive
theoretical analysis and experimental evidence where feasible; a failed first variant alone is not proof
that the whole direction is impossible. If a proposed evaluation seems to need human judgement, first check
whether an established dataset, automatic metric, or focused annotation protocol can answer the same claim.
State what each alternative can and cannot prove.

Mechanism feasibility plus no direct same-field collision is enough to begin a paper draft. The principal
comparison can mature while drafting; mark predicted trends in source comments until measured. When the main
comparison table is ready, actively remind the author that the paper draft can proceed. After each experiment,
ask the author whether its script should be marked as the final script for that experiment.

When evidence is weak, give the current verdict and the experiment that could change it. If the direction no
longer fits the author's stated modalities or research question, surface that conflict before spending
resources. When the author asks for explanation, describe each idea as problem, mechanism, baseline, novelty,
and current evidence; avoid substituting a status log for the argument.

Example: a new augmentation improves accuracy. Start from a close, open-source augmentation paper in the same
field, reproduce its reported baseline in its framework, and change the augmentation while matching the data,
backbone, and training budget. If the budget also changes, the result cannot isolate the augmentation's effect.
