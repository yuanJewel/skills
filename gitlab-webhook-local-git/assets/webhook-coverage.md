# Webhook coverage and boundaries

- Approved scope/source candidate/actual GitLab version: {{evidence}}
- Authentication mode and route: {{token/signature/controlled migration; basis for capability and timeliness}}
- Allowed events/project/ref/caller permissions: {{existing contract; unknown items}}
- schema/delivery ID/business operation mapping: {{header/body consistency and dedup window}}
- Local Git manifest: {{only when Git actions are needed; root, instance, endpoint, path, ref, operations, cleanup}}

| Scenario | Synthetic input and independent expectation | Actual method | Result/evidence | Unverified |
| --- | --- | --- | --- | --- |
| Authentication/freshness | {{wrong token/bad signature/replay}} | {{pure function/HTTP stub}} | {{rejected with no side effects}} | {{version}} |
| Events/permissions | {{unknown/ownership/ref/caller}} | {{method}} | {{result}} | {{missing items}} |
| Duplicates/concurrency/out-of-order | {{inbox -> operation -> build}} | {{fault location}} | {{counts and states}} | {{real trigger}} |
| Git boundary | {{path/alias/redirect/SSH}} | {{approved synthetic service only}} | {{admitted/rejected}} | {{forbidden external items}} |

- In-flight/recovery: {{unknown initiations queried first, dedup state not cleared}}
- Verdict: {{event contract, Git protocol, real GitLab each separately; no external registration/tunnel}}
