# Delivery, business idempotency and out-of-order events

## Separate three identities

The delivery ID dedups retries of the same message; an event chain ID may correlate several events; the business operation prevents duplicate side effects. The current GitLab [Delivery headers](https://docs.gitlab.com/user/project/integrations/webhooks/#delivery-headers) state that `webhook-id` and `Idempotency-Key` stay the same across retries, the latter already existing in older versions; `X-Gitlab-Event-UUID` can be shared across recursive events and cannot be used directly as a unique ID for every delivery. When the actual version lacks a header, choose per its contract and record the scope of the guarantee.

Bind the dedup key to the trusted instance/receiving route or hook configuration, the message ID and the necessary business scope, avoiding collisions across instances. Store a body fingerprint to detect same-ID-different-content conflicts; the fingerprint does not replace authentication. The same message may be delivered through both project and group hooks, so the business layer must also dedup by business operation identity; a per-hook inbox alone cannot guarantee single execution.

## Persist receipt before responding

Authentication/schema/permission entry checks pass -> atomically insert into the inbox (unique key + fingerprint + state) -> persist the processing intent -> return an accepted response -> process asynchronously. A 2xx should correspond to reliable local receipt; replying success before the queue is persisted loses events. Without durable storage, do not promise reliable async processing.

Repeat with same ID and same content: if completed, reuse the processing result; if pending, return accepted and continue the original processing without creating a new operation. Same ID with different content: reject and keep a non-secret diagnostic. Worker claiming needs an atomic state transition; an owner losing contact or a lease expiring does not prove the old executor has stopped, so the side-effect side still needs an idempotency identity or reconciliation.

Before triggering a build, save the operation, job and snapshot. A request timeout enters unknown; first query the matching queue/build and never trigger again. When marking the inbox processed and the external side effect cannot share a transaction, cover the window with an outbox/downstream idempotency or a queryable operation; without this capability, state explicitly that exactly-once cannot be guaranteed.

Retries target transport/temporary dependency failures; validation or permission rejections are not retried indefinitely. Set backoff, a limit and an actionable final state. Whether expired records can be cleaned up is decided by the replay window/business dedup retention; do not delete records and let old events execute again.

## Out-of-order delivery and permissions

The time different events are received is not the order they happened. If a trusted version/sequence exists, check monotonicity. A commit SHA only identifies content and is not naturally orderable; do not judge old vs. new by string comparison. Without a sequence, converge through allowed state transitions and authoritative queries; do not query state from an arbitrary Git remote and cross the local boundary.

A final state is not revived by a late running event; an old branch event must not overwrite a later confirmed state. Keep cancellation intent, the old operation and the new operation separate; late callbacks must have their identity verified. When execution is long delayed, re-verify current permissions/disabled state per the business contract; having passed receipt authentication once is not permanent authorisation.

Test matrix: resending the same delivery, two workers racing, same ID with a different body, project/group duplicates, crash after persisted receipt, side effect succeeded but response lost, stale state arriving late, recursive events sharing a UUID, permission revocation, dedup expiry. Without an explicit sequence, output "pending reconciliation"; do not fabricate an ordered success verdict.

Interruption recovery checks inbox/outbox/operation state and the real final state of processes, keeping the candidate and the version used; do not clear the dedup table or replay all events. Real GitLab redelivery/recursive triggers still need verification in a real environment authorised by the consuming project; synthetic scenarios cover only the local receiving contract.
