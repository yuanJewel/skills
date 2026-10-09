# gRPC runtime contract

Use when RPC behaviour, client policy, interceptors, identity, errors or streaming change. Adapted from GH02, extended with trust boundaries and failure assertions; sources and license are in the [NOTICE](../NOTICE.md). This page is a review method; it does not authorise access to real services or replacing protocol mechanisms.

## 1. Method identity and consumers

Write the RPC as `/package.Service/Method`, and record request/response types, unary/client-stream/server-stream/bidi mode, proxy/transcoding routes and existing client versions. Renaming, moving packages, deleting methods or changing streaming mode all change the existing call contract; message fields being wire-compatible does not keep the old method path working.

Read consumers' connection lifecycle, credential injection, timeouts, error handling and service config. A schema-only change can also touch gateway mappings, auth path allowlists or generated interfaces; verify by actual impact. Choose a parallel method/version only when an incompatible migration is needed; do not add an RPC for every small change.

For affected unary methods also verify request/response size, repeated element count, nesting complexity, downstream fan-out and in-flight limits. Small bytes do not mean small work; complete necessary identity/parameter/capacity validation before expensive or irreversible work. Keep the limits of the project contract, and use synthetic inputs at exactly the bound, over the bound, and cancelled after partial start to verify the point of rejection, peak concurrency and resource reclamation. Do not invent new uniform numbers or force a validation library.

## 2. Deadline and cancellation

