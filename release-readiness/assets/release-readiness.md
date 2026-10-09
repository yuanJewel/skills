# Pre-release readiness recommendation

Main recommendation: {{ready for human acceptance / needs fixes or more evidence / awaiting final human decision}}.
Current candidate: {{actual content and artefact identity, environment; the version the user saw}}.
Scope and prerequisites: {{acceptance source, go-live intent, necessary prerequisites}}.

| Evidence category | Criteria/applicability | Source and candidate | Result and gaps |
| --- | --- | --- | --- |
| Review/known defects | {{scope}} | {{record}} | {{valid conclusion or pending fix}} |
| One local full suite | {{expected set and environment}} | {{shard/final-state reports}} | {{PASSED/FAILED/BLOCKED/N/A; state not run explicitly}} |
| Human acceptance/change retest | {{accepted scope and affected items}} | {{explicit decision and old/new candidate relationship}} | {{accepted / pending operation / change requested and retest}} |
| Other necessary categories | {{choose by risk, delete irrelevant rows}} | {{evidence or gap}} | {{applicability}} |

Residual risk: {{impact, mitigation/recovery prerequisites and decision responsibility; without an explicit decision it is not treated as accepted}}.
Real external manual items: {{applicable items such as traffic cutover/real event triggers, the boundary of local proof, follow-up responsibility}}.
Automated test time: {{actual/expected elapsed time with parallelism and waits}}.
Manual work/waiting/go-live window: {{give ranges, unknowns and conditions separately; no combined promise}}.
Follow-up: {{necessary extra evidence or human decision, retest rationale for candidate changes; in-flight work stated if any}}.

This summary is a pre-release recommendation; release execution and the actual go-live result are evidenced separately.
Reference it from the existing task/user presentation contract; do not copy the plan or status workbench.
