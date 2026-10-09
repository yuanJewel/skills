# HTTP contract checklist

Sources and license: see the [SKILL.md Sources section](../SKILL.md#sources).

## From input to resource boundary

For each endpoint write method/path, caller, resource identifier, business action, sync/async and allowed states. GET/HEAD safe semantics should avoid business write side effects; the intended repeat effect of PUT/DELETE must match the contract. Whether PATCH is idempotent depends on the patch semantics; an increment-by-one usually cannot be replayed freely. For an existing non-standard endpoint, first explain the current contract and the compatibility cost; do not treat naming preference as a defect of this round.

Separate parameters into path/query/header/body; write type, required, default, the difference between null and omitted, length/collection limits, allowed enums, numeric ranges, time format and time zone. Strict big integers or money must not be distorted by passing through floating point. Make explicit how repeated query keys, unknown fields, multiple JSON values and Content-Type are handled. Whether to tolerate or reject is decided by the existing consumer contract; do not change strictness on your own.

For complex objects use a separate allowlist of request fields so user input cannot overwrite internal permission, state, tenant or audit fields. Batch requests also need explicit ordering, maximum item count, atomic or per-item results, and how to retry after partial failure.

## Authentication, authorisation and fields

Per the project model, first authenticate, then authorise by operation and resource scope; pass the original caller along a trusted internal chain. External request headers must not impersonate internal identity directly. Anonymous entries need explicit allowed actions and limits; a successful login does not mean permission to read a given object.

Verify separately list filtering, single-item reads, writable fields and expanded related fields. `fields/include` only narrows the allowed set and must not open secret fields. After permissions change, every request and every cache hit re-verifies the required permissions; cache keys isolate principal/scope. Never share an administrator's response with ordinary callers.

Whether a resource exists may itself be protected. Choose 403 or an existence-hiding 404 per project convention, and make sure it cannot be easily bypassed through different error bodies or latency. The authoritative egress at the bottom controls sensitive content; upper layers handle it as an authorised response. Do not pass plaintext to an unauthorised layer and trim it there.

## Success and failure

| Situation | Common response semantics | Contract to add |
| --- | --- | --- |
| Synchronous success | 200; creation commonly 201 with Location; 204 when no body | Returned fields, resource identity and completion condition |
| Asynchronous acceptance | 202 | Operation identifier/query entry; acceptance is not business completion |
| Invalid format or semantics | 400 or established 422 | Stable error code, field details; do not echo secrets |
| Unauthenticated/forbidden | 401/403 or 404 for protected objects | Challenge/identity and the boundary of what may leak |
| Not found | 404; 410 when permanent removal is confirmed | Distinguish soft-deleted/invisible/expired |
| State conflict | 409; failed conditional request commonly 412 | Version, recovery action; no blind retry |
| Over quota/temporarily unavailable | 429/503 with applicable Retry-After | Limit dimension, wait and retry eligibility |
| Internal/upstream failure | 500/502 etc. per gateway semantics | Disclosable information, trace, whether the result is unknown |

This is a selection framework; it does not require rewriting currently valid status codes. Error codes are stable and programmable; messages are for humans. SQL, stack traces, connection strings and internal auth details must not be exposed directly. A gateway should not collapse all downstream errors into 500, nor pass through untrusted internal messages. Data, headers and metadata such as archive/partial-result markers are passed per the contract; do not keep only the main list and lose the incompleteness marker.

## Timeouts, caching and concurrent updates

The caller's deadline runs through downstream calls; internal budgets may only tighten it. Make explicit whether a write may still complete after a client timeout. Retries at different gateway layers must share a total count/time budget to avoid layer-by-layer multiplication. When the transport fails and the result is unknown, check operation status/idempotency result first.

Choose Cache-Control and Vary for read caching by data sensitivity; never share data that carries identity. Where caching is involved, verify permission revocation and invalidation of stale content; do not require adding caching to every endpoint.

If concurrent modification must prevent lost updates, write the version field/ETag and conditional request contract: read version -> submit with matching condition -> atomically check and update. Do not check first and then write unconditionally. A version conflict returns recoverable information; the client must re-fetch state/re-decide and must not automatically overwrite others' changes.

## Compatibility and verification

Check whether field addition/removal/type, empty values, omission, error codes, ordering, time, auth and rate limiting affect old consumers. A new field can also break strict-parsing/signing clients; an optional field can also change default behaviour. Use the known consumer matrix to verify the compatibility window and the evidence for retiring the old version; do not force a fixed number of versions or duration.

For each endpoint give success and at least one opposite input, listing request, response status, key fields and side effects. The implementation also needs local contract tests/consumer tests; proofreading the document does not replace actually running them. List suggested extensions (new version path, unified envelope, new pagination style) separately from authorised mandatory work.
