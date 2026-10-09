---
name: http-api-design
description: Design or review new and evolving HTTP endpoints, making inputs and outputs, permissions, errors, idempotency, pagination and compatibility windows explicit. Internal fixes under an established contract verify only the affected boundaries; do not rebuild product requirements out of REST preference.
metadata:
  version: "0.1.0"
---

# HTTP API contract

Write down the behaviour callers can rely on, then choose the implementation. Inputs are the existing endpoints and consumers, the approved goal, identity/permissions, data scale, failure and retry semantics, the compatibility window, actual protocol/framework capabilities and the allowed verification environment. When key business semantics are missing, mark them pending verification and continue the structural and error review that does not depend on them.

## Method and routing

1. List endpoint -> caller -> resource scope -> business action -> possible side effects. Keep existing naming, response envelope and versioning strategy; explain the impact of consistency issues first, and do not switch to a new REST style on your own.
2. Read the [HTTP contract checklist](references/http-contract-checklist.md) and write, item by item, input constraints, authentication/authorisation, success/failure, timeouts and compatibility. Separate suggested extensions from what this round must do; capabilities the product did not ask for are not omissions.
3. When writes can be retried or lists are paginated, read [Idempotency and pagination](references/idempotency-and-pagination.md). An HTTP method name does not make the implementation safe; side-effect and state evidence is required.
4. Record observable examples, fields and errors with the [endpoint contract template](assets/endpoint-contract.md). When a complete API description already exists, only fill the gaps; do not create another authoritative format.
5. With synthetic requests, verify success, validation error, unauthenticated, forbidden, not found, conflict and rate limiting one by one; state why any case does not apply. Retries, permission changes and concurrent races need separate scenarios; a complete static contract does not mean the service passed real tests.
6. Output explicit decisions, pending verification items, compatible consumers and verification gaps. On interruption keep the contract version, verified requests and unknown in-flight work; after a write timeout check state first, and do not execute a side effect twice by retrying.

## Branches and recovery

- Old consumers unknown: a draft for a new endpoint can be finished; do not promise compatibility for existing clients or remove old fields immediately.
- Permission model unknown: state who must provide the definition; do not impose a "per-resource owner" or global role model. Filter sensitive fields at the authoritative egress; never fetch the full secret and then hide it in the UI.
- Unknown whether an operation is idempotent: state the possible side effects and the worst-case replay; do not recommend automatic retries before the contract is explicit.
- Test environment missing: do contract and state reasoning, record real network results as unverified; do not call production endpoints to fill the gap.

Normal example: keep the existing list envelope, add a unique sort key for data with identical timestamps and bind the filter conditions to the cursor, then verify there are no boundary duplicates between previous and next pages. Counter example: charging again on every delete just because DELETE is listed as idempotent. HTTP idempotency refers to the intended effect on the resource; it does not guarantee identical responses and does not allow extra side effects to replay without limit.

Mechanical field checks may use low/low; general endpoint design uses normal/medium; idempotency races, authentication/authorisation, mixed versions and pagination consistency use normal/high. Grade words map to actual execution configuration through the project resource mapping. Treat real external calls as a separately authorised action; documentation examples do not trigger them automatically.

## Sources

1. Pinned source: [EC06 api-design](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/skills/api-design/SKILL.md).
2. Adopted the method/status, error, pagination and compatibility framework; idempotency key scope/fingerprint/atomic race/expiry, pagination change gaps and field permissions are own-authored for this package, and the upstream is not recorded as a complete source for idempotency keys.
   Dropped the mandatory new envelope, URL version restructuring, fixed quotas and generalisations such as "adding a field is always compatible".
3. License: shipped with the package as [LICENSE-EC.txt](LICENSE-EC.txt) (EC, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license file along when copying this package alone.
