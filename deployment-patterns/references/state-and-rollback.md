# State, idempotency and recovery

## Bind every step to facts

States may be merged per project, but the following facts must not be confused.
Before initiating an action, persist the deployment/operation ID, candidate, target, desired state and previous version; callbacks use the same identity.

| Phase | Preconditions/success evidence | Failure or unknown result |
| --- | --- | --- |
| Prepare | Candidate verification, capacity, data compatibility and rollback conditions verified | Keep the original entry point; do not trigger deployment |
| Deploy/warm-up | Target exists and runs the actual candidate; dependency initialisation complete | Keep the old service; mark partial new targets as pending |
| Ready | The target's readiness/critical smoke test is satisfied | Routing traffic forbidden; record the failure; liveness does not substitute as evidence |
| Switch | The current entry point's old identity matches and the desired target is ready; the change has an operation identity | Lost response is marked UNKNOWN; query the actual entry point; no blind re-send |
| Observe/drain | Entry point actually points to the new version; evidence for new requests/old connections is complete | Missing metrics stay undecided; drain timeout keeps/terminates/rolls back per contract |
| Complete | Observation satisfied; resources and audit final states agree | Arrival of a callback does not imply everything is complete |
| Rollback | Rollback preconditions still hold; old target artefact/data available | A failed rollback enters a needs-disposition state; no looping back-and-forth switches |

Switch with compare-and-set or an equivalent version condition, so concurrent releases do not overwrite someone else's.
Repeating the same operation queries and returns the existing result without adding deployment side effects.
Stale callbacks, out-of-order results and duplicate messages may update only the matching operation and only to allowed states; a final state is not revived by a late "running".
Record cancel intent first, then propagate it; reconcile completion-versus-cancel races per the project's final-state rules.

Deployment completion and entry-point switching may run in different systems; record each target's state and reconcile the aggregate. Partial success must not be simplified into full success.
Aggregate over the required target set; state missing targets/not-run explicitly.

## Rollback branches

Trigger thresholds specify the metric, time window, minimum samples and stop conditions; "roll back if there is a problem" is not enough.
Whether execution is manual or automatic depends on existing approval boundaries; this skill grants no new execution rights.

Before rollback, re-verify old artefact/configuration/schema/data compatibility and running jobs.
When switching back is allowed, record rollback operation ID -> entry-point confirmation -> critical path/observation -> resource final state.
With irreversible migrations or an incompatible old version, keep an explicit failed/degraded state and take the designed forward-fix or data-recovery path; do not run some SQL that looks like an undo as a guarantee.

Local rehearsal manipulates only the synthetic environment; if SSH is truly needed it may only target approved local simulation containers, with target identity verified.
Production commands stay as a manual operation checklist; no production control is obtained.

On interruption, first query the actually running candidate, the entry point and the original operation record; an unknown result is neither failure nor success.
Clean up only resources confirmed stopped this run and without references; keep old artefacts until the rollback window and reference rules allow them to exit.
