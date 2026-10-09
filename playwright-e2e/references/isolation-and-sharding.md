# Isolation, sharding and interruption recovery

## Independent resources

A BrowserContext isolates cookies/storage but not backend data.
Each parallel worker needs an independent synthetic identity or backend namespace; each case identifies its data and output by run/shard/worker/test/attempt.
Even with the same clock, identities must be unique; Date.now() alone is not enough.
Share an identity only when the server-side state is known not to change; do not share a mutable session/permission cache.

Sharing a service requires an isolation protocol; cases that break global configuration, wipe the database, restart services or contend for an exclusive lock go into an exclusive group.
A dynamic port is reported by the service after it actually binds; do not probe for a free port and then hold it as a placeholder for a long time assuming no contention.
trace, screenshot, download and report paths are also isolated by execution identity, so that a later write does not overwrite the original failure.

A fixture registers identity and cleanup responsibility as soon as it creates a resource; when setup fails halfway, release the parts that succeeded. Only immutable seeds are suitable for sharing.
A POM encapsulates repeated user operations and locators; do not hide all assertions in "always succeeds" helper functions, and a single small journey does not need a new class for form's sake.

## Sharding must allow verifying the set

First have stable scenario IDs and a browser project matrix, and make the full set before sharding explicit.
The Test runner's `--shard=i/n` is a parameter of the whole invocation and does not go into each project's configuration; verify the configuration against the actually installed version.
When an existing core script lacks this feature, have the existing scheduler assign explicit ID sets; do not introduce a new runner automatically.

Verify each shard's selected IDs/browsers, candidate, environment and start/end/final state; when merging, verify item by item the full set, duplicates, missing shards and the effective attempt.
When a rerun passes after a first-run failure, keep both results; skip/not run/interrupted must not count as passed.
Changing grep/filters/the browser matrix changes the set, so record the reason for each exclusion.

The worker count is determined by browser memory, CPU, the service connection pool, data isolation and the project budget; do not use the number of files or of AI agents as the worker count.
When resources are insufficient, reduce concurrency first; do not drop required assertions or silently omit browsers.

## Cleanup record

Each run records the browser/context it created, the service start handles/ports, data namespaces, mounts/volumes (if applicable) and output directories;
who creates and who releases, the order and re-entrancy are explicit.
A normal finally closes the context/browser, stops this run's services and cleans up this run's synthetic data; evidence retention follows project policy.

After an abnormal exit, the external recoverer first verifies that a handle still points to the same resource;
a reused PID or a directory name alone is no basis for killing a process/deleting a directory.
Query unknown in-flight work first; on cleanup failure keep the resource identity and the follow-up responsibility.
A service originally started by someone else is not stopped automatically, and cleaning a whole environment by a fuzzy prefix is forbidden.

Normal example: two workers share a read-only product seed, each with independent orders/users and reports; after one shard crashes, recovery follows the registered identities.
Counterexample: different contexts use the same backend account to edit the same record, the rerun overwrites the first-run screenshot, and everything is then called passed.
