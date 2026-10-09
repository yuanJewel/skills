# cache-aside and consistency

## First define whether errors may fall back to the source

Ordinary losable cache: read hit with valid encoding -> return; miss -> read the authoritative source; source read succeeds -> populate with the positive-value/not-found TTL; on cache failure, degrade to the source within bounds and record the failure category.
Keep source rejection, cancellation and timeout as they are; do not convert them to "not found". A cache write failure does not override a successful source read, but must be observable and must protect source fallback capacity.

When the cache is the authority for permissions/sessions/quotas or idempotency, loss does not mean allow; explicitly reject, re-authenticate or consult another authoritative path.
When authorisation changes, invalidate all related local and remote caches; deleting one UI cache is not proof that revocation took effect.

## Concurrent updates are not solved by one delete

Invalidating after the source write commits is a common starting point, but a stale read can repopulate the old value after the delete: R reads old source -> W commits new value and deletes cache -> R populates old value.
If bounded staleness is allowed, state the TTL and scope; if not, choose versioned keys/version fences, per-entity serialised coordination or authoritative-source version comparison, and prove the ordering of update and populate.
A simple "delayed double delete" only lowers the probability; it is not a proof of strict consistency.

Populating the cache with a source version does not automatically prevent stale writes from overwriting; the comparison must run atomically at the authoritative boundary, and deleting the old value must not lose the version fence needed to reject old versions.
Without a single transaction across DB and Redis, state the window explicitly and use retry/compensation/outbox or the authoritative read path. Do not promise that updating the cache before writing the DB avoids all races.

## Coalesce concurrent misses

Coalesce on the same complete cache identity, which includes tenant/permission view/encoding version; do not share results across different users. With existing singleflight or an equivalent implementation:

1. After the first miss, enter the per-key in-flight group; the leader re-checks the cache inside the group to reduce source fetches when a previous leader already populated it.
2. The leader uses a load task with a total deadline; each waiter listens to its own cancellation independently. If the task is shared, the first caller cancelling must not arbitrarily cancel other waiters; define whether the task is cancelled when all waiters have left.
3. On completion, publish the same result/error and wake all waiters; remove the in-flight entry on success/failure/cancellation to prevent key leaks. Bound concurrency and queue length across different keys, not just a single hot key.
4. State clearly that coalescing is in-process only; multiple instances may still each hit the source once. When cross-instance protection is needed, first evaluate the lease/failure cost of a distributed lock; do not add a lock by default.

With no existing coalescer and only a low-frequency path, plain cache-aside may stay, but must declare that hot-key concurrency will hit the source multiple times.
When upgrading a hot path, add this algorithm and controllable barrier tests; do not call the basic template cache-stampede protection complete. During wide cache unavailability, also rate-limit/circuit-break the source so each miss does not fall back without bound.

## Recovery and verification

Use a synthetic clock and barriers to control the order of TTL/stale read/new write/populate; verify normal hit, legitimate empty value, confirmed not-found, cache corruption, source failure, parent cancellation, cache write failure and concurrent misses.
Record unknown write results with the actual operation identity; whether a retry is safe is decided by the idempotency contract. Clean up only this round's namespace; do not scan real instances.

Positive example: a test deliberately makes the stale read populate last and verifies the version strategy rejects it.
Counter-example: claiming cache consistency because sequential SET/GET passed; a negative cache storing 403 as an empty record; singleflight where only the leader times out while all waiters hang forever.
