# Reproduction and hypotheses

## Build a discriminating loop

First pick the narrowest entry that reaches the user's symptom.
Pure-function errors use unit tests; process/serialisation errors use the CLI or integration tests; gateway errors go through the actual local proxy chain; page-state errors use a browser.
When HTTP can only prove the interface, do not use it in place of page behaviour; for actions that cannot be automated, write the manual steps and recordable result.

Record the candidate, tool/runtime, input seed, expectation and observable result.
Run once first to confirm the target failure is hit: e.g. expected total 12 but got 10 is business red; a module that cannot be imported is environment red.
Handle environment failures by fixing the approved environment preconditions first; do not change business logic to clear the red.

When comparing good and failing samples, list the differing conditions.
Remove one input, initialisation or call step at a time and rerun the same assertion; keep the simplification only if it still fails, and restore the just-removed condition if it turns green.
Minimisation must not remove possible causal conditions such as authorised identity, ordering, clock or concurrency window.
When it is not yet proven that the minimal case and the original symptom share a mechanism, label the two separately.

## Rewrite explanations as predictions

"A cache problem" is not a testable hypothesis. Rewrite it as: "If the permission cache is not invalidated, the same user still gets the old scope after a permission change, while an approved local control that bypasses that cache returns the new scope."
Also list alternative explanations, such as the two requests using different identities.

Each hypothesis has at least supporting facts, a falsifiable prediction, a discriminating experiment, the two expected outcomes and the observation.
Prefer reading existing evidence or side-effect-free controls before considering approved instrumentation; do not pad hypotheses to a fixed count.

| Result | Judgment and next step |
| --- | --- |
| The control differs only in the changed condition and the result matches the prediction | Adds support; check whether a shared variable could still explain it, then propose the minimal fix |
| The result contradicts the prediction | Rule out the hypothesis within that scope; do not change the expectation to fit the result |
| Both groups fail or both succeed | The experiment has no discriminating power or missed; check preconditions and design a new observation |
| Insufficient observation, lost samples, task not finished | Open; keep the state, and do not record the hypothesis as confirmed or ruled out |

Match root-cause wording to its strength: a repeatable boundary divergence, where a controlled change makes the symptom disappear and restoring the condition makes it reappear, can support a causal explanation.
With only correlated logs, write "suspected, pending experiment X".
If the fix changes several conditions, the result cannot establish which one took effect.

## Intermittent failures

Pin the candidate, load pattern, seed and observation window; record attempts, failures, missing samples and interruptions, and sample within a budget that can yield information.
Do not prescribe repeating 100 times or "passing N times in a row means fixed". Zero reproductions only mean it was not observed under current conditions, not that the failure does not exist.

Injecting latency/errors can widen a race window but changes system behaviour: keep results for the original and injected conditions separately.
If the failure disappears after adding logs, record that observation may affect timing and switch to lower-intrusion observation instead of deleting the failure record.
Random ordering, concurrent resources and residual state must be reconstructible; unrelated resource contention is a candidate explanation.

## Deliver even without a root cause

List the ruled-out scope, hypotheses that can still explain the phenomenon, the most discriminating next experiment, missing preconditions and the work that can continue now.
Do not treat "all tests green" as the original symptom having been reproduced and fixed.
A small fix with an already clear root cause may reuse this evidence and is not forced to rerun the full investigation.
