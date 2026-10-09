---
name: go-patterns
description: Handle interfaces, errors, package boundaries, concurrency and resource lifecycle in Go implementation or review, choosing by the actual toolchain and existing patterns. Pure documentation or mechanical formatting changes need no expansion.
metadata:
  version: "0.1.0"
---

# Go implementation trade-offs

First obtain the approved change, similar implementations, go.mod and any applicable go.work, the actual compiler version, the call chain, the concurrency limit and latency constraints.
The goal is behaviour that is explicit and verifiable for this change; using this skill does not change the project layout or add abstraction.

## Choose a path

- Synchronous functions, errors or API boundaries: read [Design and lifecycle](references/design-and-lifecycle.md).
  First judge whether a direct implementation is enough; add interfaces, constructors and options only when a real consumer or invariant needs them.
- Goroutines, shared state or asynchronous exit: read [Concurrency](references/concurrency.md).
  Every task must answer who starts it, when it stops and who waits for it; if any of the three is missing, complete the design first.
- Formatting only: use the project formatter; do not expand into a full concurrency and architecture review.
- Delivery record needed: fill only the relevant items of the [change checklist](assets/go-change-checklist.md); for testing specifics combine with go-testing.

The go/toolchain directive in `go.mod` does not prove which compiler actually ran.
Record the real version with already approved tools; new standard-library APIs, language semantics and dependencies must work on the minimum supported version.

- Actual version missing -> use an approach already confirmed to work, or mark the new API as pending verification; do not upgrade the toolchain or dependencies automatically to make an example work.
- Approved scope or call chain missing -> make static trade-offs only and give a list of questions; do not change code.

## Method

1. Draw the shortest call chain; mark the original caller, permission boundaries, error categories and resource creation points.
   Existing project layering comes first; do not bypass the authoritative data or authorisation layer for convenience.
2. Write the observable result for normal, nil/empty, failure and timeout.
   Errors keep a distinguishable cause (`errors.Is/As`) and are converted per the contract at the external boundary.
   An internal cause chain does not mean SQL, tokens or connection strings may go into logs or responses.
3. Mark the owner and success/failure cleanup for files, response bodies, transactions, timers, locks and goroutines.
   The creator need not always release, but any handover must be explicit; failure paths and early returns must also close.
4. Introduce concurrency only with a clear benefit; set a limit, backpressure and exit waiting.
   Cancellation only signals; it does not guarantee downstream has stopped. For non-cancellable calls, state the boundary and the state after a bounded wait.
5. Check error discrimination, cancellation, nil/empty values and shared state with tests matching this change's risk.
   Existing healthy code needs no wholesale rewrite; tests not run are written as unverified, and a static explanation is not a race-detector pass.
6. Report the concrete trade-offs, required verification and unresolved boundaries.
   When the candidate changes, re-verify affected paths; on interruption keep the input version, actual commands and in-flight work, and continue after confirming the writer.

## Normal use and misuse

Normal: a synchronous step that only calls a local pure function returns its result directly; it needs no interface, worker pool or "unified base type".
When a remote request gains a timeout, pass ctx along the call chain, close the response body and verify the call exits after cancellation.

Misuse: creating a large same-named interface for every struct, or adding a goroutine and only calling cancel without waiting for it to exit.
Another common misuse is taking a buffer from `sync.Pool`, returning its underlying slice and then putting the buffer back; later reuse overwrites the earlier result.
Copy the result or make the ownership transfer explicit.

Mechanical checks may use low/low; ordinary implementation uses normal/medium; concurrency, compatibility, authorisation or cross-layer errors use normal/high.
Grade words map to actual execution configuration through the project resource mapping.
Optimise only after reproducible measurement; do not introduce dependencies, pools or concurrency for tiny synchronous functions.

## Sources

1. Pinned source: [EC04 golang-patterns](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/skills/golang-patterns/SKILL.md).
2. Adopted small interfaces, error wrapping, cancellation and simple design; resource owners, waiting, minimum version and failure branches are rewritten for this package.
   Dropped fixed directory layouts, one-size-fits-all interface/return-type rules, automatic dependency changes and worker/pool examples with unclosed ownership. When updating the language or dependencies, re-verify the related APIs and examples.
3. License: shipped with the package as [LICENSE-EC.txt](LICENSE-EC.txt) (EC, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license file along when copying this package alone.
