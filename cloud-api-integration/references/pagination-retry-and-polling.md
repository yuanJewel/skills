# Pagination, retries and async polling

## Complete pagination

First verify whether the API uses page/size, offset, an opaque pagination token or nextLink; do not mix them. A token is an opaque value, passed through exactly; completion follows only that API's contract (e.g. token absent), not "this page is empty" or "fewer than pageSize". An empty page that still has a token continues; an empty result from a fully successful listing can be an empty snapshot.

Record the tokens/pages requested, IDs returned, page count/element count and the overall deadline. Repeated tokens, nextLink loops, conflicting duplicate IDs, no progress and budget exhaustion all return incomplete; publishing a complete snapshot is forbidden. When the API allows overlapping pages, dedup by a deterministic rule and record it; content conflicts on the same ID need a version/consistency policy, never silently keep the last item.

Real data changes between pages can mean the list is not a snapshot; verify the provider's consistency contract/version stamps. When a token expires or reading cannot continue, re-read that scope; keep the original incomplete result, and do not stitch fragments of two snapshots into a complete one.

## Retry decisions

| Result | Behaviour |
| --- | --- |
| 401/403/invalid signature/parameter error | Report the corresponding category directly; do not automatically switch credentials or retry until success |
| 429/explicit temporary rate limit | Wait boundedly per Retry-After and the total budget; beyond the remaining budget it is blocked/timed out |
| Connection failure/timeout/retryable 5xx | Reads back off per contract; writes may already have executed, so reconcile via operation/idempotency key first |
| Business failure/async Failed/Canceled | Final-state failure/cancellation; do not wrap as a transport retry |
| Caller cancellation | Stop further calls; keep whether the remote side executed as unknown |

Parse Retry-After per that API's format; generic HTTP may use seconds or an HTTP date, so handle dates and skew with an injected clock. Invalid/negative values use a bounded policy or are reported as a protocol error; no busy looping. Backoff with jitter, a maximum count and an overall deadline; do not exceed the user's deadline to honour a service-suggested wait. Every write retry must prove an idempotency key/identical request digest and retention window; a PUT method name does not automatically remove business side effects.

## Async operations

An accepted response is not completion. Save the initial operation ID/status URL and the request identity, choose the status endpoint/field per the specific API, and make pending/succeeded/failed/canceled/unknown explicit. Unknown enum values keep the raw value and are not treated as success; a timeout means "no final state seen", and must not be recorded as remote failure or success.

ARM summary: track via the Azure-AsyncOperation header actually returned, or Location when it is absent, and honour Retry-After; the status response and the resource provisioningState are not interchangeable fields. The meaning and final states of 201/202/200/204 for a specific API must be checked in the versioned documentation, not guessed from the HTTP code alone; polling may also require permissions different from the resource write. This rule cannot be generalised to all Azure services.

After a lost polling response, cancellation or restart, first recover the operation identity and then query; do not resend the create request to "find the result". When completion requires a resource query/business acceptance, close with the corresponding evidence. An expired operation URL must not be replaced with an arbitrary new task standing in for the original.
