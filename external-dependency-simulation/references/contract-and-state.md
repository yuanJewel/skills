# Request contract, state and independent expectations

## Define requests first; avoid loose mocks

List method, path, query semantics for repeated/empty values/encoding, required headers, content-type, and body field types/defaults/unknown-field policy. Decide by protocol which parts are strict and which are ignored: do not be byte-strict to the point of ignoring equivalent JSON field order, and do not return 200 for any body. HTTP header names are usually case-insensitive; values and repeated headers are handled per the specific protocol.

Success, empty set, not found and forbidden are not the same result. Provide error status, machine code, retryability and necessary headers; do not echo sensitive details. Responses contain the fields and ranges the caller actually depends on; extra-field compatibility, missing fields, null vs. empty string are verified against the independent contract. Malicious/malformed input uses independent raw-bytes fixtures, which must not be corrected in advance by a normal JSON encoder.

## State changes and races

Describe `pre-state + request -> response + side effect + post-state`, and define separately the atomic section of a single request and the concurrent ordering. A retry may happen after a lost response; a client seeing a timeout does not mean the server did not write. A stateful fake must be able to express written, not written and uncertain.

Idempotency keys, resource versions and the dedup window are set by the contract. Same key with the same semantics returns the original result; same key with different semantics is rejected; an expired window does not automatically guarantee no repeats ever. When exactly-once execution must be judged, record the server-side effect count; do not just look at the client receiving one success. Duplicate events, reversed events, status polling and eventual consistency need explicit advancement conditions; a read must not unconditionally become success every time.

Pagination covers at least empty first/last pages, normal multiple pages, repeated/cyclic cursors, the same ID across pages, single-page failure and upstream data changes. Give stop conditions for loops/budgets; record whether already returned parts may be delivered, and never silently truncate and call it a full success. Use an injected advanceable clock for time and save the random seed; concurrency plans also need to be replayable, and a fixed seed does not make thread scheduling deterministic.

## Prevent "the implementation and the mock being wrong together"

Write expectations from an independent specification first, then connect the implementation. Keep at least one format or state counter example derived from the specification rather than recorded from the output under test. Use the real SDK to send requests locally and observe parsing behaviour; when SDK behaviour differs from the public protocol, report the version/difference and do not tamper with the protocol assumptions to make it pass. An existing schema validator can be used, but a valid schema still does not prove state and side effects are correct.

Write evidence separately: static fixture parsing, per-method content reasoning, real local protocol execution, real external behaviour. Taking the [declaration example](../assets/http-stub.json): parsing two pages of data only proves the fixture is readable; only when the adapter actually rejects unknown paths and the client completes both pages is there corresponding behavioural evidence.
The example's top-level `match_policy` declares the matching rules: `exact` requires a full match, so `"query": {}` means the request must carry no query parameters, and extra parameters go to unmatched. `unchecked` means the example does not declare that item, and the adapter must not claim on that basis that headers were validated.

Reset waits for this scenario's in-flight work to reach a final state through completion/cancellation, or creates a new isolated instance; record leftovers of the old instance. A shared global reset can let other tests pass by mistake; use scenario-level state or serialise constrained resources instead. Failed scenarios keep the minimal call history, fixed inputs and state, then generate a new scenario to retry without overwriting the original result.