Record the caller's total budget, per-hop limits and cancellation sources. gRPC provides no deadline by default; for the calls affected this time, adopt the project's agreed finite budget and calibrate with latency/load evidence. Downstream calls derive from the parent context, taking the tighter of the remaining budget and this hop's limit; do not grant a full budget again and extend the original call. Verify the propagation configuration of the language and library; do not infer other languages from Go's behaviour. [Official deadlines](https://grpc.io/docs/guides/deadlines/)

Cancellation must reach the handler, derived tasks, blocking waits and downstream calls; the library usually cannot forcibly interrupt a business handler, so the implementation must actively observe cancellation and release resources. Test explicit client cancellation, deadline expiry and downstream failing first; check that subsequent work stops and goroutines/tasks/queues converge. Accepted async tasks that should keep running after the parent call is cancelled must have their ownership defined by the existing business contract; do not quietly continue with a detached context. [Official cancellation](https://grpc.io/docs/guides/cancellation/)

DEADLINE_EXCEEDED seen by the client and CANCELLED seen by the server need not match; keep each side's real final state and causality, and do not translate propagated cancellation into success or an unrelated business error. Cancellation signals loss of interest/stop work; it does not guarantee that committed side effects are undone. Define the commit boundary and result reconciliation separately.

## 3. Interceptors, identity and metadata

Record the chain actually traversed by unary and streaming calls, the library-defined inbound/outbound execution order and failure short-circuiting. The order must satisfy concrete dependencies: authorise by trusted principal only after authentication completes; log output after error normalisation must still be masked; a rejection mid-chain must neither skip recording the result nor continue business execution. Prefer the project's existing call credentials/secure channel mechanism for credential injection; interceptors cannot replace TLS or connection authentication. [Official interceptors](https://grpc.io/docs/guides/interceptors/)

Build a field table for the metadata actually used: key, producer, validator, forwarding destination, trusted source, repeated-value rule, size limit, logging policy and cleanup responsibility. In particular distinguish:

- Connection/service identity, original caller, and trace/correlation ID each have their own use; trace is not identity.
- An externally supplied "original caller" is only a claim; the entry point establishes trusted context from the authentication result and then propagates it to downstream services with a trust relationship. Reject or overwrite forged/duplicate conflicting values; do not copy external metadata wholesale into internal calls.
- Outbound carries only fields the downstream needs and credentials suited to that audience; do not leak upstream tokens, and do not cache one request's mutable metadata for other requests.
- Verify masking in logs, tracing attributes, error details and trailers; use synthetic sentinel values to verify credentials/sensitive identifiers do not appear in output. Record only necessary key presence, classification or controlled identifiers.

Check key names, binary suffixes, headers/trailers and library behaviour against the actual implementation; custom keys must not use the reserved `grpc-` prefix. Metadata limits are not business payload limits; verify each separately. Do not write documented suggested sizes as a fixed limit for all deployments. [Official metadata](https://grpc.io/docs/guides/metadata/)

Long-lived streams need explicit authentication points, the effect of credential expiry/revocation on established streams, and reconnect rules. Verifying only that the stream was established does not justify claiming later identity changes are handled.

## 4. Status and error details

For each change list "trigger condition -> original standard code/business code/details -> new value -> client action". Keep the project's existing business error carrier; do not force a new response envelope or rich error model. Avoid collapsing known errors into UNKNOWN/INTERNAL, or exposing raw exceptions, SQL, tokens or internal addresses.

| Semantics | Verify code and caller behaviour |
| --- | --- |
| The argument itself is invalid | INVALID_ARGUMENT; change the input |
| System state does not meet a precondition | FAILED_PRECONDITION; retrying before state is fixed is useless |
| Concurrent transaction conflict | ABORTED; may need to redo the whole read-modify-write sequence |
| Temporarily unavailable | UNAVAILABLE; whether retryable still depends on this method's side effects |
| Quota/capacity exhausted | RESOURCE_EXHAUSTED; follow the rate limit and backoff contract |
| Missing/invalid authentication vs. no access | UNAUTHENTICATED / PERMISSION_DENIED; existence hiding per the existing authorisation contract |
| Deadline/cancel | Keep the real DEADLINE_EXCEEDED / CANCELLED; do not assert the server did not execute |

The code is part of the compatibility contract; changing it affects SDK branches, retries, alerts and monitoring. If details use structured messages, record type/version/fields, size and the degraded behaviour when an old client does not know the detail; degradation should still keep the standard code, and retry decisions must not rely on parsing human-readable text. Verify whether proxies preserve trailers/details; "sent by the server" does not mean readable by the client. [Official status](https://grpc.io/docs/guides/status-codes/), [Error handling](https://grpc.io/docs/guides/error/)

## 5. Retries and unknown results

Enumerate the actual retry layers: application loops, SDK/gRPC, gateway/proxy, job redelivery. Distinguish logical requests from attempts; verify total count, backoff/jitter, rate limiting/server pushback and the overall deadline, avoiding multiplication across layers. gRPC transparent retry differs from an explicit policy; once response headers are received gRPC treats the call as committed and that mechanism no longer retries, but this is not proof of a business transaction commit and does not stop upper layers from resending. [Official retry](https://grpc.io/docs/guides/retry/)

For methods with side effects, first walk through "state committed -> response lost -> client receives UNAVAILABLE/DEADLINE_EXCEEDED". Do not conclude from the status code that nothing executed, and do not directly recommend retrying. Verify against existing mechanisms:

1. Whether it is naturally idempotent, or has a stable operation identifier/idempotency key and a queryable result; without such guarantees mark the result unknown, and query/reconcile or recover manually first.
2. Whether the dedup identity is bound to caller/scope and request content; how same key with a different payload is rejected; other principals must not read the original result.
3. Whether concurrent identical requests atomically acquire execution rights; how a crash between the side effect and writing the dedup result is handled; whether the result can still be determined after process restart.
4. Whether the retention window covers the longest retry/replay; whether a retry after expiry may execute again; whether replay returns the established result or executes again.

Design supplementary mechanisms only when authorised and required; a review must not install a dedup layer across the whole system along the way. Verification injects after commit and before response, asserting the number of business effects and the final queryable result; then cover same-key concurrency, different payloads, non-retryable errors and no new attempt after cancellation. Metrics should distinguish attempts from logical requests; a successful retry must not mask duplicate side effects.

## 6. Streaming lifecycle

State for each direction the message order, who terminates, half-close, final status, resource owner and bounded buffering. A client finishing sending is only a half-close; the server can still return messages. The client should keep reading until the stream's final state and check the final status. A successful Send may only mean entry into the framework buffer, not remote processing/persistence; reading messages midway does not replace final completion. [Official lifecycle](https://grpc.io/docs/what-is-grpc/core-concepts/)

Flow control can block sending, but application-built queues must still be bounded. State where backpressure goes with slow consumers, the block/reject policy when queues are full, per-message/total/concurrency limits, and whether cancellation unblocks Send/Recv/queue waits. Bidi avoids deadlock from both sides only writing and never reading; verify concurrent read/write and same-direction concurrency limits against the language API. [Official flow control](https://grpc.io/docs/guides/flow-control/)

Whether a stream can resume after interruption is decided by the business contract; gRPC does not provide business-level exactly-once/replay automatically. With existing cursors/acknowledgement points, describe sequence numbers, duplicates, dedup and expiry; do not require resume mechanisms for streams without that need.

For this streaming mode choose at least: empty stream with normal half-close, half-close after several messages with the final result received, slow reader and full queue, active cancellation from both sides, server error midway, disconnect/reconnect. Assert received content and order, final state, buffer limits and that all resources are eventually released; for long-lived streams also verify identity expiry. Half-close must not wrongly cancel the server's remaining responses, and cancellation must not leave permanently blocked tasks.

## 7. Scope of evidence

Run old client -> new service and new client -> old service against the actually supported versions; keep results for method path, authentication failure, details, deadline/cancel, lost response and stream close. In-memory transport can prove the tested handler and interceptor logic, but not real TLS, HTTP/2 proxies, load balancing or the release environment; keep these untested items explicit. When checks or fault injection are unavailable, write executable expectations and the reason for being unverified; do not fill in a pass with reasoning.
