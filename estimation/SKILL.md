---
name: estimation
description: Estimate effort, elapsed time and resource usage for a plan or release phase, calibrate expectations against dependencies and parallel capacity, and verify actual usage at delivery or takeover. A short Q&A does not get a budget sheet; an estimate does not replace plan approval, dispatch or automatic timeout termination.
metadata:
  version: "0.1.0"
---

# Time and resource estimation

Give the user expectations they can judge, and correct them promptly when evidence changes. State accumulated effort, actual elapsed time, waiting and resources separately; never merge them into one seemingly precise completion moment.

## Required inputs

Consume the existing plan; do not copy it for the estimate:

- deliverables, acceptance and task slices;
- dependencies, file write sets and environment conflicts.

Then take the host limits and samples given by project configuration:

- grade words and reasoning weights (grade words map to actual execution configuration through the project resource mapping);
- execution channels, platform capacity and concurrency quotas;
- occupancy by the main task and unknown in-flight work, machine limits;
- available historical samples.

When price or usage is missing, write unknown; time and occupancy estimates can still be given. When a key interface or acceptance scope is missing, give a conditional range and state which decision would change the forecast. Resource units are a project scheduling rule, not currency or a measured cost multiplier; never treat a model tier name as a price list.

## Estimation and calibration loop

1. **Split work by outcome.** Count research/design, implementation, verification, independent acceptance, fixes and integration into the acceptable task they belong to; fix shared prerequisites first, then split independent parts. Different packages, tests or files are not inherently parallel tasks.
2. **Build evidence-based ranges.** Use similar tasks, pending-verification items or a small trial to give each item an effective-hours range, noting basis and uncertainty. Without historical samples, mark the first estimate low confidence; do not invent percentiles or fixed per-file durations.
3. **Lay out a feasible timeline.** Read [Critical path and capacity](references/critical-path-and-capacity.md); compute the longest dependency chain first, then add main-task occupancy, independent resource pools, execution channels, file/environment conflicts and the acceptance queue. Total effort divided by head count is not a feasible duration.
4. **Give the user choices.** Embed the required fields of the [estimate template](assets/estimate.md) in the existing plan, stating current scope, expected elapsed time, accumulated effort, limiting factors, waiting and unknown cost. When the user asks to shorten time, offer evidence-based parallelism, reduced waiting, phasing or reduced scope with their costs; do not pass off cutting tests as an equivalent speed-up.
5. **Calibrate when the first group completes.** Per [Calibration and usage](references/calibration.md), verify authoring, review, rework, waiting and actual coverage; keep the original estimate and update the remaining forecast. On clear delay or changed prerequisites, proactively report cause, impact and feasible options; never extend silently and indefinitely.
6. **Reconcile at phase end.** Against the original scope and acceptance, list actual results, accumulated usage, unfinished items and the next-phase forecast; hand over to the existing `context-handoff` checkpoint. When switching sessions keep the task-level ledger; do not restart a new execution as zero cost.

An estimate does not by itself authorise dispatching subtasks, changing executor/execution channel or raising concurrency; actual execution is handled by `subtask-dispatch`, which consumes the capacity and recommendations. When the matching method is unavailable, follow the project's existing process; installing the whole library is not required. Without a new user decision, continue the authorised scope; do not request start approval again for routine calibration.

## Failure, change and exit

- For a failed request, first establish whether it executed, whether usage is available and whether it is still in flight; unknown is never filled as 0, never releases occupancy and never triggers a full re-dispatch. Count retries into waiting and extra usage per the current task policy; do not build the same retry count into every project.
- Dependencies or machine capacity unproven: give the conservative path and the improvement once the prerequisite holds, separately; do not list ideal parallelism as a commitment.
- User does not accept the expectation: shorten non-essential waiting and adjust independent scope where possible; when acceptance must change or the phase must end, give the concrete impact and let the current user decide. Never terminate, archive or lose in-flight work on your own because the estimate time was reached.
- Actuals not visible or counting scopes overlap: list the visible part, the gap and the counting boundary; do not fill in reasoning tokens, and do not double-add cache or billing costs.

## Verification and resource recommendation

Check three counterexamples: serial dependencies cannot be divided by concurrency, remaining capacity is insufficient after main-task occupancy, and an environment bottleneck is smaller than the execution slots; then check user shorten-time choices, disconnect retries, cross-session accumulation and missing prices. Correct arithmetic does not mean accurate effort; samples and prerequisites must be given together.

Organising an existing ledger can use `low/low`; critical path and complex capacity `normal/medium`; architectural uncertainty `normal/high`. Grade words map to actual execution configuration through the project resource mapping. Simple estimates are done by the main task; only complex, independent data organisation is delegated, per authorisation. Do not hard-code service provider, reasoning weight or head count.

## Sources

1. Pinned sources: [SP02 writing-plans](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/writing-plans/SKILL.md), [EC02 cost-aware-llm-pipeline](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/skills/cost-aware-llm-pipeline/SKILL.md).
2. SP02 lends task boundaries with explicit files/interfaces that are independently acceptable; EC02 lends per-task routing, accumulated ledger and transient-retry classification. Critical path, constrained parallelism, ranges and takeover reconciliation are own-authored for this package.
   Dropped commits/worktrees, fixed step sizes, fixed models and prices, character thresholds and automatic termination on budget exhaustion.
3. License: shipped with the package as [LICENSE-SP.txt](LICENSE-SP.txt) (SP, MIT) and [LICENSE-EC.txt](LICENSE-EC.txt) (EC, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license files along when copying this package alone.
