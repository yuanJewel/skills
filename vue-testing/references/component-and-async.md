# Components, async and DOM boundaries

## mount and the observation surface

Drive with props, form input, clicks and child events; assert DOM text/state, emit payloads and service call results.
shallow is chosen to replace unrelated subtrees, not as a general default: if the fault depends on parent-child events, slots or a real form component, keep the relevant subtree.
A stub must fulfil the props/events/slots that are depended on; an empty stub cannot prove its validation or accessibility.

wrapper.vm may be used for a narrow assertion, with the reason stated, when no reasonable public observation surface exists; prefer testing the public composable/store.
Snapshots only assist with structural change and cannot replace error, permission and side-effect assertions.
Select by semantics or a stable test identifier; jsdom computes no real layout, so a style attribute or isVisible cannot prove actual occlusion, focus traversal or rendered geometry.

## Wait by async source

| What to wait for | Control method | Insufficient practice |
| --- | --- | --- |
| Vue DOM update | await trigger/setValue, or nextTick after changing props/state | Reading the DOM immediately after writing state |
| Service Promise | A deferred whose resolve/reject is controllable; after completion flushPromises, then verify the DOM | Only nextTick and expecting the network to be done |
| Debounce/retry timer | Advance the existing fake timer to the contract time, then wait for the related Promise/Vue update | A fixed sleep, or an unbounded runAllTimers that swallows loops |
| async setup/Suspense | Wrap in a real Suspense, give the dependency a completion condition, check fallback -> content | Mounting the async component alone and assuming it rendered |
| Browser-specific behaviour | Verify the same candidate in a real browser | Treating jsdom as a browser |

flushPromises does not complete an unresolved Promise, does not advance future timers, and does not prove the service was called.
When using fake timers, verify the current Vitest version and the scheduling source flushPromises uses, so that flush does not wait forever once timers are mocked.
Mock only the clocks needed; resolve the dependency first, then advance the corresponding queue.

The example below assumes the project provides SaveForm, which receives a `save` that returns a Promise;
it disables the save button during submission, emits saved on success, and on failure shows an alert and keeps the input.
Adjust names and selectors to the actual interface; do not change the product contract based on the example.
The code must run in an existing Vitest/VTU/Vue environment; with dependencies missing, only syntax and the deferred can be verified, which does not count as a framework pass.

```js
import { expect, it, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import SaveForm from './SaveForm.vue'

function deferred() {
  let resolve, reject
  const promise = new Promise((yes, no) => { resolve = yes; reject = no })
  return { promise, resolve, reject }
}

it('does not submit twice while saving and keeps the input after failure', async () => {
  const pending = deferred()
  const save = vi.fn(() => pending.promise)
  const wrapper = mount(SaveForm, { props: { save } })
  try {
    await wrapper.get('input[name="title"]').setValue('Synthetic title')
    await wrapper.get('form').trigger('submit')
    await wrapper.get('form').trigger('submit')
    expect(save).toHaveBeenCalledTimes(1)
    expect(wrapper.get('button[type="submit"]').attributes('disabled')).toBeDefined()
    pending.reject(new Error('synthetic failure'))
    await flushPromises()
    expect(wrapper.get('[role="alert"]').text()).toContain('Save failed')
    expect(wrapper.get('input[name="title"]').element.value).toBe('Synthetic title')
    expect(wrapper.emitted('saved')).toBeUndefined()
  } finally {
    wrapper.unmount()
  }
})
```

Duplicate submission of the same handler must be tested through multiple valid entry points, not only by clicking an already disabled button.
Split success and failure into cases with independent expectations; a late-response test completes two deferreds in reverse order and verifies that the old finally does not close the new loading.
An unmount test must also let pending complete and observe no update/no leftover listener; unmount not throwing is not enough on its own.

## Teleport and accessible interaction

When a real Teleport is needed, create a target unique to this case before mounting, attach it to a known container, and query the actual target content;
at the end unmount first, then remove the nodes this case owns. A test using a teleport stub proves only local content/events, not cross-container focus/stacking behaviour.
Assert Suspense's fallback, success and failure paths separately per the contract; do not let the test finish by swallowing exceptions globally.

Test inputs must distinguish loading, error, empty, readonly and permission; hidden/disabled tests also verify that no write call is made.
Time input/display follows the project's wall-clock or absolute-instant contract; inject the clock and change the test timezone rather than depending on the development machine's settings.
