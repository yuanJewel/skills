# Parallelism, external integration and results

## Serial contract first, then concurrency

Without xdist, run the same selection through the existing serial entry; do not assume the -n option is available.
A session fixture is its own session in each worker and is not guaranteed to run only once globally.
When a global one-time initialisation is needed, use an existing coordination mechanism with an independent owner; a pytest fixture name does not guarantee mutual exclusion.

External resource names include run, worker, case and attempt to avoid collisions on retry or restart;
without xdist the worker value comes from the serial execution identity, with no hard dependency on the worker_id fixture.
Paths use tmp_path, not a fixed temp.txt; ports are reported by the service after it binds; databases/schemas/cache keys/queues and reports are each isolated.
A namespace must not contain unvalidated input or secrets.

Shared read-only seeds can be reused; permission/configuration/global-state changes, database wipes and service restarts must hold the corresponding resource exclusively.
A fixture's transaction rollback isolates only transactions on the same connection and does not guarantee that writes from other threads/processes/independent connections are rolled back too;
verify DDL and external side effects separately.

## Integration prerequisites and failure injection

Read the allowed local target, candidate, dependency versions and purely synthetic seeds.
A stub interface must cover those of success, rejection, timeout, cancellation, pagination or partial failure that are relevant this time; a passing mock does not prove the real driver/protocol.
Real behaviour of databases/caches and the like is verified only on an authorised local isolated instance; never fall back to connecting to production.

Separate retried reads from retried writes: reads can usually be retried safely;
for a write whose response is unknown, first query by operation identity or rely on the interface's idempotency contract;
a test should not bypass the product's retry policy and swallow errors on its behalf. Test-runner retries must not change independent expectations either.

## Results must include the execution phase

- collection error: the cases were not fully collected; no "0 failures" conclusion can be given.
- setup error: the test body did not run; list the allocated resources and the cleanup result.
- call failed: keep the independent assertion, actual value and synthetic input; keep the original failure after the fix.
- teardown error: the test body may have passed, but resources were not reliably released; list it separately and do not count it as all passed.
- skipped/xfail: does not prove the expected behaviour passes; record the reason, whether it is required and the condition for restoring it.
- xpass: expected to fail yet passed; verify whether the marker is stale and whether it is strict; do not silently keep an expired exemption.
- exit code 5/no tests collected: no test ran; an empty selection is not success.

Verify nodeid/parameters/selection, candidate, versions and each shard's final state; avoid looking only at pytest's overall exit code.
The list of scenarios implemented by markers can be collected, but collection is not execution.
For an unknown plugin, verify the entry capability first; installing coverage/parallel/async plugins automatically to fill in the table is forbidden.

Normal example: a cache namespace per worker, waiting for your own background task to exit after cancellation, and retries that keep the attempt.
Counterexample: every worker's session fixture wiping the same database, or covering the original failure with only the final JUnit report.

## Recovery after interruption

Save the current run/worker handles, the external resource list, and completed and unknown results; on takeover, confirm the final state of the processes and the sole writer before restarting.
Release only resources confirmed to belong to this run; process kills and directory cleanup stay within the original permissions; do not infer "stopped" from loss of contact.
Write cleanup exceptions, retained resources and the next step into the evidence record.
