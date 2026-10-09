# Identity and group sync

## Identity does not move with the display name

The project designates an immutable, unique directory identity key, namespaced by directory source; entryUUID, objectGUID and similar are adopted only where the real schema guarantees them.
Login names, email and DNs are mutable and are not permanent primary keys across syncs. A renamed user keeps the original internal identity; a newly created user with the same name but a different stable key is a new principal and cannot inherit the old permissions.
When the key is missing/duplicated or conflicts across directories, quarantine the record and block authorisation changes depending on it; do not merge by guessing.

Fix case/normalisation rules and historical compatibility first; do not arbitrarily lower-case a whole DN or strip characters. Take returned attributes only from an allowlist.
Directory ACLs may hide entries/attributes, and insufficient service account permission is also an incomplete read; do not claim the user was deleted.

## Obtain complete group membership

1. Define the group membership model: group contains member DNs, user memberOf, POSIX memberUid or a directory-specific matching rule; do not assume these are interchangeable. Identify direct/nested group support and use the real schema's identity comparison.
2. Define this sync's scope, paging protocol, page size/total entries/time limits; track the cookie/token, duplicate pages and server result code.
   Finish only when the last page and all required attributes are present; sizeLimit/timeLimit, a repeated token or a mid-way disconnect all make the candidate incomplete.
3. Nested traversal maintains stable IDs of visited groups, the current path and a bounded queue, limiting depth, node count and total deadline.
   If a cycle exists but the closure is complete, deduplicate to a set per the approved policy and alert; if the contract forbids cycles, reject. When a limit is hit or the closure cannot be confirmed, the partial result must not be used as complete authorisation.
4. Apply the approved mapping to the complete set; unmapped groups do not invent roles. Union/precedence/explicit deny across multiple groups is decided by the project contract; do not default to "strongest group wins". Compute by the real global or resource scope.
5. The candidate carries a sync epoch/version and a scope-completeness flag, and is published atomically after verification. On failure keep diagnostics and the last complete version, but do not keep using old permissions indefinitely.
   Whether later requests are rejected or used with limits is decided by the authorisation freshness contract; see the authorisation and revocation topic.

Sync deletion or revocation needs complete-scope evidence; a partial read must not drive bulk deletion of users/groups. An explicit disable event may be marked rejected and sessions revoked on its own, without waiting for a full sync.
An older sync result arriving late must not overwrite a newer permission version; without a directory change sequence number, serialise publishing and record cross-page change/snapshot capability limits, re-checking affected users when needed.

## Synthetic cases

The base LDIF contains two users, multiple groups and a no-mapped-group scenario, with no production identities/passwords.
A cycle negative case can add group A member=B and B member=A in a separate fixture; the test returns a bounded closure or the rejection the project requires, and must not hang.
Duplicate identity keys, paging cookie loops, a lost second page and a late old epoch are constructed with a protocol stub; do not pretend the LDIF expresses every directory failure.

Normal: a user with the same stable key has their DN renamed; existing sessions still point to that principal, and groups are recomputed from the current complete result.
Counter-example: after deleting a user and recreating one with the same name, the old administrator relationship carries over because the DN is the same; the stable key must identify them as different principals.
An OpenLDAP fixture cannot prove nested group, paging or disable-attribute semantics of other directories.
