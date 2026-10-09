# Endpoint contract

- Goal, approved scope, existing contract version: {{reference}}
- method/path and caller: {{business action, resource scope, identity source}}
- Success definition: {{sync completion/async acceptance, status and Location/operation_id}}
- Permissions: {{endpoint/object/field; list and expansion; revocation/cache hit}}

| Input location/field | Type/required/default | Bounds and null semantics | Authoritative source |
| --- | --- | --- | --- |
| {{field}} | {{rule}} | {{limit/precision/time zone/unknown or repeated}} | {{user/service/not writable}} |

| Case | HTTP status/business code | Response fields | Side effects and retry |
| --- | --- | --- | --- |
| Success | {{code}} | {{synthetic example}} | {{completion condition}} |
| Validation failure | {{code}} | {{field errors, no secrets echoed}} | {{whether recorded}} |
| Unauthenticated/forbidden | {{code}} | {{existence boundary}} | {{no business side effect}} |
| Not found/conflict | {{code}} | {{recoverable state}} | {{re-decide}} |
| Rate limited/temporary failure/unknown | {{code}} | {{Retry-After/query identity}} | {{whether retryable and budget}} |

## Fill in only when relevant

- Idempotency: {{scope, fingerprint, same key with same/different content, pending/uncertain/final state, atomic eligibility, downstream reconciliation, post-TTL semantics, permission re-check}}
- Pagination: {{total order, boundary predicate, limit, bound cursor, snapshot/live consistency, change gaps, total, last page}}
- Concurrent update/batch: {{version condition/atomicity/partial failure}}
- Timeouts and caching: {{total budget, downstream cancellation, unknown result, cache isolation for sensitive responses}}
- Compatibility: {{consumer matrix, field/error/behaviour impact, exit condition for old/new coexistence}}

## Verification and pending items

{{For each scenario: synthetic request, independent expectation, real run/static analysis, evidence location. Keep existing information, business facts pending verification, author suggestions and mandatory work for this round separate; a complete document does not certify the service as verified.}}
