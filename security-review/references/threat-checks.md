# From controllable input to actual impact

Choose the checks that match this change; loading unrelated tech stacks every time is not required.
Every finding must form the causal chain "controller -> input -> path -> missing constraint -> impact".

## Identity and object-level authorisation

Verify separately: whether the credential is valid, whether the principal may perform the action, whether the principal may access this object/tenant, and whether field-level output is allowed.
An internal request identity must come from trusted propagation or a verified service contract; never accept an external header that directly elevates identity.
Service-to-service authentication only says which service it is; it does not prove the original user has permission on every resource.

When roles or groups change or an account is disabled, check whether sessions/caches are invalidated per the project contract; do not decide a global force-logout policy on your own.
For async jobs, verify whether authorisation is checked at enqueue, at execution or both, and what happens after object ownership changes.
Where facts are missing, list the specific state as pending verification.

Synthetic negative cases: logged-in user A requests object B without permission; a forged internal-user header; reusing an old session after revocation;
a batch request mixing in one unauthorised object.
Expectations come from the project permission contract; do not make a capability the contract does not require (such as per-tenant isolation) mandatory on your own.

## Authoritative sensitive outputs and machine use

Enumerate the outputs: responses, logs, errors, audit, caches, exports, generated configuration and historical versions.
The sensitivity decision sits in the authoritative layer the project designates; stripping fields in an upper layer does not prove other callers will not leak.
Error wrapping and internal logs likewise must not emit raw secrets.

An approved machine-use exception must be limited by purpose, input object and output consumer. It is not a general identity.
If the project contract lists history records or echoed render results as sensitive outputs, "internal call" cannot be used to open history records or echo render results to unauthorised principals.
Check ordinary principals, approved administrative principals, machine flows and the contract-listed sensitive outputs separately;
judge by the project's exact contract, not by permissions this package adds on its own.

Distinguish a redaction placeholder from a new secret being written: saving a page must not write the mask back to the original field, nor leak the true value through returned length/error details.
Verify only with manually constructed marker values; do not sample real configuration. When locating a log leak, report the field name/path, not the full value.

## Input, interpreters and the filesystem

- **Database**: bind values with driver parameter binding; dynamic table names/sort columns cannot be solved with value placeholders and must be mapped from an allowlist.
  Raw expressions in an ORM still need their controlling source traced.
- **Commands**: prefer a fixed program and an argument array. No shell does not mean no risk: also verify whether a controllable argument becomes an option, a target path or a sub-tool expression.
  Quoting and escaping cannot replace a semantic allowlist.
- **Paths/uploads**: judge against the real allowed root; verify path traversal, absolute paths, symlinks, overwrite/race conditions and non-regular files.
  Extension/MIME is a hint, not proof the content is safe; when archives are processed, also verify extraction paths and total size/entry count.
  The validator must take effect before the path is consumed.
- **External URLs**: verify scheme, destination address, the boundary after DNS resolution/redirects and the response body limit.
  A string containing localhost does not prove isolation, and a loopback proxy may still reach a real remote.
  SSRF suspicions can first be verified with the source chain and synthetic redirects, without actually probing private services.
- **Parsing boundaries**: check length, nesting depth, numeric range, nulls, duplicate keys, invalid encoding and pagination limits per the specific protocol;
  do not swallow parse errors and produce a successful default.

## Output, sessions and the browser

Choose encoding by the actual output context (HTML, attribute, URL, script); treat normal template escaping and explicit raw HTML rendering differently.
Rich-text sanitisation must match allowed tags/attributes/schemes, not just remove script. CSP is only a supplement and cannot replace correct encoding.

Cookie policy follows same-site/cross-site needs and the authentication method; verify HttpOnly/Secure, SameSite and CSRF protection separately;
SameSite=Strict cannot be applied unconditionally to every product.
CSRF concerns credentials the browser attaches automatically and state-changing paths; CORS is a browser read restriction, not authentication or backend access control.
For credentialed cross-origin requests, verify the exact origin, preflight and caching differences; do not widen authorisation with a wildcard origin.

Name webhooks precisely by protocol: a shared token is token verification, not a signature; a real MAC/signature needs raw bytes, algorithm, timestamp/replay and rotation rules verified.
Compare with a suitable primitive; after authentication passes, still verify event type, object scope and idempotency identity. Do not assume a vendor's signature mechanism from a header name.

## Resources and dependencies

Along paths an attacker can trigger, verify concurrency, timeouts, retries, size, decompression, pagination and cache growth;
even if each layer "has a timeout", the overall deadline still needs verifying.
Limits are chosen by real business load, not copied from fixed counts in upstream examples. A failure response must not leave unbounded work running in the background.

For dependencies, first verify the actual version, the lockfile and the code reachable at runtime;
an advisory name match does not mean affected, and unknown usage or reachability stays pending verification.
Install scripts, provenance, signatures/checksums and licences are handled per the project's supply-chain rules; the review does not automatically run package-manager fixes or bulk upgrades.
Never claim "no vulnerabilities" because it is the "latest version".

## Evidence levels

Source can confirm facts such as a directly missing object check or a sensitive field entering logs;
whether it is externally exploitable may also depend on entry-point reachability, so write the two separately.
A synthetic experiment only proves behaviour under the isolation premise.
Dynamic tool reports need scan scope, rules, version and raw findings verified; an empty report or a tool failure does not mean pass.
The report states the paths covered this time, the invisible premises and the remaining verification; it gives no absolute whole-system security conclusion.
