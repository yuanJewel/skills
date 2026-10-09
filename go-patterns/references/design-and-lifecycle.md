# Design, errors and resource lifecycle

## Let the consumer decide the abstraction

First find the real callers and the stable responsibility. If an existing concrete type meets the need, keep using it.
When an external boundary must be replaceable, a consumer's permissions must be narrowed, or there are multiple implementations, define the smallest interface near the consumer.
Whether to return a concrete type or an interface depends on public API encapsulation, compatibility and the replacement contract; do not force "always return a struct".
Avoid tests that must fake dozens of unrelated methods.

Constructors exist to validate required dependencies or establish invariants; a type whose zero value is safe to use needs no ceremonial constructor.
Writes to a nil map must initialise it or return an explicit error; a nil slice can be appended to.
An interface holding a typed nil is not equal to nil, so `if dep == nil` cannot catch every injected fault.
Choose the receiver by mutation, copy cost and method set; a value containing a mutex must not be copied after first use.

Do not equate "created a new interface" with correct layering.
Caller identity comes from a trusted entry point and must keep its meaning when passed across layers; ordinary user input must not forge a service identity.
Verify only the boundaries this change touches; do not expand into rebuilding the whole authentication system.

## Distinguishable errors, bounded exits

Internally, use `fmt.Errorf("load item: %w", err)` to keep the cause; callers use `errors.Is` / `errors.As` to distinguish cancellation, not found, conflict and temporary failure.
Do not compare strings. Whether to expose the underlying error type is part of the API contract.
If an underlying implementation detail must not become public contract, convert it to a stable business error at the authoritative exit while keeping safe internal diagnostics.

Wrap with the operation and a safe object identifier; do not concatenate tokens, raw request bodies or connection strings.
External errors and internal logs each choose their own disclosable fields; "logs are internal" does not permit arbitrary secrets.
For secondary errors from `Close`/rollback, keep the primary failure and record actionable secondary failures.
A successful write followed by a failed close/flush may mean data was not fully persisted; do not ignore it mechanically.

Example: a read interface returns `ErrNotFound`, and the caller tests `errors.Is(err, ErrNotFound)`; it is still distinguishable after another layer of wrapping.
Counter-example: replacing every error with `errors.New("failed")` loses cancellation and conflict and causes wrong retries.

## ctx, timeouts and resources

Within a request lifecycle, pass ctx along the chain, usually as the first parameter; never replace a still-valid request ctx with Background to escape cancellation.
A background long-lived task explicitly defined by the project gets its own task lifecycle, recording the task owner, state and termination protocol.

To shorten the time limit for a sub-operation, use `context.WithTimeout` with `defer cancel()`; do not arbitrarily extend a deadline the caller already set.
ctx must not be used as a bag of optional parameters; identity/trace values follow the trusted-entry contract.
Choose timeouts from the overall budget, retries and cleanup time; do not copy fixed values from examples.

| Resource | Success path after creation | Failure / early return | Verification focus |
| --- | --- | --- | --- |
| HTTP response | Consume the specified status / bounded body, close the body | When Do returns a response, body ownership still applies | Non-2xx is not success; response size limit and cancellation |
| File/stream | After writing, handle flush/close errors per the contract | Keep the primary error, run cleanup | Whether data is actually persisted before close |
| DB transaction | Promise success externally only after Commit | Attempt Rollback; an unknown commit result requires reconciliation | Do not blindly replay side effects that may already be committed |
| Lock | Protect the invariant within the smallest critical section | Release on early return too | No unbounded network calls while holding the lock |
| Buffer/slice | Make clear whether it is borrowed or handed over | Do not reuse while the caller still uses it | After returning to the Pool, the returned value must not point to the same backing memory |

Use pooling and preallocation only when a real hot spot benefits.
Analyse synchronisation for both shared maps and pointer fields inside maps; copying a map variable does not copy the data.
When returning a slice, state its mutability and retention period; copy when needed.

## Version and verification

Read the minimum supported toolchain, module replacements and existing lint configuration; prefer the existing standard library.
Examples such as `errors.Is/As` need support in the project version.
New concurrency helpers, range semantics or testing APIs cannot be justified for older versions just because they "compile" on the current machine.
When first verifying a new API, check the official documentation for the same version and record the exact page; if documentation is missing, keep it pending verification.

Before implementing, list one normal case and a matching failure counter-example: nil/empty input, wrapped error, whether resources are released after cancellation.
Interface and zero-value changes must also be checked against existing callers.
Static trade-offs can still be completed without an environment, but the receipt marks compilation, behaviour and races separately as unverified.
