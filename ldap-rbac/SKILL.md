---
name: ldap-rbac
description: Design, review and synthetically verify LDAP login, directory sync, group-to-role mapping, API authorisation and revocation. Use for bind/search, identity uniqueness and stale-session invalidation problems. It obtains no credentials, queries no real directory and does not change existing permission categories on its own.
metadata:
  version: "0.1.0"
---

# LDAP authentication and authorisation

Take inputs first:

- authentication/authorisation contract, directory product and schema;
- permitted search base DN/scope/attributes, TLS trust and identity requirements;
- identity unique key, disable rules, group mapping and conflict precedence;
- session/cache invalidation deadline, and the approved local synthetic environment.

Design-only work needs no credentials. With schema missing, list the fields pending verification; do not query a real directory with a guessed memberOf or username rule.

## Working route

1. Draw authentication, group reading and authorisation decision as three timed stages, each with its own failure semantics. Authentication success does not grant write permission; a directory disconnect does not mean the user does not exist.
2. Per [Connection, search and bind](references/ldap-bind-and-search.md), verify TLS, empty passwords, input escaping, connection identity and timeouts. Reject invalid requests first, then look up the unique user with the service identity, and finally verify the user's credentials on a separate connection.
3. Per [Identity and groups](references/identity-and-groups.md), verify identity stability, paging completeness, cycles and multi-group computation. Separate "complete read with no mapped group" from "read failed".
4. Per [Authorisation and revocation](references/authorization-and-revocation.md), fill in the [permission matrix](assets/permission-matrix.md): resource, action, actual scope, field egress, approval and cache freshness.
   Implement only the current contract; do not use generic best practice to expand administrator capability or force multi-tenancy.
5. Use the [synthetic directory](assets/synthetic-directory.ldif) in an approved isolated OpenLDAP fixture to verify basic search/group structure. The file has no passwords; a successful login needs the test fixture to supply a synthetic password separately.
   Connection/TLS, paging and directory-specific behaviour need protocol tests; pure-function results cannot substitute.
6. Deliver the authentication sequence, matrix version, failure/revocation flows and evidence; mark each item as format check, static reasoning, actual protocol verification or unverified.
   On interruption, save the candidate version, identities of running synthetic resources and undetermined state; on recovery, first verify resource ownership and old writers.

Normal: a user with valid credentials and no mapped group, where the project contract assigns them a read-only guest role (e.g. guest), gets a session while restricted APIs reject.
Counter-example: a username containing search filter metacharacters widens the search and the first entry is taken; values must be escaped and exactly one identity required, otherwise login fails.

With the revocation deadline missing, output options and risks first; do not claim "immediate invalidation". With no usable LDAP instance, complete only the matrix, fixture and negative-case design; do not install a server or touch a real directory.

Resource guidance: single-item text/structure checks use `low/low`; routine implementation uses `normal/medium`; connection concurrency, identity merging and revocation races use `normal/high`. Grade words map to actual execution configuration through the project resource mapping.
Dependency simulation may combine with the evidence boundaries of `external-dependency-simulation`, but reading this file does not require loading the whole library.

**Closing cleanup**: synthetic directory instances or containers, imported test entries, sessions and token caches are cleaned up after verification ends. Follow the local resource cleanup rules of `task-implementation`: register identities at creation, at closing clean up only the objects registered this time, write evidence to keep and cleanup failures into the receipt, and use no global cleanup commands.

## Sources

1. Pinned sources: [WS03 auth-implementation-patterns](https://github.com/wshobson/agents/blob/46891e7e60da0e52baf1050b7b6391b64e84c6d9/plugins/developer-essentials/skills/auth-implementation-patterns/SKILL.md) and its [details](https://github.com/wshobson/agents/blob/46891e7e60da0e52baf1050b7b6391b64e84c6d9/plugins/developer-essentials/skills/auth-implementation-patterns/references/details.md), [EC01 security-review](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/skills/security-review/SKILL.md).
2. From WS03, adopted separation of authentication/authorisation, permission checks and session revocation; from EC01, trust boundaries and negative verification. LDAP, sync completeness, scope and revocation timing are own-authored for this package; topic RFCs are used only to verify short facts, and no example implementation is copied.
   Dropped URL tokens, default admin allow-all, fixed token lifetimes and imposed OAuth/MFA/multi-tenancy.
3. License: shipped with the package as [LICENSE-WS.txt](LICENSE-WS.txt) (WS, MIT), [LICENSE-EC.txt](LICENSE-EC.txt) (EC, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license files along when copying this package alone.
