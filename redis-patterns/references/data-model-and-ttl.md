# Data model, keys and expiry

## Choose by access pattern

| Access | Candidate structure | Boundaries to define |
| --- | --- | --- |
| Whole-object read/replace, counters | String/encoded object | Encoding version, empty value, size, concurrent overwrite; counters use atomic commands, not GET then SET |
| Independent field updates | Hash | Field permissions/concurrency; field-level expiry is not assumed, verify the Redis version first |
| Membership tests/ordered ranking | Set/Sorted Set | Cardinality, pagination and tie ordering for equal scores |
| Ordered queue/event consumption | List/Stream | Acknowledgement, replay, loss/duplication, backlog limit; the structure itself does not guarantee business exactly-once |
| JSON/vector | Module/version with confirmed capability | Use only when the access need matches existing capability; do not install automatically |

Follow existing key conventions; a hierarchy of entity/tenant/encoding version with stable IDs is recommended. Keys carry no secrets, full personal data or unbounded query strings.
Unsanitised user input must not control the namespace or the Cluster hash tag. Do not rewrite a small object that is only read whole because "Hash is better".

## TTL is a data contract

Define TTLs separately for normal values, confirmed not-found, sessions/permissions, locks and idempotency records; for each, state acceptable staleness, who refreshes/deletes, and behaviour after failure.
An empty cache differs from source data not existing; an empty string may also be a legitimate value, so use an explicit found marker. Short negative caching is only for authoritative confirmation of non-existence; do not cache timeouts/rejections as not-found.

Set the value and expiry in one atomic command/script, avoiding SET succeeding while EXPIRE never runs.
A plain SET overwrite usually clears the old TTL; set a new TTL explicitly, or use KEEPTTL when the version supports it and the semantics are right. HSET/INCR modifications do not reset the TTL. Give callers an explicit unit; do not mix seconds and milliseconds.

A client's zero TTL may mean persist forever, and a non-positive EXPIRE/PEXPIRE deletes the key; validate the range before sending the command, and do not use a negative value to "temporarily disable".
TTL checks distinguish a missing key from a key without expiry; do not treat both as 0 seconds remaining. Implementations and tests verify against the actual command return semantics.

Jitter reduces simultaneous expiry: pick a value within the approved interval from an injected random source, keeping the final TTL positive and within the maximum staleness requirement.
A fixed seed is reproducible, but business writes must not share one fixed sequence across all instances. Define whether a cache hit slides the expiry; frequent reads must not keep revoked state alive forever.

Expiry is not a scheduler; "should have expired" does not prove a callback ran on time.
Capacity/eviction policy may remove keys early; authoritative state needs a persistence and recovery design.
Tests cover just before/after the boundary, zero/negative input, TTL on overwrite and decode versions; real Redis semantics must be verified on a real isolated instance.

Counter-examples: INCR followed by a conditional EXPIRE that fails midway, leaving a permanent rate-limit key; caching an empty value for every error; a permission cache relying only on a long TTL with no revocation propagation.
