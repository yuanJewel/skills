# Local failure diagnostic map

This is a method for choosing evidence, not an unconditional command list. Use only verified local probes; field scope and budget follow the probe safety reference.

| Symptom | Preferred narrow evidence | Must distinguish | Never do automatically |
| --- | --- | --- | --- |
| Container not ready/restarting repeatedly | Instance identity, state/exit code, health result, recent bounded safe error categories | Not started, startup failure, dependency not ready, readiness failure | Restart, recreate, full inspect, change environment variables |
| Latency/timeout | Per-phase request latency, pool wait/active count, queue length, CPU/memory summary | Client-side queueing, slow dependency, blocked main loop, GC/resource pressure | Scale out, change timeouts, clear caches to try |
| Connection failure | Allowed target and port identity, connection error type and sampling time | DNS, refused, TLS, proxy/network boundary | Change DNS/certificates, bypass the proxy, access real services |
| Endpoint returns 200 but the function fails | Business state/error code, correlation ID and call-chain phase | Success-response shell, partial failure, stale artefact, expired cache | Write to the DB directly or repeat non-idempotent requests |
| Inconsistent state/out-of-order callbacks | Operation identity, persisted state version, callback time/final-state metadata | Unknown request, late event, repeated execution, aggregation gap | Back-sign success, re-send jobs, delete old records |
| Log times disagree | Original time zone/precision, source clock skew, the same correlated event | True ordering, buffering delay, time-zone misinterpretation | Infer root cause after converting with the host default |

Escalate scope stepwise: existing evidence -> narrow sampling of one target -> allowed scope of related dependencies.
Each widening states why it can distinguish the current hypotheses; it is not a scan of the whole workspace or all container logs.
A dynamic "recent" must be replaced by the actual collection window, so samples from different rounds are not compared by mistake.

Local reproduction needs independent purely synthetic input, seed, execution and cleanup records; this skill only proposes the design, and the corresponding test process runs it when existing authorisation explicitly covers it.
When an application fix needs code changes, hand it to the approved implementation scope; do not fix in passing because the diagnostic tool happens to have write capability.

Positive example: for an endpoint timeout, first look at pool_wait's share of total latency, then verify connection return in this case.
Counter-examples: ruling out the connection pool just because CPU is low, or running an automatic full audit/scanning a real cloud because a security warning appeared in the logs.
