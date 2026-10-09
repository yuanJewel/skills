# Clients, connections and Cluster

Clients are usually reused for the application lifetime, with a pool or multiplexed connection; the creator is responsible for closing.
Separate connection usage of blocking commands, Pub/Sub and ordinary requests according to client capability; do not let long blocking calls exhaust the ordinary request pool.
Do not create a new client per HTTP request, and do not blindly enlarge the pool to mask leaks.

Set connect, pool-wait, command and total operation deadlines, all bounded by the caller's remaining deadline; retries plus backoff also count against the total budget. Parent cancellation immediately stops waiting and any later source fallback.
Distinguish pool exhaustion, dial failure, read/write timeout and business nil; observing wait/active/timeout counts is enough, and logs never print tokens/values.

Reads may be retried according to idempotency; INCR, list pushes, Lua scripts and the like may already have executed, so a response timeout must not be blindly replayed.
Even a seemingly idempotent SET may extend the TTL or overwrite a concurrent value on retry; judge by the specific contract. Check the client's default retry options first; do not assume no duplicates just because business code has no retry.

A pipeline reduces round trips; it is not a transaction. Check every command's error and result; a dropped connection may leave the whole batch's outcome unknown; do not automatically replay a batch containing non-idempotent writes.
MULTI/EXEC serialises a command sequence but does not provide database-style rollback for runtime errors; one command failing inside the transaction does not mean commands before/after it did not run. WATCH conflicts need bounded retries and re-reads.

Cluster multi-key transactions/Lua scripts require the same hash slot; use a shared, non-empty hash tag to express the entity scope that needs atomic cooperation, and avoid packing all tenant data into one hot slot.
User-controlled identifiers need escaping/encoding so embedded braces cannot break hash tag selection. Cluster supports only DB0; do not use different database numbers for tenant isolation.

MOVED/ASK redirects are handled by a Cluster-aware client against the current topology, with a bounded number of redirects still subject to the deadline; during resharding, same-slot multi-key operations may also be temporarily unavailable, so do not claim same-slot is always executable.
Cross-slot transaction needs require changing the model or using authoritative coordination; do not switch back to a non-Cluster client to force execution.

Queries on large collections need a cardinality/result-size budget first. SCAN-family iteration is not a consistent snapshot and may return duplicates or empty batches; it ends when the cursor returns to zero; COUNT is a hint, not a strict page size.
When a complete snapshot/deletion is needed, first define concurrent-update semantics and an independent record; do not treat scan results as a fixed full set. This skill does not scan or clean up a real keyspace.

Enable client-side caching only when protocol/client version, invalidation notifications, disconnect cleanup, cold start after reconnect and permission propagation are all defined; after a lost Redis response, do not keep stale authorisation indefinitely.

Choose verification by what changed: deadline exit when the pool is full, parent cancellation, pipeline partial errors, unknown command results, cross-slot rejection/redirect and disconnects.
Without a real isolated Redis/Cluster, record only stub and code evidence and keep the actual-version verification gap.
