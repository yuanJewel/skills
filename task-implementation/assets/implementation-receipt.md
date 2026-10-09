# Implementation receipt

- Task and approval: {{goal, task/phase locator, approved version or explicit instruction source}}
- Status: {{author done / still unfinished / awaiting evidence; separate from independent acceptance}}
- Candidate and write permission: {{files actually changed, content identifier/version, sole writer and stop-writing state}}
- Implementation result: {{which behaviour changed, why, which existing contracts were used}}

## Acceptance comparison

| Acceptance behaviour | Expected | Actual | Environment/input and evidence | Judgment |
| --- | --- | --- | --- | --- |
| {{specific behaviour}} | {{observable assertion}} | {{real result}} | {{candidate identity, command/manual check and log location}} | {{pass / fail / unverified}} |

Bug or new-behaviour regression: input/evidence of the failing reproduction, whether the failure cause is really the target behaviour, result after the fix. When not applicable (pure copy etc.), state the reasonable check adopted; do not fill in a fictional red light.

## Deviations and limits

List the plan's original location, actual difference, reason, impact on requirements/interfaces/resources and the authorisation basis. Plan conflicts record evidence from both sides; without a decision they are not written as accepted. Checks not run, environment gaps and untested paths are listed separately; exit codes do not replace business conclusions.

## Resource cleanup

- Reclaimed: {{containers/images/processes/ports/temporary files/test data, each with identity}}
- Kept and why: {{evidence retention, user request, still referenced or no permission to delete}}
- Cleanup failures and next step: {{object identity, failure reason, who handles it and when; write "none" if none}}

## Recovery and handover

Completed and still valid parts, remaining tasks, dependencies, existing checkpoint, related execution handles and stop facts, next step and writer. The result is consumed by the existing status maintainer and reviewers; do not create another overall plan or user workbench.
