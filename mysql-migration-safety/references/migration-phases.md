# Phases, re-entry and recovery

## Entry criteria and compatibility table

First compare the real old schema with the target schema and confirm historical migration IDs/content identity, to avoid drift from editing an already applied migration.
Verify both creating a new database from scratch and incrementally upgrading an old one; migrations on startup must also verify that only one executor runs across multiple instances. Lock expiry does not mean the old executor has stopped.

List the read/write matrix of the old/new application against old and new columns, especially background jobs, reports, bulk writes, auditing and callbacks. Checking only current HTTP requests misses old writers.
Before contracting, require evidence that all old consumers/jobs have retired; do not just wait a fixed number of days.

| Phase | Action and entry criteria | Verification | Failure recovery |
| --- | --- | --- | --- |
| Expand | Add compatible schema; algorithm and locks verified | Old application can still read and write; new schema matches the definition | Stop later phases; check the actual schema, do not assume the DDL did not take effect |
| Sync | Old and new paths have a defined authoritative source and dual-write/sync mechanism | New writes are not overwritten by backfilled old values | Keep old reads; check partial dual writes and compensation |
| Backfill | Stable key, batches, re-entry and progress designed | Data integrity, unprocessed items and conflicts | Resume from the committed checkpoint; reconcile unknown batches first |
| Switch reads | Backfill verified and fallback from new reads feasible | Business semantics and old/new results agree | Before reverting to old reads, verify new writes are still compatible |
| Stop old writes | All old consumers retired | No old write sources; observation-window evidence | Forward-fix if needed; do not blindly restore the old binary |
| Contract | Destructive action approved with recovery evidence | New application has no dependency on old fields | Deleted data relies on backup/PITR or manual forward fix; do not pretend a DOWN migration restores it |

Dual writes must define atomicity; do not run two unrelated UPDATEs and ignore one failing. If they cannot share a transaction, a compensation/reconciliation identity is required.
An old application that keeps writing only the old column during backfill leaves the new column stale; complete write sync or arrange an explicit write-freeze window first, then do final consistency verification.

## Batching algorithm

Choose a stable unique key (or stable composite key) and a recordable watermark. First agree on the migration coverage boundary and handling of concurrent inserts: a captured high watermark covers only the range at that moment; writes after it must go through the new path or be backfilled separately.

A reviewable pseudocode:

```text
read migration_id, transform version, committed cursor, fixed high_water
select the next batch with cursor < key <= high_water, in total key order
for selected rows, compute and write conditioned on old value/version; do not overwrite concurrent new values
save this batch's progress in the same transaction (if the tool supports it); advance cursor only after commit
put conflicting rows into a retryable/pending-verification set; do not forget them because the cursor moved
after the scan, verify the pending set and old/new consistency over the full range
```

If progress cannot commit in the same transaction as the data, allow the checkpoint to lag and rely on idempotent replay; never write the checkpoint early and skip rows.
Advancing by "largest key scanned" and judging by "rows actually changed" are different concepts; affected_rows=0 may mean already correct, concurrent conflict or no change, and does not prove completion.

Before using NULL as the "not migrated" marker, confirm whether a legitimate target can also be NULL; otherwise record transform state separately.
If `SKIP LOCKED` is used, skipped rows must not be lost permanently as the watermark advances; a rescan/queue is required. Also define inclusion rules for stable key changes, deletes and soft deletes.

Tune batch size and interval to actual synthetic load; monitor per-batch transaction time, lock waits, errors, remaining space and applicable replication lag. On hitting a threshold, stop issuing new batches and confirm the final state of in-flight work.
After a deadlock, rerun the whole re-entrant transaction; any bounded retry keeps the error and the state after reaching the limit; no infinite retries.

## Startup migrations

The startup chain may follow the project contract "schema meets target -> idempotent seed -> ready". Seeds, keyed by stable business identifiers, create no duplicates when rerun and do not overwrite user-configured values.
A failed migration step must explicitly refuse readiness for that service, keeping the error classification and migration version; how already running compatible old versions keep serving is decided by the release plan.

Do not specify in a general method which service must run migrations; read the project's sole execution responsibility.
When automatic migration meets a drop/narrowing/uncertain constraint change, stop that action per existing permission boundaries; a readable diff report can still be produced.

## Archive and time

When archiving is involved, read the project's integrity and retention contract: export object identities/time range -> persist durably -> verify readability, record the identifier set, counts and necessary content checks -> verify the full set reachable online + archived -> only then move rows out of the online table.
If export fails, items are missing or identities are incomplete, do not move rows out; moving out of online storage is not deleting business data. If export files are immutable, do not rewrite them to patch holes; create a new object with an explicit relationship.

For time changes, first distinguish instants, wall-clock time and calendar ranges; record old/new storage, transport, display and archive-partition semantics.
Verify equivalence with the same instant in multiple offsets, before and after the project's month boundary, a non-default time zone, and cross-month migration; do not add/subtract a fixed number of hours across the whole database as a universal fix. A historical defect-fix note is not evidence that the issue is unfixed today.

## Recovery material

For each step, save before/after schema identity, migration ID, committed watermark, synthetic identifiers of conflicting/failed rows, execution state and the raw error.
Recovery first determines which of three positions the failure was at (before execution / during execution / response lost after commit) and queries the actual state.
A backup existing does not mean recovery is possible; that requires verified restore steps and an acceptable recovery point/time. Forensics involving real data follow project permissions; never reuse real data in a test environment.
