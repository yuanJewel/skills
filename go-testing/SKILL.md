---
name: go-testing
description: Write, review or diagnose Go tests, choosing table-driven tests, stubs, httptest, concurrency, fuzzing and isolated integration verification by public behaviour. Existing healthy tests are not rewritten because the skill is used, and coverage does not replace fault-detection power.
metadata:
  version: "0.1.0"
---

# Go behaviour tests

Inputs: this change's acceptance and risks, affected public boundaries, independent expectations, Go and test-dependency versions, allowed environments, resource and concurrency constraints, and existing tests.
Without an explicit expectation, find the contract first; never compute want from the return value of the function under test.
Ordinary low-risk text or mechanical changes do not get forced tests.

## Choose the method by risk

- Inputs, outputs, errors and HTTP contracts: read [Unit and contract](references/unit-and-contract.md).
  First verify observable behaviour at the smallest stable layer, then choose table-driven or separate cases.
- Cancellation, shared state, order sensitivity, parsers or performance: read [Concurrency, fuzzing and measurement](references/concurrency-and-fuzz.md).
  These tools are enabled by risk; do not add race/fuzz/benchmark to every test by default.
- Databases, time, external protocols and shared resources: read [Integration isolation](references/integration-isolation.md).
  Distinguish what stubs cover from real implementation semantics; use only authorised synthetic environments.
- Delivery: use [Test evidence](assets/test-evidence.md); raw logs stay in the consuming project, and the status must not just say "go test passed".

## Procedure

1. List normal and failure boundaries for new or changed behaviour: choose nil/empty, no permission, conflict, cancellation or recovery by actual risk.
   Reuse valid existing cases; do not rewrite them all because an internal function was refactored.
2. First write the independent oracle, the required fixtures and which faults the test can detect.
   A defect regression runs before the fix and is confirmed to fail for the target fault, then passes on the fixed version; if the old version cannot run, state the gap rather than manufacturing a red history.
   Cases without a known fault may verify detection power via counter-examples, assertion review or isolated fault injection; not every test must be made red first.
3. Create synthetic fixtures with an explicit lifecycle.
   Add no framework when the standard library suffices; follow project conventions for existing frameworks.
   A missing version or dependency blocks only the affected tests; do not install or upgrade to make them pass.
4. Start from the smallest affected package and widen by risk.
   Record the packages run, filters, build tags, version, actual command, timeout, exit code, and run and skipped items.
   Explain separately: zero tests matched, compile failure, timeout and cached results.
5. On failure, first preserve the seed/order/input/logs, then distinguish implementation, oracle, fixture or environment.
   Do not auto-rewrite golden files, delete flaky tests or loosen assertions to get green.
   After a fix, rerun the affected part; repeat wider tests only for new evidence or risk.
6. Report the actual final state: passed, failed, blocked/not run, not applicable.
   Skipped integration tests do not count as passed; list cleanup failures and leftovers separately.
   On a process timeout, first confirm whether test child processes have terminated; interrupted output is not the end.

Normal example: fixing a pagination bug with empty results, use the contract-defined empty array and cursor expectation to prove the old version fails and the new one passes; no need to raise repository-wide coverage.
Misuse example: the mock always returns success and the test only asserts err is nil, so it cannot detect real error mapping; add a failing stub and assert the code and side effects.

Mechanical command/result tidying may use low/low; ordinary test design uses normal/medium; concurrency, authorisation, time or conflicting independent expectations use normal/high.
Grade words map to actual execution configuration through the project resource mapping. Allocate concurrency quota by isolated resources, not by number of cases.

**Wrap-up cleanup**: child processes, listening ports, containers, temporary directories and test databases/namespaces started by tests are reclaimed after the tests end; external resources not covered by `t.Cleanup`/`TempDir` are registered separately.
Follow the local resource cleanup rule of `task-implementation`: register identity on creation, reclaim only objects registered by this run at wrap-up, write retained evidence and cleanup failures into the receipt, and use no global cleanup commands.

## Sources

1. Pinned source: [EC05 golang-testing](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/skills/golang-testing/SKILL.md).
2. Adopted table-driven tests, cleanup, httptest and the race/fuzz/benchmark layering; isolation, clock/time zone, result summary and detection-power boundaries are own-authored for this package.
   Dropped fixed coverage targets, mandatory red-green for every case, automatic golden updates and assertion-free examples. Before upgrading testing APIs, verify the minimum toolchain.
3. License: shipped with the package as [LICENSE-EC.txt](LICENSE-EC.txt) (EC, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license file along when copying this package alone.
