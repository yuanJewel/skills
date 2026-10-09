# Deployment and recovery runbook

Target/executor and boundary: {{local rehearsal or manual real operation; existing approval reference}}.
Candidate/target/previous version: {{immutable artefact, configuration structure, schema/messages, target set}}.
Strategy and rationale: {{current topology, capacity, downtime, RTO/RPO, mixed-version preconditions}}.
Operation identity/state record: {{deployment/operation ID, sole writer, query/callback entry}}.

| Step | Preconditions | Exact target action/executor | Success evidence | Failure/unknown recovery |
| --- | --- | --- | --- | --- |
| Prepare/deploy/ready | {{candidate etc.}} | {{local or manual execution}} | {{per target}} | {{keep old/query}} |
| Switch/drain/observe | {{stable readiness etc.}} | {{entry-point identity and conditions}} | {{traffic/connections/business}} | {{bounded branch}} |
| Rollback | {{artefact and data compatibility}} | {{rollback operation ID}} | {{entry point/critical path}} | {{where a failed rollback goes}} |

Metric window/samples/thresholds: {{source, no-data branch}}.
Repeat/cancel/restart: {{idempotency key, cancel intent, final-state reconciliation}}.
Resource exit: {{old environment/artefact retention conditions, owner, cleanup result}}.
Actual evidence/unverified: {{record local model, real local environment and external manual work separately}}.
