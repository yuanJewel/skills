# Deviation judgment and recovery

Read this page when a task cannot continue as expected. First save the recoverable candidate identity, failing inputs/outputs, related execution handles and completed parts; do not change the acceptance criteria first to make the implementation "pass".

## Decision table

| Observation | How to distinguish | Action that may continue | Not yours to decide |
| --- | --- | --- | --- |
| Implementation differs from an explicit requirement | Original requirement/approved acceptance is clear, current behaviour differs | Find the root cause and fix within this task's write scope; add a meaningful regression | Widening permissions or changing the requirement to fit the implementation |
| Ordinary implementation choice differs from sketch code | External behaviour/contract/scope unchanged, existing project pattern applies | Decide the minimal reasonable implementation and explain necessary deviations | Treating the sketch as immutable design, or hiding a real interface change |
| Test/environment failure | The error occurs before the target behaviour, e.g. missing tool/wrong entry | Fix the environment this task controls or use an allowed check method; mark the unverified boundary | Installing unauthorised dependencies, changing others' environments, recording "not run" as pass |
| Plan contradicts original requirement/interface | Point to both locations, versions and the concrete field/behaviour | Stop the dependent part, provide the precise conflict and minimal options; continue independent items | Changing to a new requirement yourself, signing approval on someone's behalf |
| Out-of-scope discovery | No necessary dependency on this task's acceptance, or no write permission | Record fact, impact and location, hand to the authorised maintainer | Fixing files without write permission in passing, or forcing scope expansion |
| External action needs permission not yet granted | Current authorisation does not cover the side effect | Complete reviewable preparation and follow the existing permission flow | Switching tool/execution channel to bypass the limit |

A "plan error" needs evidence: for example task A promises an optional field while task B rejects empty values as required; or approval covers read-only queries while the plan schedules write-back. Provide the conflicting text and affected acceptance; do not use the vague "the approach is unreasonable". Plan body and approval handling go to `plan-design` / the existing decision flow; do not create a second body.

## Quality of failure evidence

Record the command actually executed and its environment identifier, candidate content identity, inputs, exit code, key output and business assertion. Keep long logs at the allowed evidence location and verify in segments per the project's line/byte conventions; truncation does not count as a full read. Example commands are never auto-executed; check side effects and the project's real entry first.

A bug case's red light must point at the problem being fixed. If a new case passes on the first run, check whether the original behaviour was already correct, the assertion too weak or the path not invoked; do not fabricate a prior failure record. When it cannot be reproduced, state the missing conditions and adopt a feasible equivalent verification, but never claim the original fault was reproduced.

Exit 0 with a failed assertion counts as failure; non-zero exit due only to an unmet environment prerequisite counts as unverified/environment-blocked, not a product bug. A passing test proves only the recorded inputs and paths; integration, performance or real-service capabilities not exercised are listed separately.

## Re-entry and stopping writes

1. Verify the approval still applies; read current file identifiers and checkpoints, do not trust a "done" label alone.
2. Check whether old commands or child executions are still running; do not re-run side-effecting actions until a stop is confirmed.
3. Compare existing changes against expectations and preserve others' work; locate changes of unknown origin first, never overwrite and explain afterwards.
4. Pick the smallest unfinished task to continue. Re-verify only when candidate/dependency changes affect evidence; do not mechanically repeat the full test run.
5. Stop writing at the delivery boundary and give done, not done, unverified, current in-flight work and next step; keep this recovery information even when blocked.

Cancellation or budget overrun does not automatically authorise deleting results. When retention or archiving is needed, consume `archive-maintenance` and handle only files you are authorised to handle; important evidence is never cleaned up before the receipt is written.
