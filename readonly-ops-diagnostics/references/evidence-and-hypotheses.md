# Time, evidence and hypotheses

## First unify time to the same instant

Every piece of evidence keeps its original time string, time zone/offset, precision, collection window, source clock and known skew.
Times with an offset can be converted to a unified instant for comparison; for times without a time zone check the project contract first, never guess the local time zone.
Different precision, buffered log writes and asynchronous transport require a time-uncertainty interval; when ordering overlaps, establish no strict before/after.

For example, 10:00+08:00 and 02:00Z are the same instant; the former is not eight hours later. A log that says only 10:00 with unknown time zone stays unknown.
Time corrections keep the original; never edit the original log directly.
Correlation IDs/operation IDs and monotonic stage sequence numbers help, but verify whether they are unique across processes.

## Falsifiable hypotheses

A symptom states who saw what and when; a trigger is a correlated change; a root cause needs a mechanism and counter-evidence.
"Timeouts appeared after the deployment" does not mean the deployment caused the timeouts.
Rank by likelihood x impact x verification cost, but do not treat subjective scores as evidence.

| Hypothesis | Support | Counter-evidence/alternative explanation | Smallest distinguishing probe | Conclusion |
| --- | --- | --- | --- | --- |
| Pool exhaustion causes queueing | pool_wait rises in the same window | Normal concurrency with timely connection return weakens it; dependency latency can also exhaust the pool | Bounded pool wait/active/return metrics | Supported/weakened/unknown |
| DNS/connection establishment failure | Errors in the connect phase | If established connections fail too, investigate the server side instead | Per-phase latency/error category | Not verified by restarting |

Look first for evidence that distinguishes competing hypotheses; do not search for synonymous log lines to support the first guess.
Each conclusion links the exact evidence range and records uncovered time/targets and conflicts.
No logs does not mean no behaviour, especially when sampling/rotation/buffering gaps exist.

## Output and recovery

The report separates observed facts, mechanism inferences, remaining unknowns and the next step.
Confidence explains its basis, e.g. "two independent metrics agree, but the connection-return trace is missing"; do not give precise percentages by feel.
Keep safe summaries of contradictory evidence as they are; never delete samples that do not support the conclusion.

The smallest next step carries a target, allowed read-only action, expected supporting/refuting result and stop condition.
If distinguishing requires reproduction/latency injection/restart, explicitly hand off to a separate approved test or implementation task; this diagnosis does not execute it automatically.

After a fix, verification on the same candidate/same symptom is still needed; "restart recommended" cannot be written as "recovered", and a brief non-recurrence does not mean the root cause is resolved.
Handover on interruption keeps evidence times and in-flight work; old conclusions are revised with new evidence, and historical originals are not altered.
