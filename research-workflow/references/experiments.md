# Experimental method

Use this page for experimental design, execution, resumption, and result interpretation in machine learning
algorithm research. Project instructions decide actual machines, devices, paths, and scheduling. The closest
open-source paper's framework is the starting point for a new idea; existing final scripts and records govern
replays and closely related experiments.

## Design the comparison

- Start from the paper's central question and proposed explanation. Map each essential mechanism claim to a
  predicted observation, a controlled test, and a result that would weaken it. Then test the practical gain
  that follows from the explanation. Keep mechanism evidence and outcome evidence distinct: an outcome gain
  alone does not prove the proposed reason for that gain.
- State the claim and estimand: the outcome, unit of analysis, population or workload, and effect of the
  proposed change. Choose a baseline that a knowledgeable reviewer would consider competitive, not one
  weakened by an avoidable implementation difference.
- Fix artifact or model version, data and selection rule, sample count, intervention or training state,
  randomization, evaluation procedure, and compute conditions as relevant. For paired comparisons, say which
  factors are identical and which one changes.
- Define the observation window and included work. For runtime claims, specify timer boundaries, concurrency,
  warmup, repetitions, and aggregation before looking at favorable measurements.
- Define each metric's numerator, denominator, unit, and aggregation. Distinguish counts from rates,
  per-item from per-group outcomes, and intermediate proxies from the primary outcome.
- Plan a short correctness or feasibility gate before a costly run. Include the quality and training
  comparison needed for the claim, but do not launch a full study when a small controlled test answers the
  narrow question.

An ablation must isolate its claimed cause. If a historical comparison changes several algorithmic or
implementation factors together, label it a combined comparison and add a matched control for causal
attribution. Record the original plan and any protocol change; a new protocol produces a new comparison rather
than silently replacing the old one.

Tune where needed for a fair and competent implementation, applying comparable budgets and recording choices.
Do not make repeated score-seeking the research plan or present a tuned gain as proof of the underlying
explanation. If the diagnostic evidence contradicts the insight, revise the claim or investigate the conflict
before extending the performance table.

Choose rows from the claim and the adopted baseline framework. A useful comparison matrix often contains the
reference method, a strong alternative, the proposed full method, and one controlled removal per claimed
component. For each row, name the sole intended difference and any unavoidable implementation difference. If a
row shares a configuration with another table, point both tables to the same measurement identity.

Write the acceptance criterion as an observable result before running. It may be a numerical threshold
supplied by the project, a paired improvement with stated uncertainty, a correctness invariant, or a
qualitative failure mode. Do not invent a target just because a table needs a winner. The optional
[protocol card](../assets/experiment-protocol.md) carries these decisions into an existing plan.

## Track and execute

For each active idea, maintain `TASK.md` with its research question, adopted baseline framework, plan, decision
gates, and next experiment, and `PROGRESS.md` with completed steps, observations, run identities, and open
issues. Re-read `TASK.md` before starting each step; update `PROGRESS.md` after completing one. Use the
project's established locations and conventions when they exist. Keep a distinction between a working script
and a script the author has marked final for an experiment.

1. Locate the original metadata, command, script, and raw records. Verify that a candidate script actually
   implements the requested boundary; reuse it if it does. For a related new experiment with an existing final
   script, copy that script and change only the method-specific logic. Preserve all other experimental logic;
   do not redesign the adopted experiment framework. Ask the author after each experiment whether to mark its
   script final.
2. Check data, artifact version, environment, resources, and resume boundary. Run the preflight required by
   the project before a long job. Respect project scheduling and other active jobs; preserve a valid recovery
   point before pausing a job when the project requires it.
3. Run with the fixed protocol, preserving the command, environment, code identity, raw logs, output samples
   or hashes when relevant, and failure records. Place a rerun in a new output directory. Do not overwrite or
   splice partial records into a complete run.
4. On interruption, inspect the last committed state and actual process state before resuming. Continue
   from a supported boundary and record any changed condition. A failed or cancelled job stays distinguishable
   from a completed job.
5. Derive summary statistics from the raw record and check that its observation count, repetitions, sample
   count, and configuration match the intended comparison. Reuse one measurement record wherever the same
   configuration appears in several tables.

Compute the declared summary and contrast from raw observations, preserving the unit of analysis, weighting,
and pairing. For distributed measurements, document any cross-device aggregation. Report variability when the
comparison is noisy, and never select only favorable repetitions after observing results.

Analyze in this order: verify the record count and identities; reconstruct each observation's measured event;
apply the declared aggregation; compute per-method summaries; compute the declared contrast; inspect dispersion
and outliers without discarding them post hoc; then compare with historical records under their own protocols.
Judge any output mismatch against the actual correctness criterion rather than treating a convenient proxy as
a verdict.

When the claim concerns a complete workflow, measure that workflow directly. Component timings cannot
reconstruct total elapsed time when operations overlap. A pilot, a component measurement, and a full study
describe different scopes even when their labels sound similar. Keep their results and conclusions separate.

## Advance the research

After each diagnostic or comparison, record the observation, its uncertainty, and which explanation it
supports or weakens. Decide the next smallest test that would change the research decision. Prioritize tests
that separate competing explanations, verify a necessary condition, or remove a major threat to the paper's
main claim. State whether to continue, revise the method, broaden evaluation, or stop the direction, and
record why. A negative result is evidence to analyze, not an automatic reason to run a larger version of the
same experiment.

Update the claim-to-evidence map and planned paper figures as results mature. Keep open questions and missing
cells visible, and distinguish planned work from completed work in status reports. If a result changes the
central claim, revise the experiment plan and manuscript argument together.

## Interpret and deliver

Check surprising gains and regressions against the old runner, observation boundary, artifact version, input,
selection rule, workload mix, and aggregation before attributing them to the method. A historical positive
result is evidence to reconcile, not a reason to force the new number to be positive. Preserve both records
and explain why they differ when the protocols do.

The result should identify the matched baseline, actual event measured, number of observations, aggregation,
method versions, and any protocol deviation. Mark unrun cells as missing. Put raw provenance and audit details
in a separate existing project record when the author asks only for a table. Keep diagnostic measurements
available without presenting them as paper-ready evidence.

Example: a preprocessing method claims to reduce total analysis time. A shorter preprocessing stage supports
that component claim; the total claim needs a direct measurement of the complete analysis. When preprocessing
and computation overlap, summing their separate durations does not estimate elapsed time.
