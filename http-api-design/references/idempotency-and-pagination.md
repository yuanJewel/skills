# Idempotency keys and pagination

Sources and license: see the [SKILL.md Sources section](../SKILL.md#sources).

## An idempotency key is not a retry switch

First decide whether the business effect can happen twice, whether the final state can be queried, and whether an idempotency key is needed. A pure overwrite update may rely on version and resource identity alone; create/charge/trigger-job operations need an explicit logical operation identifier. Anonymous requests without a stable calling principal need a project-defined usable scope; do not quietly use an unreliable IP as identity.

An idempotency record contains at least: principal/tenant or resource permission domain, operation and version, key, request fingerprint, state, result/resource or operation ID, creation time/retention period. The key is reused by the caller when retrying the same logical request; it must not be newly generated on each retry.

The fingerprint covers the normalised inputs that change side effects: route resource, business body, key query parameters/version, etc. Exclude irrelevant variation such as trace and transport time. Normalisation of JSON key order/omission and defaults needs explicit rules and must not merge semantically different requests. The fingerprint does not store raw secrets, and logs do not record sensitive full requests. Identity binding comes from the authenticated principal; do not trust only the tenant in the body.

| Current record | Incoming request | Result |
| --- | --- | --- |
| Absent | Valid input, authorised | Atomically create pending and acquire execution eligibility |
| pending | Same fingerprint | Return the established in-progress/query identifier or wait boundedly; do not execute again |
| succeeded | Same fingerprint, still authorised now | Return the original result or the same operation identifier; state explicitly which response fields are kept |
| Present | Same key, different fingerprint | Conflict error; do not overwrite the record or silently execute anew |
| uncertain | Same fingerprint | Query the authoritative side effect/reconcile; never delete the key first and then retry |
| expired | Any | Handle per the expiry contract; do not by default allow a dangerous side effect to happen again |

Failures also need classification. Does a validation/authorisation failure create a record? Can a temporary failure that definitely produced no side effect be retried? Is a definite business rejection saved as a final state? Each needs a contract. Do not cache every 500 as a permanent failure, and do not treat every failure as not executed.

## Atomic races and crashes

A key within one scope needs a unique constraint or an equivalent atomic conditional write; the race loser reads the existing record. When the side effect and the idempotency state live in the same database, establish consistency in a feasible transaction and promise success only after commit. Do not do `exists` -> execute -> `set`; concurrency causes double execution.

When the side effect is in an external system, a local transaction cannot cover the remote side automatically. Prefer passing an idempotency key/operation identity the downstream supports, persist the initiation intent, and query or reconcile after timeout. When the downstream is neither idempotent nor queryable, state that exactly-once cannot be guaranteed and offer manual recovery/a product choice; do not claim a Redis lock solved the crash window.

A pending lease timeout only means the owner may have lost contact, not that the old worker has stopped. Reclaiming needs version/fencing or an authoritative-side check that prevents the old owner from continuing to commit; without it, keep the result unknown and reconcile. Duplicate notifications, late callbacks and convergence after restart are also part of the contract.

Choose TTL by the maximum retry window, the consequence of a business duplicate, and privacy retention. An in-progress record cannot simply be released on expiry. A final result may expire, but non-repeatable actions also need a business unique constraint/dedup tombstone or rejection of overly old requests. The client also needs to know whether the same key is allowed after expiry, and after how long it can no longer retry safely.

Before every return of a cached result, re-confirm identity and permissions; after permission revocation, do not leak the old response just because the key hit. The same key from a new principal is isolated. Secret fields in the result store, encryption/masking and retention follow project policy; do not cache whole HTTP responses indiscriminately for long periods.

## A complete synthetic choice

Example: an authenticated user requests an export at `/exports`, the body is a fixed filter, and the key scope is user + API version + create-export. The first valid request atomically writes pending and returns 202/operation_id. Concurrent requests with the same key and same body return the same operation_id; with a different body they return 409. After completion the same key still returns the same operation. The generated file is fetched separately by effective permission; replaying the operation identifier does not bypass download authorisation.

When the job loses contact, first query the export record; reclaim only after confirming it has not executed and the old owner can no longer write. If the product keeps results for only 24 hours, it must also define rejection of requests after 24 hours or a business dedup window. "Regenerate after 24 hours" is side-effect semantics that needs explicit acceptance, not an automatic HTTP guarantee.

## Stable boundaries for pagination

Small data sets that need page jumping may keep offset; large traversals may choose keyset/cursor. Offset can miss/duplicate under concurrent inserts and deletes, and a cursor does not automatically provide snapshot consistency. First decide whether the contract is "best-effort browsing of current data" or "exactly-once over the full set at a point in time"; the latter needs mechanisms such as a snapshot/version upper bound.

Ordering must be total, e.g. `created_at DESC, id DESC`, with a unique id and preferably immutable boundary fields. The next-page predicate follows the same order: `created_at < last_time OR (created_at = last_time AND id < last_id)`, to avoid missing items with identical timestamps when ordering by time alone. When needed, fetch limit+1 to determine has_more, and make the meaning of an empty cursor on the last page explicit.

The cursor binds ordering, filters, resource scope, version/snapshot and the last key. Prevent tampering by signing/authentication or server-side storage; Base64 is not a trusted proof. Re-check permissions on every page; user fields must not pose as an internal cursor. Cursor expiry, changed filters and reuse across principals are rejected or restarted per the contract; never silently query a new scope with an old position.

Even with a unique key, changes to the sort field can still cross the boundary. Describe visibility separately for inserts on the read/unread side, deletions, permission changes and archive migration. When the online + archive full set is needed, both sides use the same ordering and dedup identity, and keep read-failure/incomplete markers; do not hide missing pages behind a 200. Whether total is exact/estimated/omitted is decided by the contract; do not assume totals stay consistent across pages.

Verification matrix: identical sort values across pages, empty first/last pages, limit extremes, changed filters, tampered/expired cursors, cross-principal use, concurrent inserts/deletes/updates, permission revocation. The idempotency matrix additionally covers concurrent same key with same content, conflict with different content, response lost after execution, crash before/after commit and the TTL boundary.
