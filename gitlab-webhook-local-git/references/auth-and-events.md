# Authentication modes and events

## Pin the mode first

Inputs must state the instance's actual version, feature flags/configuration, trusted receiving route and authentication mode. Verify against the matching version of [GitLab Webhooks](https://docs.gitlab.com/user/project/integrations/webhooks/). The current rolling documentation says signing was introduced in 19.0 and became generally available in 19.1; do not infer that older instances support it.

- Shared token mode: compare the non-empty token configured for the trusted route in constant time; reject missing, ambiguous duplicate headers or wrong values. `X-Gitlab-Token` is a plaintext header carrying a shared secret, not a body signature; the transport must be protected.
- Signature mode: enable only when the actual version's contract supports it. The current public contract uses `webhook-id`, `webhook-timestamp` and `webhook-signature`; the signed message contains the ID, timestamp and raw body. Verify strictly per the official encoding/algorithm and multi-signature format; the time window and allowed skew are defined by the project.
- Migration mode: if supporting both old and new authentication is authorised, state explicitly which trusted configuration allows which mode. A present but wrong signature header never downgrades to token.
  - A route that enforces signatures also rejects a missing signature; an attacker removing the header must not automatically enter the old mode.
  - This is a deliberate tightening by this package: the migration advice on the GitLab Webhooks page above is to configure both tokens during the transition, with the receiver verifying the signature when present and falling back to the token when absent.
  - If the project needs compatibility during migration, explicitly configure token fallback for that route; the fallback still validates per the shared token mode.
  - A safer cutover can use a separate route/an explicit configuration effective time.

Signature verification happens before body parsing/re-encoding; proxies that compress or transform the body also need a contract. Request size, header length, timestamp format/overflow and duplicate headers need limits and rejection behaviour. A valid signature does not guarantee freshness; reject times too far in the past/future, and idempotency is still needed within the replay window. Do not log secrets, signature verification plaintext or full bodies.

## Minimal event schema

Check the specific event in [Webhook events](https://docs.gitlab.com/user/project/integrations/webhook_events/), not GitLab CI YAML examples. Verify that the header event type matches body object_kind/event_name, project_id matches the nested project.id, the repository mapping is valid, and ref exactly matches the allowlist. Validate IDs and commit SHAs by contract type/length; unknown types produce no side effects.

Push, Tag, Merge Request and Pipeline do not share one schema; this round supports only approved events. The commits list of a Push may be truncated or empty; do not treat it as a complete commit graph, and do not assert no change just because the list is empty. Branch creation/deletion, zero OIDs and null checkout values are handled separately per the contract for that version and action; do not take "the last commit" as the sole target.

After receiving a trusted notification, still verify the caller-to-internal-identity mapping in the event, current permissions and allowed actions; usernames and emails in headers/body do not automatically grant permission. For an allowed event on a disallowed repository/ref, explicitly ignore or reject it and record a non-secret reason. Whether unknown/irrelevant events are ignored with 2xx is decided by the contract; never quietly execute a default branch.

URLs, avatars and repository addresses in the payload are display/verification data only and are not accessed automatically. Sensitive logs by default contain only event type, internal correlation ID and processing category; when troubleshooting needs extra fields, allowlist them one by one and mask them. Never print the whole body of an authentication failure.

Normal example: after verifying the signature, strictly parse a valid Push projection, then choose the local repository by the internal project mapping. Counter example: sorting the JSON and re-signing before signature verification changes the original message and cannot prove the authenticity of the received bytes. Another counter example: accepting any project_id with a valid token.
