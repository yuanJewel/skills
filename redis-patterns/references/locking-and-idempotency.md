# Locks, leases, rate limiting and idempotency

## Minimal mutual-exclusion contract

Define the protected resource, holder, lease, maximum operation time, renewal, behaviour on losing the lock, and the actual writer.
A single Redis instance can use the atomic SET key unique-token NX PX lease-ms; the token comes from a reliable random source and differs on every acquisition; do not use a fixed process ID.
An acquisition timeout is unknown; do not immediately treat it as not holding the lock and then write the resource with the same action.

Release must atomically compare the token and then delete. Logic compatible with common older versions can use a Lua script: compare GET with the held token and DEL only on match; never GET then DEL from the client.
Redis 8.4 introduced DELEX IFEQ, but do not use it unless the target version is verified. The following is a logical algorithm, not to be run on a real instance:

```text
release(key, own_token): atomically
    if GET(key) == own_token: DEL(key); return released
    else: return not_owner
renew(key, own_token, lease): atomically
    if GET(key) == own_token: PEXPIRE(key, lease); return renewed
    else: return lost
```

After a renewal failure or unknown response, do not assume the lock is still held.
The lease deducts acquisition/network time and keeps a margin; long pauses, clock changes and process death all change the guarantee; a live process does not mean a valid lease.
Waiting for a lock needs a bounded total deadline, backoff/jitter and cancellation exit; do not renew indefinitely to hog the resource.
When release returns not_owner, do not delete someone else's lock, and do not rewrite a fact of business success into "not executed".

## Fencing and failover

Old holder A's lease expires and B acquires a new lock; after A recovers it may still write to an external DB/service. A random token prevents wrong release but does not stop the stale A from writing.
Strongly consistent paths need a monotonic fencing token that the resource receiver atomically uses to reject older tokens, and must verify that token allocation does not go backwards under failover; Redis INCR with asynchronous replication alone cannot guarantee this.
Without receiver cooperation, choose stronger coordination/DB conditional updates or explicitly downgrade the guarantee; do not advertise full mutual exclusion.

Redis replication is asynchronous; a lock not yet replicated before primary failure can be lost, and another holder acquires it after replica promotion. Ordinary Sentinel/Cluster failover does not remove this window.
The official Redlock discussion also requires considering fencing/clocks and pauses; this skill does not treat node count as a proof of correctness and does not deploy a distributed lock algorithm by default.

## Rate limiting and idempotency are different problems

Rate-limit counting and window expiry must be atomic; define fixed/sliding window, boundary bursts, rejection code, clock source and policy when Redis is unavailable; never INCR successfully, fail EXPIRE and block forever.
Retry counts increment repeatedly; whether retries should count is decided by the business contract.

An idempotency record contains at least caller/resource scope, operation key, normalised request digest, in-progress/completed/failed state, result identity and retention period.
Reject the same key with a different request digest; concurrent duplicates look up the same result or are explicitly told it is in progress; reconcile unknown execution results first.
A single expiring SET NX key is not exactly-once: the key may expire and the operation repeat, and a crash may have written business data without the result. An authoritative transaction/unique constraint or a reconcilable business identity must cover the window.

Synthetic counter-examples: after A expires and B acquires, A's release must not delete B's lock; A writing with a stale fence is rejected by the resource; no further writes after renewal failure; a lost acquisition response must not blindly retry side effects; repeated requests after the idempotency record expires are handled per contract.
A stub model can only verify the algorithm; it does not prove actual Lua script atomicity, primary/replica switchover or clock assumptions.
