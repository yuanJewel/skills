---
name: test-strategy
description: Choose test scope, assertions, fixtures and execution isolation from the behaviour and risk of the current change, and state the reasons for what is covered and what is not tested. Use to create or adjust a verification approach; language-specific test implementation, completion judgement and release ordering are handled by their dedicated methods.
metadata:
  version: "0.1.0"
---

# Risk-driven test strategy

Choose the smallest effective verification mix that catches this change's failure modes. More tests are not automatically more trustworthy, and coverage cannot replace independent expectations.

## Inputs

Read the approved acceptance, the changed behaviour/interfaces, the candidate content, existing cases and run entry points,
dependency stubs, environment/data ownership, machine resources and comparable durations.
For an unknown interface or expectation, settle the contract first; when the run foundation is missing, propose the minimal items to add, and do not build another framework to "improve quality".
With an existing plan, add the test part directly; do not copy the overall plan or status board.

## Selection and execution

1. **List behaviours and failure modes.** Starting from user-observable results, data/state changes and consumers, build the mapping
   "behaviour -> possible failure -> capturing layer -> independent assertion -> fixture -> evidence".
   Check the impact surface per [Risk and scope](references/risk-and-scope.md), and give the untested items with reasons.
2. **Choose the lowest effective layer.** L0 copy/static changes may be checked only; L1 local deterministic behaviour gets unit tests or targeted regression;
   L2 data/interface/state combinations get integration and contract tests;
   L3 authentication/authorisation, compatibility and critical paths add error cases, concurrency and the necessary end-to-end tests.
   The levels are test-selection suggestions; several risks can coexist; they are not a quality score or a mechanical add-more-tests package.
3. **Write expectations that can be judged true or false first.** Use [Assertions and fixtures](references/assertions-and-fixtures.md) to verify business results, boundaries, errors and side effects;
   a mock only isolates external dependencies and must not let the test bypass the behaviour under test.
   A defect regression confirms failure from the target symptom before the fix and a pass after it;
   other tests prove their value through contracts, properties or known boundaries, without manufacturing an error for every test.
4. **Arrange order and resources.** Verify the run entry point/candidate and fixtures first, then run the cheap, highly discriminating slices;
   independent shards may run in parallel within approved resources.
   With multiple executors or a shared environment, read [Sharding and recovery](references/parallel-execution.md); do not shard by file count alone.
5. **Execute and keep the results.** Record the first run and reruns; triage failures into product, fixture, environment and contract first; one blocked shard does not stop independent shards.
   Not run cannot count as passed; N/A needs an applicability reason; a test framework skip does not map to N/A automatically.
6. **Retest by impact and deliver.** When the candidate, acceptance or fixtures change, state which evidence is invalidated and retest the affected slices and adjacent risks.
   Use the [test plan fragment](assets/test-plan.md) to record scope, basis, estimates, limitations and result references;
   completion judgement goes to `verification-gate` or the project's existing equivalent rules.

## Scope boundaries

Day-to-day changes get relevant checks and regression; do not automatically require TDD for every change, deleting an existing implementation to rewrite it, or a full suite per task.
The complete release full suite is scheduled only after the user has stated go-live preparation, the candidate is pinned and the corresponding prerequisites are met;
the ordering is `release-readiness` consuming this strategy.
A partial green cannot be renamed a full suite, and this skill cannot be used to start real external tests.

If the chosen layer cannot observe the risk, add one layer rather than piling up assertions of the same kind.
For example, a local function paginating correctly does not prove the proxy preserves the cursor; adding a boundary contract test is enough, and a whole-site E2E is not necessarily needed.

## Results and recovery

For the meaning of the status words `PASSED`/`FAILED`/`BLOCKED`/`N/A` and "not run", see `verification-gate`. Record the reason for items not yet started.
State product pass and fixture pass separately.

When an execution with side effects is interrupted, check handles and results first; do not restart the same data write while in-flight work is unknown.
A first failure followed by a pass still keeps the flakiness information; converge the conclusion only after a clear explanation, an isolating condition or fix evidence.
When the complete result is not visible, keep it unverified; exit 0 or a subtask's one-line "passed" is not full coverage.

## Resource suggestions

Existing deterministic cases may use low/low; key assertions and isolation design normal/high; grade words map to actual execution configuration through the project resource mapping.
Shard by the host limits given by project configuration, such as executors, concurrency quota and machines/environments.
Estimates include preparation, queueing, acceptance and necessary retests; actual values go back to project records; do not hard-code models, head counts or average durations.

## Sources

1. Pinned sources: [SP05 test-driven-development](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/test-driven-development/SKILL.md), [SP06 verification-before-completion](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/verification-before-completion/SKILL.md).
2. From SP05, adopted observable behaviour, failing for the right reason and minimal regression; from SP06, adopted binding conclusions to execution evidence.
   Risk levels, impact propagation, isolation and result semantics are own-authored for this package.
   Dropped TDD for every change, deleting implementations to rewrite, a full suite per task, mandatory rerun on every statement and the absolutism that "partial evidence has no value".
3. License: shipped with the package as [LICENSE-SP.txt](LICENSE-SP.txt) (SP, MIT; both sources belong to obra/superpowers);
   library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license file along when copying this package alone.
