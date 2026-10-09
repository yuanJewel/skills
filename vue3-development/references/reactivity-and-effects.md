# Reactivity and side effects

## State and derivation

List state sources, writers and lifecycles first: the server result is not the edit draft, and the URL filter is no longer silently overwritten by another copy in a store.
ref suits values that are replaced; do not casually break read tracking of a reactive object with plain destructuring.
When destructuring is needed, verify the project's Vue version and toRefs/toRef usage; do not assume an older version supports the newer compiler's reactive props destructure.
computed only derives; it sends no requests and does not modify source values.

watch observes an explicit getter/ref; when watching the route, observe only the parameters that change the request, and avoid deep-watching the whole route, which causes duplicate loads.
watchEffect automatically collects only dependencies read during the synchronous phase; reads after the first await cannot be relied on as automatically tracked dependencies.
For an expensive deep watch, find the fields that actually change first.

## Async reads: an old response must not overwrite new state

Below is a Vue 3 Composition API example that uses the onCleanup provided by the watch callback and does not depend on the newer onWatcherCleanup.
`input` is a ref and `read` is a read function injected by the project; it must honour the passed signal or allow the result to be discarded.
The watcher is created synchronously inside the component setup/effect scope; when it is created outside a scope, the caller must keep stop and release it. Cancellation only saves resources.

**The guarantee that an old response does not overwrite new state is the `active` check: even if the service ignores cancellation, a callback whose `active` is false does not write state.**

```js
import { ref, watch } from 'vue'

export function useLatestResource(input, read) {
  const data = ref(null)
  const error = ref(null)
  const loading = ref(false)
  const stop = watch(input, async (key, _previous, onCleanup) => {
    let active = true
    const controller = new AbortController()
    onCleanup(() => { active = false; controller.abort() })
    error.value = null
    data.value = null
    loading.value = key !== ''
    if (key === '') return
    try {
      const value = await read(key, { signal: controller.signal })
      if (active) data.value = value
    } catch (cause) {
      if (active) error.value = cause
    } finally {
      if (active) loading.value = false
    }
  }, { immediate: true })
  return { data, error, loading, stop }
}
```

The example chooses to clear old data as soon as the filter switches;
if the product requires keeping old data, add an explicit refreshing/old-filter marker so the old list does not appear to belong to the new filter.
Error objects are mapped to safe copy at the boundary and are not serialised directly to the user.
If an active cancellation has no follow-up request, the caller must define the idle state after cancellation; stop only guarantees stopping and cleanup and does not promise to reset the returned refs.

Regression observes at least: A then B, with B completing first and A arriving late; a late failure of A must not clear B's loading; switching to an empty filter;
neither success nor failure updates after unmount; the current request can be retried after failure. Verifying only the order of successes is not enough to prove finally is race-free.

## Lifecycle and writes

The creator of timers, event listeners, subscriptions and standalone watchers owns their cleanup. Cleanup unregisters the same function reference;
resources established asynchronously must handle the "created only after unmount" case, not just clean up a handle that does not yet exist in onUnmounted.
SSR paths do not access window/document at module top level.

A save is a command; "just discard the old result" cannot be reused as a guarantee that the server write was cancelled.
After the click, set pending synchronously and capture this submission's draft and object identity; when the service may already have written, do not retry blindly.
Component unmount only prevents local updates; the result must be recovered through the server-side operation identity.
Idempotency, conflict versions and unknown-result handling follow the API contract.

Counterexample: registering cleanup only after an await inside watch; calling abort alone while ignoring that the old Promise still completes;
an old request's finally setting the new request's loading to false; creating an uncleaned timer on every render.
