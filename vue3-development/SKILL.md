---
name: vue3-development
description: Implement or review the state flow, async side effects and interaction states of Vue 3 components, stores and composables. Use for a defined front-end behaviour change; do not refactor the whole front end because a Vue keyword appears, and do not force migration of existing Options API code.
metadata:
  version: "0.1.0"
---

# Vue 3 behaviour development

Locate this change's user action and observable result first, then decide whether to change the component, the state layer or a side effect.
Follow the project's existing Vue/API/routing/UI-library contracts; do not escalate a small change into an architecture rework.

## Inputs and missing items

Take the target behaviour and acceptance, allowed files, the relevant component/API/route/permission contracts,
the actual Vue and UI library versions, the existing state management and test capability.
Without version evidence, avoid version-specific syntax;
when the API's save/clear semantics are missing, settle the interface gap first and do not treat an empty string or a placeholder as the clear value on your own.
Without a runtime environment the state flow can still be reviewed, but browser behaviour cannot be declared passing.

## Choose the smallest change boundary

1. Mark a single source of truth for each piece of data: who owns server data, the local edit draft, the route query and cross-page shared state.
   Use computed for derived values; use watch for side effects that must observe external changes. Details in [Reactivity and side effects](references/reactivity-and-effects.md).
2. Draw the parent-child/API inputs and outputs involved this time, and declare props, events and save results; split only for an independent responsibility or a real reuse need.
   Existing Options API, JS/TS style and directories may stay. See [Component contracts](references/component-contracts.md).
3. Cover read, edit, save, failure and leaving the page along the user path. Late responses, duplicate submits, permission changes, read-only and empty results each have a defined outcome.
   See [Interaction states](references/interaction-states.md).
4. Implement the narrowest change and verify the affected behaviour through the existing check entry; component tests may use `vue-testing`, and browser events/layout need real-browser evidence.
   When no adjacent skill is available, follow the project's tests of the same kind; do not depend on installing the whole library.
5. Use [Component plan and results](assets/component-plan.md) or the existing record to give the changed contracts, states and evidence;
   mark parts not actually run as unverified, and do not call static reading a successful user path.

## Failure, recovery and resources

First distinguish request failure, business rejection, cancellation and stale responses.
On failure keep the retryable input; a permission rejection must not be turned into success automatically, and cancelled/late responses must not overwrite the current state.
When the save response is unknown, first query the result by the interface identity, then decide whether to retry; blind repetition of non-idempotent actions is forbidden.

On interruption, save the input version, candidate files, verified/unverified items and in-flight work; continue after confirming the sole writer.
Parallelise only when files and shared state do not conflict and the budget allows.

Resource suggestion: pure extraction and predefined checks use `low/low`; ordinary component changes use `normal/medium`;
cross-component state races, authorisation or lifecycle problems use `normal/high`. Grade words map to actual execution configuration through the project resource mapping.

Normal example: fix only the out-of-order filter results, keep the page structure, and add cancellation/late-arrival protection plus an observable regression.
Counterexample: only the button label changes, yet the site-wide state library is migrated, a new dependency is installed, or hiding a button stands in for server authorisation.

**Wrap-up cleanup**: local dev servers, watchers and occupied ports started during development are stopped on delivery or abandonment; temporary debug code does not stay in the candidate.
Follow the local resource cleanup rule of `task-implementation`: register identity on creation, reclaim only objects registered this run at wrap-up,
write evidence to be kept and cleanup failures into the receipt, and use no global cleanup commands.

## Sources

1. Pinned source: [VUE01 vue-best-practices](https://github.com/vuejs-ai/skills/blob/c9d355ff23f654309dd02006be671859df0a134c/skills/vue-best-practices/SKILL.md) (only this pinned entry was read; no claim of having read all its attached pages).
2. Adopted the single source of state, props/emits, and the responsibilities of derivation versus side effects; the interaction, request race and recovery examples are own-authored for this package.
   Dropped mandatory four references for every task, fixed component counts, Options API migration and adding a state library.
   After a Vue/UI library upgrade, re-verify by affected syntax and behaviour.
3. License: shipped with the package as [LICENSE-VUE.txt](LICENSE-VUE.txt) (VUE, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license file along when copying this package alone.
