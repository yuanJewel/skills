# Task boundaries and verification methods

Consult the relevant section when task coupling, cross-module contracts, failure recovery or budget are uncertain. The examples below only illustrate the method; files, rules and technical choices follow the current project.

<a id="boundaries"></a>
## 1. Draw boundaries by acceptance loops

A task should answer: when are inputs available, to whom is it delivered, what changes, which observation means success, what state a failure leaves, who closes it. To judge whether a split works, imagine a reviewer accepting one part and returning the other: if the first part cannot be verified independently or would leave an unusable intermediate state, merge them or first establish an explicit usable contract with a compatible transition.

- Installation preparation, configuration and documentation are usually delivered with the capability they serve, unless they are themselves independently acceptable products.
- A shared file has one current writer; when two tasks touch the same file, data migration or exclusive environment, state the order or let one task integrate. Listing parallelisable tasks does not authorise spawning subtasks.
- A phase ends with a stable delivery and acceptance conditions. Dates are recorded only when the user actually gave them as constraints; "half done today" is not an acceptance condition. Large tasks may be phased, but unverified state is never turned into done because time is up.
- Task steps keep what the executor cannot decide alone: exact signatures, constrained values, state changes, key algorithm trade-offs and verification assertions. Established conventions may be followed by the executor; function bodies are not written line by line into the plan.

## 2. Establish a single interface contract

Each cross-boundary interface gets an I-ID, is produced by one task, and consumers reference that definition and its version. When schema/API documentation exists, reference the exact symbol and content version and list only changes; a type without a definition must have a definition location or owning task, never an empty name.

| Checked object | At least make explicit |
| --- | --- |
| Call shape | Module/file/symbol, method name and parameter order, types, return type; or HTTP method/path, RPC service/method, event name and payload schema. |
| Data semantics | Field names, units, nullable/default, enum meanings, identity source, pagination or ordering and other actually relevant constraints. |
| Behaviour | Who authenticates, what success and failure are, how state changes; with retry/concurrency/cancellation make idempotency, timeout, cancellation propagation and final state explicit. |
| Consumption relation | Producer task, consumer tasks, both baseline versions, adaptations that must come first and ownership of generated artefacts. |
| Proof | Corresponding verification ID, observable assertion and evidence; static type agreement proves only the part checked. |

For example, if the plan defines `lookup(id: string) -> Item | null` and another task calls `lookup(id: number) -> Promise<Item>`, there are three conflicts: input type, synchronous semantics and the not-found result. Unifying the method names on both sides is not enough: re-read the real interface and requirement, choose the supported contract, change the dependent design, and add verification of the not-found result and consumer behaviour. If the real interface was not read, record the pending I-ID and blocked tasks; do not guess one side as fact.

For protocol evolution, consult the relevant schema or protocol skill for the project's stack; a generic interface table does not by itself prove wire, JSON, generated-API or runtime compatibility.

<a id="recovery"></a>
## 3. Failure recovery and compatibility must be executable

Pick normal, error, boundary, permission, concurrency and recovery paths by the actual change; write irrelevant categories as not applicable with the reason. At least review conditions users will meet even if the requirement does not spell them out: empty/non-existent input, dependency timeout, partial success, duplicate requests, old clients, late results after cancellation. Do not impose every technical scenario on every project.

Each relevant failure F-ID records: trigger and observable signal, current persistent/external state, condition for stopping further actions, retry/compensation/rollback method, required permissions, post-recovery checks. "Roll back on failure" is not executable; state the recoverable baseline and target, who executes, and how to confirm no side effect is left. When rollback is impossible say so and give isolation, compensation or forward-fix paths and the decisions needed.

Compatibility K-ID records old/new producers and consumers, data formats, mixed-run window, migration order, rollback window and failure conditions. Restoring an old binary does not restore new-format data; the plan checks whether the rollback procedure can still read the data and whether dual read/write or reversible conversion is needed, adopting only strategies the project really needs.

