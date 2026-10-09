# Go change trade-offs and evidence

- Goal / approved scope / candidate identity: {{task_reference}}
- Minimum supported version, actual toolchain, dependencies and replacements: {{evidence; unknown items}}
- Affected call chain and consumers: {{identity/permission/error boundaries}}
- Choice: {{sync/concurrent; whether an interface/constructor is needed; which existing pattern is reused}}
- Input and failure contract: {{zero value, nil, empty collection, cancellation, timeout, business errors}}

| Resource or task | Owner | Exit/release | Wait/completion evidence | State after failure |
| --- | --- | --- | --- | --- |
| {{file/body/transaction/goroutine}} | {{creation and handover}} | {{each branch}} | {{who verifies final state}} | {{unknown side effects/retryability}} |

| Check | Independent expectation | Command/input | Actual result | Not covered |
| --- | --- | --- | --- | --- |
| {{errors, cancellation, races and other relevant items}} | {{contract}} | {{existing tool and version}} | {{exit code/evidence location}} | {{reason}} |

- Performance trade-off: {{conclude only with measurement; not applicable without a hot spot}}
- Failure recovery / in-flight / next step: {{keep the candidate, what was done and what still needs verification; do not treat cancellation as stopped}}
