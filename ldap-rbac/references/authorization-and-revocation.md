# Authorisation decisions and revocation

## Keep the actual contract

Fill in the matrix item by item with principal, resource type, action, scope, field permissions and approval conditions; missing rows default to deny.
Scope may be a global category or project/resource ownership; require the corresponding ownership only if the project already uses resource isolation; do not add tenant/owner automatically.

The role names below are placeholders; replace them per the project contract:

- If the project contract states `{{global_write_role}}` may write across resource ownership, tests must keep that allowance.
- If the contract defines `{{approval_role}}`, verify approval as an independent condition; do not skip it because of write permission or an administrator role.
- If a valid ungrouped user is assigned `{{read_only_guest_role}}` per contract, authentication succeeds and restricted endpoints reject; do not equate no group with a wrong password.
- Compute permissions across multiple groups per the approved rule; administrators have only explicitly granted capabilities.

Every API call decides permissions on the trusted server-side identity; never elevate identity from a role/username in the body.
Path parameters and resource ownership/existence are verified per project semantics so the client cannot swap IDs at will; bulk lists, exports, downloads and background jobs all use the same decision semantics.
Sensitive fields are trimmed at the authoritative egress and writable fields are restricted; hidden UI buttons and frontend masking are display only; errors/logs/caches must not leak separately.
Write actions on cookie sessions also need the existing CSRF protection; RBAC does not replace it.

## Revocation sequence

1. Write the revocation contract first: directory change discovery delay, permission publish time, maximum cache/session delay, and handling of already started actions. "Immediate invalidation" can only map to a provable boundary; a TTL does not replace the commitment.
2. Disabling a user, removing a group or changing the mapping all update the authoritative user/policy version; publish the invalidation notice in the same transaction or via a reliable event.
   Each API checks the version/disabled state, old caches are invalidated, and old sessions/refresh tokens are revoked per contract. If the contract says removing all groups converts to the read-only guest role, old write permissions must not remain either.
3. A JWT relying only on signature and expiry cannot be revoked immediately: per contract add request-time checks such as an authoritative version/denylist, or honestly declare that old permissions remain valid within the lifetime and obtain the corresponding design decision. Revoking only the refresh token does not erase existing access tokens.
4. When permission changes race with requests, define the effective point; critical writes re-check current permissions before commit/execution, and queued jobs carry the principal and re-check at execution, never permanently reusing administrator permissions from enqueue time.
   In-flight work needing cancellation/compensation is handled per business contract; do not claim abort means rollback.
5. Lost invalidation notices are compensated by authoritative version checks or a controlled short deadline; when cache errors occur or the permission version is unreadable, deny restricted operations by default and do not reuse old roles without a time limit.
   If a bounded failure grace period is approved, list the maximum duration, action scope and risks; the skill does not enable it automatically.

Keep failure to obtain complete authorisation information separate from "complete result with no group"; do not downgrade an error to the guest role and then claim the sync succeeded.
After recovery, verify and publish the complete new version; old epochs and old sessions must not revive permissions. The directory itself does not revoke application sessions on its own.

## Required assertions

- User with valid credentials but disabled: no usable new session; the existing session is rejected per the deadline.
- After login, removing the write group or changing the mapping: old cookie/JWT, another node's cache, export endpoints and queued write jobs are all invalidated at the effective point.
- Multiple groups, no group and project-defined global categories: follow the project category rules; approval permission is independent; an over-privileged API call is still rejected even when bypassing the UI.
- Directory/cache disconnect and missing pages: permissions must not widen and no false complete snapshot is published; record the permission staleness window.
- Unauthorised reads of sensitive fields or bulk updates of unauthorised fields: rejected/trimmed at the authoritative egress; responses, errors and logs contain no plaintext.

Results record policy version, synthetic principal, action, scope, revocation timeline, expected/actual, allowed window and evidence location. If real directory policy and multi-node invalidation were not run, mark them unverified; a static matrix cannot sign off on their behalf.
