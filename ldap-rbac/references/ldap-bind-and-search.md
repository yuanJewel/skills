# Connection, search and user bind

## Authentication sequence

1. Validate input length, encoding and required fields per the authentication contract; reject an empty username and a zero-length password outright. Do not trim, normalise or log the password; a successful service bind is not user authentication success.
2. Establish a TLS channel with connect/handshake/read-write deadlines: verify the trust chain and the target server identity. StartTLS must succeed before any secret is sent; on failure close the connection and never fall back to plaintext; LDAPS verifies the certificate likewise.
   TLS versions/cipher suites follow current platform policy; do not copy the old suite recommendations of early RFCs.
3. Search the permitted base DN, scope and attributes with a least-privilege service identity (bind DN); terminate if the service bind fails.
   Search scope, attribute names and search filter structure come from trusted configuration; the user supplies only one escaped value and cannot choose arbitrary attributes or concatenate a full filter.
4. The search returns exactly one user; take the returned DN and stable identity key. Zero entries is authentication failure; multiple entries is an identity conflict: alert internally, return the uniform failure externally, and never take the first.
   Size limit/time limit/referral/missing page means "incomplete", never zero entries or unique.
5. Establish a separate, TLS-verified user connection and bind with the DN returned by the search and the non-empty input password. On failure create no session; on success read the necessary state or check disable rules on a controlled service connection, then obtain the complete mapping.
   The service search connection and user connection must not share concurrent rebinds; connection pools are isolated per identity, and connections with unknown/failed identity are destroyed.
6. Create a session only after identity verification succeeds, the user may log in and authorisation state satisfies the current contract. Store the stable identity key and permission version, never the directory password; close the user connection and return the service connection per a safe pool policy.
   Every branch has timeouts, cancellation and connection reclamation.

Anonymous directory reads are used only where an isolated test explicitly allows them; they never constitute application login.
RFC4513 distinguishes anonymous bind with empty DN/empty password from unauthenticated bind with non-empty DN/empty password; a server returning success cannot replace verification of non-empty credentials.
There is no single cross-directory attribute for disabled state; use the verified schema/directory policy.

## The two escapes must not be mixed

- Filter assertion values use the library's RFC4515 encoding: `*`, `(`, `)`, backslash and NUL are each byte-encoded; e.g. the value `a*(b)` becomes `a\2a\28b\29`. Handle invalid UTF-8 bytes per library support/input contract; do not tolerantly replace them first and then wrongly merge identities.
- Obtaining the DN from the search result is safest; when it must be constructed, use the RFC4514 DN API for each RDN value, then assemble the structure. Commas, plus signs, leading/trailing spaces and so on carry DN meaning; filter escaping cannot be used for DNs and DN escaping cannot be used for filters. Compare DNs with a library/directory that supports schema semantics, not a simple lower-cased string.
- Keep already-escaped strings and raw input as separate types to avoid double escaping. If a returned DN goes into a later filter, encode it again as a filter value; do not concatenate it directly because it "came from the directory".

## Failure and evidence

Reject expired certificates, identity mismatches and untrusted CAs; simulate wrong password, empty password, username injection, two matching users, search success with results over the limit, interrupted bind, and two users concurrently.
Assert no wrongful session, no cross-user connection identity leakage and no password logging.
The authentication entry rate-limits attempts per project limits with a uniform external failure message; internally record only the reason class, correlation ID and necessary masked identity; never log the full request/directory secrets.

After a timeout, read-only searches may be retried, still bounded by the total deadline/retry count; failed logins do not automatically repeat many binds that would trigger directory lockout.
Distinguish authentication failure from service unavailability internally; responses follow the project envelope and do not reveal whether the user exists.

Basis: [RFC4513 §3.1.3, §5.1](https://www.rfc-editor.org/rfc/rfc4513), [RFC4515 §3](https://www.rfc-editor.org/rfc/rfc4515), [RFC4514 §2](https://www.rfc-editor.org/rfc/rfc4514). Only identity verification and encoding semantics are used; the TLS recommendations of RFC4513 must be combined with current updates.
