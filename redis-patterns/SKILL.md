---
name: redis-patterns
description: Design, implement or review Redis data models, TTL, cache consistency, locks, idempotency and client failure handling. Use for caching, sessions, counters, rate limiting and connection problems; pure SQL optimisation or configuration format edits without behaviour change do not trigger it automatically.
metadata:
  version: "0.1.0"
---

# Redis state and caching method

First decide whether Redis is necessary, who is the authoritative source of the data, and what the consequences of lost or expired data are; then choose data structures and commands.
Keep performance caching, authoritative state and mutual-exclusion coordination separate; they cannot share one "allow on Redis error" policy.

## Inputs and missing items

Take the actual Redis/client version, standalone/Sentinel/Cluster topology, access and write patterns, authoritative source, acceptable staleness, existing key conventions, retry/timeout policy, and the permitted synthetic environment and stubs.
Missing branches:

- Consistency requirement missing -> list read/write/failure outcomes first; do not set a TTL on your own.
- Actual version missing -> avoid newer commands.
- No isolated instance -> verify code/model only; do not claim Redis atomicity or failover is verified.

## Routing and steps

1. List entities, access scope, keys, value encoding, capacity, and who owns TTL/invalidation; choose structures and expiry behaviour per [Model and TTL](references/data-model-and-ttl.md).
2. For cache reads and update propagation, choose cache-aside, null values, miss coalescing and concurrent-update strategy per [Cache consistency](references/cache-consistency.md). Permission/session revocation does not automatically adopt ordinary cache degradation.
3. For mutual exclusion, rate limiting and idempotency, define unique tokens, compare-and-release, lease/renewal/lost contact, unknown write results and fencing boundaries per [Locks and idempotency](references/locking-and-idempotency.md).
4. Per [Clients and Cluster](references/clients-and-cluster.md), verify connection pools, deadlines, pipeline partial failure, retries and same-slot conditions. User cancellation must not be prolonged by background retries.
5. When a Go example is needed, use the [cache-aside template](assets/go-cache-aside.md); check its explicit limitations before adapting. Do not create instances, install clients or clean up real keys along the way.
   Non-Go projects implement the same semantics per the template's "usage and results table" (hit, legitimate empty value, negative cache, expiry, corruption, source error, cancellation, write failure, concurrency).
6. In a synthetic environment, use a controllable clock/random source to verify the expiry, concurrent misses, stale holder, failure and cancellation changed this time. Results state whether a real Redis/client or a stub model was used, and keep failure and unverified boundaries.

## Failure and resources

Classify failures first: cache miss, decode corruption, connection/pool timeout, business not-found, rejection and call cancellation.
When the cache is optional, degrade to bounded source reads; when Redis is the authority for permissions or idempotency, reject/block per contract; failure never means success. A write timeout is an unknown result, not "not executed".

On interruption, save the candidate, key contract version, test namespace, client/instance owner and in-flight work; verify identities before resuming, and clean up only this round's synthetic resources.

Mechanical checks may use low/low; consistency, locks/cancellation and Cluster failures use normal/high. Grade words map to actual execution configuration through the project resource mapping.
Concurrency is set by the executors, concurrency quota and host limits such as connections/instances given in project configuration; do not mask hot keys with more concurrency.

Positive example: when an ordinary display cache fails, rate-limit fallback to the source and record the degradation; when permission revocation cannot read the authority, reject.
Counter-example: letting an old task write the final result after its lock expired, or scanning the whole keyspace to delete a prefix as routine test cleanup.

**Closing cleanup**: synthetic keys in the test namespace, temporary instances or containers, and connection processes are cleaned up after verification ends. Follow the local resource cleanup rules of `task-implementation`: register identities at creation, at closing clean up only the objects registered this time, write evidence to keep and cleanup failures into the receipt, and use no global cleanup commands.

## Sources

1. Pinned sources: [RD01 redis-core](https://github.com/redis/agent-skills/blob/a84871d065f398fed55e1633f66b66f731eb4e2b/skills/redis-core/SKILL.md), [RD02 redis-connections](https://github.com/redis/agent-skills/blob/a84871d065f398fed55e1633f66b66f731eb4e2b/skills/redis-connections/SKILL.md) (only the pinned entry files were read, not the attached pages).
   Semantic check: [official locks](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/), [EXPIRE](https://redis.io/docs/latest/commands/expire/), [Cluster specification](https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/), latest pages read on 2026-10-09; command capabilities must be verified against the target version.
2. Adopted choosing structures by access pattern, keyspace, pools/batching/failure paths; cache consistency, token/lease/fencing and the Go template are own-authored for this package.
   Dropped fixed clients, fixed TTLs, modules and client-side caching enabled by default.
3. License: shipped with the package as [LICENSE-RD.txt](LICENSE-RD.txt) (RD, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license file along when copying this package alone.
