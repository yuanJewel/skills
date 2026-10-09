# Cross-boundary and performance diagnosis

## Find the first divergence from the user entry point

Draw the shortest chain along the real call path: entry -> identity/routing -> business transformation -> dependencies -> return.
At each boundary collect only allowed fields: request identity or a redacted correlation ID, candidate version, parameter summary, status code/business code, time, counts and result summary; no need to collect full secret payloads.

First pair upstream and downstream with correlated evidence from the same execution.
Different requests, an old candidate or a time-zone offset create false contradictions like "downstream succeeded but upstream failed".
When correlation is impossible, mark a gap in the chain and have the next experiment add correlation; missing logs do not prove the request never arrived, since logs may be sampled or lost.

| Observation | Discriminating next step |
| --- | --- |
| Entry fails, direct downstream access succeeds | On an approved local chain, compare routing, identity, timeout and parameters; a direct connection only narrows the scope and does not prove the full entry path is healthy |
| Value present before a boundary, field dropped / error code after it | For the same request, verify serialisation, defaults, protocol version and adaptation; record client and server candidates separately |
| Expected dependency response differs from the actual format | Verify the contract source and version; test product compatibility logic and fixtures separately; do not change fixtures first to follow the current state |
| HTTP succeeds but the business rejects or partially fails | Judge by the business contract; verify internal state, partial results and error mapping |
| External dependency unstable | Inject success/timeout/partial failure into a local stub to discriminate caller behaviour; the real dependency's cause remains unverified |

Normal example: the proxy timeout is shorter than downstream processing, and the direct connection succeeds.
Observe propagation of the original deadline, cancellation and late results; do not just enlarge every timeout.
Recovery example: the request's response was lost and the operation may already have executed; first look up the existing operation identity and final state, then decide whether a retry is allowed.

## Performance needs a comparable baseline

Define the metric the user cares about: throughput, latency distribution, peak resource use or error rate, with the threshold/tolerance set by the task.
When the threshold is unknown, give measured facts first and do not invent performance commitments.
Record data scale, hardware, candidate, concurrency, cold/warm cache, warm-up and measurement window.

Separate warm-up from measurement; interleave baseline and changed candidates or compare in an equivalent environment, keeping sample counts and distributions; never compare only one total duration.
For multi-stage systems, split queueing, compute, I/O and downstream wait; stage timings must come from the same execution, and overlapping stages are not added directly.

Observed resource saturation and queue growth can suggest a bottleneck hypothesis but are not independent proof.
Change concurrency, data scale or one dependency latency at a time and write the prediction beforehand:
if CPU-bound, raising concurrency does not increase throughput and CPU stays saturated; if downstream wait dominates, isolating stub latency lowers that stage's share.
A stub only explains controlled conditions and cannot sign off on real capacity.

When measurement noise exceeds the difference, error rates change or resources are contended, the conclusion is inconclusive; improve samples/environment and measure again.
Pause load loops that yield no information, saving current parameters and in-flight work; do not extend to unauthorised real services to test limits.
After an approved optimisation, re-measure the target metric, correctness and resource cost; faster but losing data is not an improvement.
