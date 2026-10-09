# Health, warm-up and connection draining

The liveness probe answers whether the process can still work, the readiness probe answers whether it can accept the target business traffic, and the startup probe allows a reasonable initialisation window.
An unavailable critical dependency may fail readiness; do not let every brief dependency failure trigger a liveness restart storm.
Probes perform necessary, bounded checks; they must not write business data or create load with expensive full-table queries.

Warm-up verifies the actual version, configuration structure/dependency readiness, cache loading and a minimum business smoke test; HTTP 200 does not automatically prove the response body is correct.
Timeouts, failure thresholds and success stabilisation periods are based on startup/request samples, not copied fixed seconds; without samples, mark a conservative estimate first and verify it.

Common blue/green order: prepare the new target -> new target ready -> switch the entry point so new requests go to the new target -> old target stops accepting new requests -> keep old long-lived connections/in-flight work until drained -> observe -> handle the old target per the rollback window.
The concrete proxy propagation and readiness-based removal order depend on the architecture; never kill the old process before verifying the new entry point.

Observation of old and new entry points covers the real target identity, convergence across multiple proxy/routing nodes, session affinity and WebSocket/streaming responses.
A simple DNS switch does not mean all clients update at once; existing connections do not move because of new DNS.

Draining defines the in-flight count, maximum duration, evidence that new requests have stopped, background job/queue ack boundaries and the timeout decision.
Force-stopping at the deadline interrupts requests; do it only when the contract allows and record it. Otherwise keep DRAIN_BLOCKED and move to an explicit disposition; do not announce completion.
Consumers must stop fetching and handle ack/redelivery; HTTP connection counts alone are not enough.

Observe the genuinely relevant metrics: error rate, latency, business success, queue backlog and resources.
Zero samples or missing metrics are unknown, not an error rate of 0; canary ramp-up needs enough samples or an explicit statement that no judgment is possible.
"No ERROR in the logs" does not replace critical business assertions.

Positive example: an old WebSocket keeps serving within the drain window while new requests go to the new version; on timeout, the remaining connections are recorded and the approved branch is executed.
Counter-examples: deleting the old environment immediately after readiness passes; the new version is healthy but a shared queue is double-consumed, creating duplicate jobs; writing the whole entry point as switched after a single proxy has switched.
