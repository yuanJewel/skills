# Choose the smallest feasible strategy

| Strategy | Preconditions | Main cost/failure window |
| --- | --- | --- |
| Stop-and-replace | Downtime explicitly allowed and recoverable | Zero-capacity window, data/startup failure; cannot be called zero-downtime |
| Rolling | Enough remaining capacity; old/new API/data/messages compatible | State races during mixed versions, long-lived connections, a batch failing; without verified readiness and scheduling, no promise of uninterrupted traffic |
| Blue/green | Two sets of capacity, an observable entry point, compatible shared data | Non-atomic entry-point propagation, surviving old connections, scheduled/consumer jobs running twice; an available old environment does not mean data can roll back |
| Canary | Isolatable percentage/tenant, trustworthy metrics and sample size | Low traffic gives no conclusion, sticky sessions bias samples, missing metrics; never auto-ramp without metrics |

Inputs first include the business-acceptable downtime/error budget, RTO/RPO and existing entry-point capabilities; do not introduce Kubernetes/a new proxy by default.
A small copy-text release still uses the existing artefact process, but does not build a whole blue/green setup.

Candidate identity includes the actual source content, artefact digest, configuration structure/snapshot, schema/message versions and target list.
Mutable tags must be resolved to the actual artefact; the approved object and the deployed object must be identical; this method requires no Git operations.

The database is usually not duplicated and isolated along with two application sets; old and new versions must be able to read and write coexisting data.
The schema compatibility window follows expand -> migrate -> stop old consumers -> contract; destructive actions get their own preconditions.
Old messages in queues, background workers, scheduled jobs and offline consumers also count as the old version.
When old code cannot understand a newly written format, switching back to the old image will fail: choose forward-fix/data recovery in advance, or forbid switching back.

Evaluate rollback: old artefact retrievable and verified, old configuration usable, schema/data still compatible, capacity for old instances, session/queue state can be taken over, entry-point switch-back observable.
RPO is the allowed data loss, not authorisation to delete new data at will; RTO includes detection, decision, execution and observation, not just the time to flip a switch.

Positive example: a small service without reliable metrics uses the existing rolling deployment with manual observation, and states the mixed-version compatibility.
Counter-example: choosing blue/green only because the name sounds advanced, ignoring the shared write database and two sets of scheduled jobs sending duplicate messages.
