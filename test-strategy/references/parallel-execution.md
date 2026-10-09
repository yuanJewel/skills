# Parallel sharding, aggregation and recovery

## Define resources before sharding

Each shard needs stable case IDs, the candidate, prerequisites, data/files read and written, environment/ports, an output directory, an estimated duration and completion evidence.
Treat shared mutable fixtures, global switches, the same deployment target and executors that cannot run concurrently as mutually exclusive resources;
only genuinely isolated shards may run at the same time.

Organise prepare -> execute -> acceptance by prerequisite topology, jointly constrained by the host limits given by project configuration:
executors, concurrency quota, machine CPU/memory and number of environments.
An idle concurrency quota does not mean the same environment can be rebuilt concurrently; a compiler CPU limit likewise cannot, without basis, force all read-only checks to run serially.

The main task maintains the single execution list and the aggregation; executors write only their own shard's artefacts.
Delegate only when authorisation allows and there is an independent output; the input states candidate identity, case set, ownership, exit/interrupt method and result location.
Test independence is no reason to widen external service authorisation.

## Aggregation verifies the complete set

Compare against the planned case set first, rather than counting how many "success" messages arrived.
Each result binds the candidate, case ID, attempt identity, prerequisites, complete final state and evidence; duplicate receipts are deduplicated, different attempts keep their history.
Missing shards, unknown IDs and overlapping writes are verified first; a total pass count does not offset omissions.

- Execution of this scope may be declared complete only when every expected item has a valid result; a failed item stays failed, and the other passes remain valid item by item.
- For status meanings see `verification-gate`; skips are judged per item by its rules and do not count as N/A automatically.
- A case process that exits 0 without the expected result is handled as an evidence gap and cannot be PASSED automatically.
- Rerun passes after a first failure: record both runs and the differing conditions; unexplained, mark it flaky; do not delete the first run or pick only the best run.

## Interruption recovery

First verify still-running processes/remote handles and artefacts already written, and keep unknown occupancy; reallocate the same resource only after the stop is confirmed.
Separate completed valid shards, unfinished shards and possibly contaminated shards.
Valid shards whose candidate is unchanged and conditions still apply need no mechanical rerun, and missing shards continue;
an environment or data rebuild may invalidate part of the evidence, so re-verify the impact.

Example: of three shards, A is complete, B was interrupted mid-execution and C has not started.
A's result is kept if it has complete identity and is data-isolated from B;
for B, check in-flight work and partial writes first, clean up only within its own ownership, and rerun the affected cases after recovery; C can proceed independently once its prerequisites are met.
One overall runner finishing does not mean all three shards completed.

If acceptance changes during a full suite, first lock the new requirement and candidate and compute the items to add/retest;
when impact cannot be bounded, widen verification, and do not move the old overall green straight onto the new candidate.
The aggregate conclusion is determined by what the evidence means; the test strategy does not replace release permission.
