---
name: pytest-patterns
description: Write, review and diagnose Python pytest cases, handling fixture lifecycle, parametrization, mocks, async and parallel isolation. Use for a defined testing task; do not convert every Python script to pytest, and do not install plugins automatically.
metadata:
  version: "0.1.0"
---

# pytest testing method

Write the contract under test as independent expectations first, then choose fixtures, parametrization and stubs; test count and coverage are no substitute for behavioural correctness.

## Inputs and capability

Take the target module/behaviour, allowed files and external boundaries, the actual Python/pytest/plugin versions,
the existing test entry, async mode, fixture ownership, node resources and how results are counted.
Without pytest, cases can be written and separable standard-library logic executed, but this cannot be called a pytest pass;
without pytest-mock use unittest.mock/monkeypatch, without xdist run serially, and install neither automatically.

Without an async plugin, do not treat a bare async def as executed: being collected or skipped does not prove the function body ran.
With no plugin and a test that fully owns its event loop, asyncio.run may be used inside an ordinary test;
with loop-bound fixtures or an existing async framework, settle the compatible mode first and do not start a nested event loop.

## Method routing

1. Write input, action, output/error/side effect, and parametrize with explicit expectations and readable IDs.
   A counterexample must be able to expose the target defect; do not fix assertions to fit a wrong implementation.
2. Follow [Fixtures and async](references/fixtures-and-async.md) to decide scope, resource acquisition/release, patch boundary, async mode and cancellation.
   Use existing fixtures where possible; do not build a large autouse fixture for uniformity.
3. For external integration or parallel runs, follow [Parallelism and integration](references/parallel-integration.md) for independent data, worker/attempt identity and cleanup;
   external calls run only in a permitted isolated environment.
4. Run the affected cases first and confirm the actually collected set, that the test bodies executed and the final state of cleanup; run related regressions afterwards when needed.
   Record failed/error/skip/xfail/xpass/not run; exit code 0 cannot stand in for all expectations passing.
5. Use [pytest evidence](assets/pytest-evidence.md) to deliver scope, versions, plugins, original failures and re-verification;
   do not rerun unrelated tests or push TDD/coverage thresholds without need.

## Failure and continuation

Tell apart collection, fixture setup, test call and teardown. A setup failure may not have reached yield yet; resources already acquired successfully must be released.
Keep both assertion failures and cleanup failures; a teardown failure must not overwrite the first business error.
An unavailable dependency blocks only the corresponding integration; pure-logic checks may continue.

On continuation, verify the candidate, selected set, execution handles, exclusive resources and completed results; do not assume the old process has stopped.
When resources are insufficient, change concurrency first; do not skip required cases.

Resource suggestion: mechanical execution uses `low/low`; routine fixtures/parametrization use `normal/medium`; event loop, shared state and concurrency failures use `normal/high`.
Grade words map to actual execution configuration through the project resource mapping.

Normal example: tmp_path per case, the real function under test, a stub at the HTTP boundary; without xdist, run the same set serially.
Counterexample: the whole suite sharing a fixed temp.txt, counting a skipped async test as passed, rerunning until green and then deleting the first-run failure.

**Wrap-up cleanup**: processes, containers, temporary files and test data started outside fixtures are reclaimed after the session ends;
built-in temporary directories such as `tmp_path` follow pytest's own retention policy, and the global basetemp is not cleaned by hand.
Follow the local resource cleanup rule of `task-implementation`: register identity on creation, reclaim only objects registered this run at wrap-up,
write evidence to be kept and cleanup failures into the receipt, and use no global cleanup commands.

## Sources

1. Pinned source: [EC08 python-testing](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/skills/python-testing/SKILL.md).
2. Adopted the fixture/yield, parametrization, mock/autospec, async and temporary-resource topics;
   cleanup on setup failure, the strict/auto distinction, worker isolation and the no-plugin path are own-authored for this package.
   Dropped mandatory TDD for every task, fixed coverage, shared temporary files, automatic plugin installation and undeclared external calls.
3. License: shipped with the package as [LICENSE-EC.txt](LICENSE-EC.txt) (EC, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license file along when copying this package alone.
