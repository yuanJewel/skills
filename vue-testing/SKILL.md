---
name: vue-testing
description: Write, review or diagnose behaviour tests for Vue components, Pinia stores and composables, choosing real or stub boundaries and controlling async. Use for a concrete testing need; real layout, native browser events and end-to-end chains need browser-layer evidence.
metadata:
  version: "0.1.0"
---

# Vue behaviour testing

Determine the behaviour to prove this time first, then choose the narrowest test boundary that can prove it. Keep healthy existing tests; do not rewrite the whole suite for the sake of uniform style.

## Inputs and capability check

Read the target contract, affected components/services, the existing test entry, the actual versions of Vue/Vitest/VTU/Pinia and the DOM environment.
`@pinia/testing` is an optional capability; do not assume it exists or install it automatically.
Without the plugin, use the existing createPinia, a mock at the service boundary, or continue with independent pure-logic checks;
without Vue or the runner, deliver only code/static results and state explicitly that framework execution is unverified.

Record external dependencies and synthetic fixtures, clock/timezone, and the allowed write/cleanup scope.
Lacking real DOM capability does not block logic tests, but cannot prove layout, occlusion or real browser events.
If the requirement's auth conclusion depends on the server, component permission cases can prove only UI behaviour.

## Choose, implement and judge

1. Write input -> action -> observable output plus negative cases; expectations come from the contract and are not copied from the current implementation.
   For components observe DOM/emit/external calls, for stores state/action effects, for composables public refs/return values and lifecycle.
2. For components and async, follow [Components, waiting and DOM boundaries](references/component-and-async.md) to choose mount/stub, nextTick, Promise, timers, Teleport/Suspense.
   Do not append a uniform sleep to every async step.
3. For stores/composables, follow [Pinia and composables](references/pinia-and-composables.md) to make explicit real actions, stubbed actions, plugins and scope.
   After stubbing, only the call is proven; do not claim the action's real side effects pass.
4. Run in the minimal failing scenario; record first-run failure, fix and re-verification separately.
   For the changed path, choose among normal/empty/error/permission/race/unmount; do not force every case to include all boundaries, and do not pad coverage numbers.
5. Use [Test plan and results](assets/vue-test-plan.md) to record the real environment, what the stubs prove, results and the remaining browser/API-layer gaps.
   Not run/skip does not count as passed, and all-green unit tests do not mean the real chain is all green.

## Failure and recovery

For flaky failures, first tell apart Vue updates, service Promises, timers, mount dependencies or resource leaks, then use control points to reproduce reliably.
Do not turn red into green with uniform delays, swallowed exceptions or repeated reruns.
After a failure, still release the wrapper, scope, Teleport target and subscriptions created by this case; restore fake timers/mocks to their original state so the next case is not polluted.

On continuation, first verify the candidate, executed/in-flight work and fixture ownership;
different tests running in parallel share only immutable data and have independent Pinia/DOM/external resources.

Resource suggestion: mechanical execution uses `low/low`; routine test implementation uses `normal/medium`; async races, lifecycle, permission or mixed-version problems use `normal/high`.
Grade words map to actual execution configuration through the project resource mapping; concurrency is subject to host limits such as machine and environment, supplied by project configuration.

Normal example: the test of a component calling the save action stubs the action; a separate store case runs the action for real and mocks HTTP.
Counterexample: asserting "server save succeeded" on a stubbed action; claiming a dialog is unobstructed in a real browser because a jsdom attribute exists.

**Wrap-up cleanup**: dev servers, browser processes, occupied ports and temporary output other than coverage/snapshots, started by tests or previews, are reclaimed at the end.
Follow the local resource cleanup rule of `task-implementation`: register identity on creation, reclaim only objects registered this run at wrap-up,
write evidence to be kept and cleanup failures into the receipt, and use no global cleanup commands.

## Sources

1. Pinned sources: [GH03 unit-test-vue-pinia](https://github.com/github/awesome-copilot/blob/7cce7cfb4b61196c36d7e8eb8475ae84b356b126/skills/unit-test-vue-pinia/SKILL.md), [VUE02 vue-testing-best-practices](https://github.com/vuejs-ai/skills/blob/c9d355ff23f654309dd02006be671859df0a134c/skills/vue-testing-best-practices/SKILL.md) (for VUE02 only the pinned entry was read).
2. From GH03, adopted the narrowest boundary, public behaviour and the real/stub Pinia choice; from VUE02, adopted the topical classification of async/lifecycle/Suspense/Teleport/browser differences.
   Details and missing-capability branches are own-authored for this package.
   Dropped default shallow, installing test plugins and an absolute ban on wrapper.vm.
3. License: shipped with the package as [LICENSE-GH.txt](LICENSE-GH.txt) (GH, MIT), [LICENSE-VUE.txt](LICENSE-VUE.txt) (VUE, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license files along when copying this package alone.
