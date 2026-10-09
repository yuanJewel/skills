# Synthetic blue/green rehearsal template

Rehearse only in a local isolated environment the user explicitly allows.
Without that environment, the state model below can be used first to check decisions, explicitly marked "model passed".
blue/green are only synthetic target names, not real addresses. Real containers, proxies, connections and databases need separate evidence.

Preparation: two synthetic immutable artefacts A/B, independent instance identities, the existing local entry point, synthetic sessions/queues, an operation record and controllable readiness/metrics; reusing real traffic/data is forbidden.
The old/new schema compatibility switch is simulated by a fixture and cannot serve as proof about a real database.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Evidence:
    candidate: str
    ready: bool
    compatible: bool

def decide_switch(active, expected_old, evidence, observed_route):
    if observed_route is None:
        return "QUERY_ROUTE"
    if active != expected_old or observed_route != expected_old:
        return "RECONCILE"
    if not evidence.ready:
        return "KEEP_OLD_NOT_READY"
    if not evidence.compatible:
        return "KEEP_OLD_INCOMPATIBLE"
    return "MAY_SWITCH_LOCAL"

def decide_retire_old(route_is_new, inflight, metrics_ok):
    if not route_is_new:
        return "QUERY_ROUTE"
    if inflight > 0:
        return "WAIT_OR_DRAIN_BLOCKED"
    if metrics_ok is None:
        return "OBSERVATION_UNKNOWN"
    return "RETAIN_FOR_ROLLBACK" if metrics_ok else "EVALUATE_ROLLBACK"
```

The model only outputs the next step and performs no switch; real execution additionally needs an operation identity, candidate verification and authorisation.
`MAY_SWITCH_LOCAL` does not mean "already switched"; `RETAIN_FOR_ROLLBACK` does not mean the old environment may be deleted.
Cancellation and callback final states need separate verification against the project implementation.

| Synthetic scenario | Independent expectation | Evidence a real environment must add |
| --- | --- | --- |
| B warm-up fails | Keep A, route no traffic | Entry point still A and no requests reached B |
| Switch response lost | Query the entry point, no blind re-send | Operation record and the actual target of every entry point |
| Old connections not drained | Wait, or drain blocked | Actual in-flight long-lived connections/queue items and deadlines |
| Schema incompatible | Do not proceed with switch / do not promise rollback | Old/new read-write/message compatibility matrix |
| Mixed versions (A/B serving requests or messages concurrently) | Allow coexistence only if old/new read-write/message compatibility is verified; otherwise do not proceed | Requests/messages actually handled by each version during coexistence and their read-write results |
| New-traffic metrics fail | Evaluate rollback preconditions | Old artefact/data still recoverable |
| Repeated execution / stale callback | Return the original operation's facts; do not revive a final state | Persisted state machine / idempotent implementation |

Record candidate, environment, real start/end, first-round failures, recovery, unknown in-flight work and cleanup responsibility.
A successful rehearsal is not written up as a production traffic switch or a verified real managed-service event.