Designing a recovery path grants no permission to perform its external operations; when permission or environment blocks that verification, name the actual owner, evidence needed and scope; other independent tasks continue.

<a id="estimates"></a>
## 4. Minimal estimation basis

Count research, implementation, verification and integration in the task hour range, without adding shared acceptance to every task again. Keep the estimate time, basis, main uncertainties and original estimate; later forecasts are listed separately. Resource parameters come from the project's current contract: main-task occupancy, tool and executor capability, available slots, concurrency quotas, exclusive environment limits, machine resources and unknown in-flight work; these host limits are supplied by project configuration.

The longest dependency chain is the lower bound of elapsed time without resource conflicts; after scheduling on actually available resources add integration and necessary waiting. For example, A needs 2 hours, B and C each depend on A and need 3 hours: 5 hours with enough independent resources; 8 hours when B and C share a single environment. Accumulated task effort is 8 hours either way and cannot be the sum divided by three tasks. The numbers only illustrate and are not project commitments.

Separate human waiting, external blocks, actual active time and measurable usage. Accumulated actual includes known retries and rework; on continuation read the old value; invisible tokens, prices or durations are marked "unknown/not provided", and no exact amount is derived from them. An explicit 0 may only mean an observed zero, such as evidenced not-yet-executed.

The estimate's grade-word suggestion (cost tier/reasoning tier) is not the host's actual effective configuration; grade words map to actual execution configuration through the project resource mapping. For an upgrade give purpose, time/resource impact and the user's options, then execute per existing authorisation and configuration. For a clear deviation explain the reason, remaining forecast and continue/adjust scope/hand over options; with existing continuous-execution authorisation and unchanged scope, continue while keeping the deviation facts, without turning every task into no-approval-needed.

<a id="review"></a>
## 5. Self-check and skill behaviour acceptance

Verify by the following relations, not merely by whether tables are filled:

1. From each original R-ID find task T-ID and acceptance V-ID; not found means omitted. Trace T-IDs in reverse; move unfounded new requirements to suggestions or clarification. Fact evidence and requirement sources are not mixed.
2. From each producer I-ID trace all consumers: name, parameters, types, return/error semantics, field units and version agree item by item; do not check only the current module. After a contract change check all affected tasks.
3. From risks and requirement boundaries find F-ID/K-ID and their verification; missing failure/old-version paths go to the actually responsible task, not only a "risks to watch" paragraph.
4. Check that exact files exist or are genuinely planned additions, and that verification commands/manual steps have prerequisites, inputs, assertions and evidence locations; unknown tools and commands not run are never marked as passed.
5. Verify dependencies and write permission allow the proposed parallelism, effort and elapsed time are separated, and approval references are really locatable and cover this candidate. Author self-check and independent review are recorded separately.

The scenarios below are behaviour acceptance samples for this method; actual results go into task evidence, never back into this page as a general guarantee:

| Input scene | Expected observation |
| --- | --- |
| Multi-module requirement with deliberately mismatched producer/consumer signatures and omitted handling of non-existent input | Locate the I-ID, affected tasks and missing V-ID explicitly; fix the contract after verifying facts, add boundary acceptance, do not just unify wording. |
| Complete approved design exists, continuation requested | Reference and verify the original design; no second plan, no re-confirming an already decided execution method; continue within authorisation. |
| New feature includes author-recommended extra product capability; compatibility baseline or approval evidence missing | The recommendation keeps its suggestion status; related tasks pending, design may continue; no claim of approval or compatibility pass. |
| Reversible low-risk copy fix | Use diff/rendering checks proportionate to risk, no mechanical full plan and test suite; project mandatory checks still apply. |
| Tasks limited by serial dependency/shared environment, continuation usage partly invisible | Elapsed time reflects the limit; original estimate and accumulated actual retained, no division by concurrency, unknown not recorded as zero. |
