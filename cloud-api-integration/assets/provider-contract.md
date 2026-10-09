# Provider call contract

Scope/version: {{provider, API/SDK version, actual method/action and source URL}}.
Client mode: {{direct HTTP or existing SDK, construction injection, evidence that default credentials/metadata are disabled}}.
Allowed targets: {{local endpoint/transport, redirect/nextLink/status URL validation}}.
Request/auth: {{parameters/encoding/signature version, synthetic clock/nonce/key; never fill in real credentials}}.

| Call | Input/response fields | Pagination completion | Errors/retries | Async final state/idempotency |
| --- | --- | --- | --- | --- |
| {{required API}} | {{type/nullable/unit}} | {{exact criterion}} | {{category/budget}} | {{operation identity}} |

Domain identity/mapping: {{provider/account/region/kind/ID, time/precision/unknown state}}.
Completeness/reconciliation: {{full set per scope, manual protection, association preservation, distinguishing complete-empty from incomplete}}.

| Synthetic scenario | Independent expectation | Actual result/evidence | Boundary of proof |
| --- | --- | --- | --- |
| Pagination/failure/cancellation | {{chosen per this API}} | {{first run and re-verification}} | {{model/HTTP/SDK}} |

Unverified and recovery: {{real provider behaviour, missing SDK, operation/token/in-flight work, next step}}.
