# Naming, boundaries and errors

Read this page when verifying names, interfaces, errors and concurrency semantics. Do not expand one language's examples into rules for all languages.

## Naming and responsibility

Names state domain meaning, unit and state: for example `timeoutMs` distinguishes the duration unit, and `isEnabled` expresses a boolean test; specific casing/abbreviation follows project tools and language convention.
Short loop variables may stay; for cross-scope `data`/`flag`, judge whether the reader can identify the object; do not flag them mechanically from a name list.
Before changing public names, verify callers and serialisation compatibility; a local rename must not break an external protocol.

Function boundaries centre on one stable responsibility and a testable contract; inputs, outputs, side effects and failure modes are clear.
A long but linear mapping table may be easier to read than several jumping functions; a short function may also hide several side effects.
Early returns can reduce nesting, but must not skip required cleanup, transaction completion or response logic.

## Reuse judgment

For similar code, compare: input constraints, return semantics, errors, permissions, side effects, lifecycle, dependency/deployment boundaries. Syntactic similarity alone is not enough.
Use existing small utilities first; extract only when there really is a stable shared contract, and list the real callers, the differences kept and the shared failure impact.
If an abstraction needs many switches to express two continually changing branches, keep a clear local implementation for now.
Do not merge different permission paths to reduce line count.

## Error propagation and boundaries

Validate type, range and the conditions permission requires at the input boundary; whether to re-validate internally depends on how trusted the boundary is.
Errors keep the root cause and the context needed to locate it, while avoiding output of sensitive values.
Returning a default success value leaves the caller unable to distinguish "really empty" from "read failed"; return an error or an explicit degraded state per the contract.

Wrap errors with the language's native cause mechanism, such as Go's wrap chain, Python exception chaining, or JavaScript's supported cause; verify the actual version supports it in the project.
Do not log the same error at every layer and create duplicate logs, and do not catch, drop the cause and rethrow a generic string.
Log placement and client-error redaction follow project conventions; "add try/catch to every function" is not a general rule.

Concurrent tasks need clarity on who starts, who waits, who cancels and how the remaining tasks wind down after a failure.
Run in parallel only when independent and resources allow; serialise when there are ordering dependencies.
After request cancellation/timeout, no ownerless background task or held connection may remain; verify idempotency and side effects before retrying.
Concrete framework semantics are verified by the language package or project conventions.

## Language differences and reasonable exceptions

| Situation | Correct judgment | Counter-example |
| --- | --- | --- |
| Go struct maintaining counters/caches | Mutable state can be necessary; make the owner, locks or message passing explicit and verify concurrency semantics | Using an immutability slogan to create lock-free reads/writes or repeatedly copying lock-holding objects |
| Vue reactive object/ref | Keep dependency tracking per the project Vue version; allow framework-supported update methods | Replacing the reference for uniform immutable style, leaving consumers holding the old object |
| Python external dynamic payload | The boundary may use explicit Any and validate/narrow immediately; stable internal contracts use explicit types | Spreading Any across the module, or faking untrue types to eliminate Any |
| Third-party field names that break convention | Keep serialisation keys, map locally inside; note the contract source | Renaming JSON fields so old clients cannot read them |
| Inconsistent style in generated code | Find the generation source/version/tool configuration and regenerate through the allowed process | Hand-editing generated output, lost on the next generation |

These are judgment examples and do not mean any project's current version has been verified; give semantic conclusions after running the necessary specific checks.
