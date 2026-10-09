# Resource reservation, occupancy and recovery

Read this page on first dispatch, insufficient resources, unclear requests or recovery. Use the project's existing status store; the following are semantic fields and do not require a new ledger file.

## Start decision

Compute per independent resource pool: available units = pool limit − units of all reserved/running/unknown in-flight executions. Use the project's grade-word and execution-channel mapping to obtain this run's cost; the same model with different reasoning may cost differently, so never count by model name alone. When the main task has real run cost it is counted in its pool too.

Dispatch only when this run's cost does not exceed available units and a host slot is actually free. A free unit in another pool does not offset a shortage in this one; renaming, switching tool or switching session creates no new available units. When configuration lacks weights or the host gives no reliable state, mark unknown and stop new starts that depend on that data.

For example, with a synthetic limit of 7 and a request cost of 8, dispatch must be refused even with an empty task list. With limit 10, 4 used and 4 needed but no free platform slot, still wait. The numbers only illustrate the calculation and are not default configuration.

## Two status axes

| Business result | Execution fact | Resource handling |
| --- | --- | --- |
| Pending or blocked | Still running/paused but not terminated | Keep occupancy |
| Done | Checks/uploads/child executions still in flight | Keep occupancy until all end |
| Not done | Dispatch confirmed failed, platform confirms it never started | Release reservation, keep the failure record |
| Any | Request result unknown or stream broken | Keep occupancy, query the original execution |
| Any | All related executions confirmed ended | Release occupancy, keep actual usage |

## Minimal persistent information

Logical task ID, execution attempt ID, real platform handle, resource pool and weight basis, reservation time, execution-state evidence, end time, accumulated usage, latest checkpoint. Logical task and attempt are separate, so querying the same request does not create new usage. When the platform provides no usage data record "unavailable"; do not pass reserved units or wall-clock time off as billed usage.

Write the reservation before dispatch; add the handle after success; release when clearly not started; query when unclear. If writing the ledger fails, stop new dispatches first and restore the mapping; never send several and backfill later.

## Re-entry recovery

1. Read the approved version, original task, original handles and the checkpoint with the last recorded usage.
2. Query the real execution and its related child executions; without query capability rely on verifiable stop evidence; if still uncertain keep the unknown in-flight entry.
3. Compare existing artefacts and do not redo verified parts. If the old execution is running, keep waiting or contact the original executor; confirm a stop before taking over write permission.
4. After a new attempt is approved, append only its reservation/usage; existing records remain; releasing occupancy does not zero accumulated usage.
5. Hand recovery results to the existing status maintainer. History retention follows the `archive-maintenance` method; never clean up handles and evidence still needed for location.

When budget or elapsed time exceeds expectation, first give completed work, remaining dependencies and a revised estimate; whether to continue is judged by existing authorisation and budget limits. Never split a task into several aliases to get around resource limits.
