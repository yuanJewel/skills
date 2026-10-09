# Review dimensions and evidence thresholds

Read the dimensions relevant to the change first; for each, ask "what input or failure would make the goal fail", not merely whether the section exists.

## Scope and reuse

Break the original requirements into observable behaviours and trace them to plan tasks and acceptance; conversely, check why each task is necessary.
A missing requirement mapping may be an omission or a reasonable implementation detail; judge against the goal.
If a new service, new dependency, full migration or maintenance regime exceeds the goal, point out the added cost and the approval gap.

Before reuse, verify the actual callers and existing libraries: whether inputs/outputs, errors and side effects, permissions, dependencies and deployment boundaries match.
Similar names are not a shared contract.
The plan may use a proposed new caller, but mark it "proposed/assumption"; a function that does not yet exist cannot serve as evidence of reliable reuse.
When suggesting an abstraction, list the migration targets, the minimal contract and the shared failure impact; if the benefit is insufficient, keep the local implementation.

## Architecture and failure recovery

Along one real user path, draw entry -> authorisation -> domain processing -> data/external dependencies -> result; verify that each call edge is permitted by the project architecture.
Judge by identity and data sensitivity at which layer permissions are enforced, and whether the output can bypass the constraints.
Cross-module tasks must specify interface version, field meaning, backward/forward compatibility and dependency order, not just list module names.

For each new state change, take at least one realistic failure point: before the call, partial success, unknown result, retry, cancellation or restart.
Verify whether there is an idempotency identity, compensation or a recoverable checkpoint; for irreversible actions the word "rollback" does not replace recovery capability.
State who holds write permission during the operation, when it is released and what evidence recovery needs.
Specific protocol compatibility goes to the relevant technical method; do not declare compatibility from an overview.

Example: after a payment request times out it is resent immediately, but the original request may already have been charged, and the plan has no idempotency identity.
The evidence is the timeout branch and the interface definition; the plan gap can be pointed out without touching the real payment service.
Whether the actual backend already deduplicates is listed separately as pending verification.

## Quality and maintenance cost

Verify that each task has a precise change boundary, interface deliverables and an owner; a task cannot use "optimise everything" as acceptance.
Errors must keep cause and diagnosable context, not be swallowed and treated as success. Check input boundaries, nulls, duplicates, concurrency and changes to existing behaviour.
Existing project patterns come first; a new abstraction states why existing patterns are insufficient; do not manufacture a large refactor for the review.

Treat only problems substantively related to the goal as must-fix in this round. Out-of-scope facts may record location and impact without being expanded into implementation tasks.
Judging the current code requires reading the corresponding authored source/configuration; generated artefacts, copied files and documentation claims are not independent implementation evidence.

## Testing and acceptance

Each important behaviour maps to an assertion that can fail: what result normal input produces, how invalid/unauthorised input is rejected, how boundaries, concurrency and recovery are observed.
Existing tests need their assertions and run environment verified; a matching name does not mean coverage; asserting only "no exception thrown" does not prove the result is correct.

For a bug regression, state which precondition reproduces the old error and how fail-before-fix and pass-after-fix are evidenced.
When the implementer has not written code yet, what is reviewed is the acceptance design; do not claim tests have passed.
Copy-only, style-only or generated-artefact changes choose checks by impact; do not write duplicate assertions for volume.
Necessary checks come from approved behaviour/project gates; extra real-service or destructive verification is judged separately against authorisation.

## Performance and scale

Along each per-request and loop path, estimate call counts, rows, memory and waits: N+1, unbounded queries/caches, whole-file loads, blocking without timeouts, missing indexes or repeated computation.
List the expected scale and its source; for unknown scale give thresholds or open test questions, do not fabricate benchmarks.
A caching proposal also needs invalidation, consistency and sensitive-data boundaries verified. A small offline copy change may state that this dimension is not applicable.

## From observation to conclusion

`CONFIRMED` means the evidence suffices to confirm the fact stated in the item; `UNVERIFIED` means the original input or verification is still missing.
Neither automatically sets severity: a confirmed punctuation difference is not a blocker; an unknown key recovery capability may make the overall result pending evidence.

An issue must have: exact version and location, reproducible trigger, expectation, what the plan actually says, impact, evidence, minimal viable suggestion, necessary verification.
Try to disprove your own inference first; two models repeating the same assumption is not cross-validation.
After a fix, keep the original issue identity and verify the change's impact; do not hide unresolved items under new numbers.
