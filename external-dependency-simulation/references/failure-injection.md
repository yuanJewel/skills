# Failure matrix and recovery

Choose scenarios by what the caller actually promises; exhaustive coverage is not required every time. For each item write the injection point, server-side state before and after, client observation, retry/stop condition, assertion and cleanup. Merely making a fake raise TimeoutError does not prove a socket deadline or connection close.

| Failure | Effective injection | Key assertions |
| --- | --- | --- |
| Rejection/authentication failure | Synthetic forbidden, expired or missing-field contract | Permanent rejections not retried, details not leaked, no real identity used |
| 429/temporary 5xx | With/without Retry-After, in the time formats the version supports | A single layer owns retries, overall deadline, count limit and backoff, replayable with virtual time |
| Failure before connecting | Controlled local non-listening endpoint/transport error | No known write; bounded failure does not discover production addresses automatically |
| Disconnect after request accepted | Server records the effect, then drops the response | Enter uncertain result/query state or idempotent recovery; no blind duplicate creation |
| Timeout/slow stream | Delayed headers, chunked body or frozen virtual task | Distinguish connect/read/overall timeout; no ongoing work from this task after cancel |
| Malformed/oversized response | Raw bytes, wrong types, truncated body, over-limit pagination | Explicit parse/budget error; no successful empty set output; bounded reads |
| Eventual consistency | State visible after a fixed clock point, invisible to early reads | Bounded polling, immediate exit on a final-state error, clear failure when still not ready after expiry |
| Out-of-order pagination/events | Repeated cursor, duplicates across pages, redelivery and reversed order | No loops, no duplicate side effects, old state does not overwrite new state |
| Scenario interruption | Keep in-flight IDs, server-side effects and local state | Recovery verifies state first; while the old execution is unclear, do not create the same side effect anew |

For messaging systems also distinguish delivery, consumption, ack and business commit; the redelivery paths differ for disconnects before and after ack. Using a fake to prove handler idempotency does not mean real broker durability and reconnection pass; when that layer is needed, use the corresponding local service with synthetic data.

## Completion criteria

Verify together the final return, request count, server-side effects, the final state after cancellation and remaining state. Two concurrent nodes with the same business ID must not cross state; while one node resets, continuous reads on the other should be unaffected. Random-failure tests record the seed and scheduling order; inconsistent replays are marked uncertain, and running more times until green is not enough.

Output a difference table: unsimulated TLS/permission policies/timing/quotas/real delivery behaviour and their impact, and which layer of evidence is needed to close each. Real post-launch confirmation items retained by the project (listed in the project contract) are not closed by local simulation; local simulation only provides preparation evidence and cannot remove these items from the checklist.
