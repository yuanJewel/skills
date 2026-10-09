# Pinia and composable testing

## Choose real versus stub

| Goal | Setup | What the assertion can prove |
| --- | --- | --- |
| Component should call an action | @pinia/testing present: stubbed action; else spy on the existing real Pinia or mock the service | Call count, arguments, component feedback; not action internals |
| Store state transitions/error recovery | createPinia per case, setActivePinia or pass pinia explicitly; real action, mock external I/O | The real store logic is correct within the stub boundary |
| Component and store working together | Real action (stubActions:false with the testing plugin), mock I/O outside the permitted boundary | The interplay; still not the real backend |
| Plugin extension behaviour | Install it on the test app per the current Pinia version, then use the store | The plugin really takes part; setActivePinia alone does not guarantee it is installed |

Do not assume createTestingPinia is available; when it is, choose stubActions explicitly and provide createSpy: vi.fn in projects that need spies.
initialState is organised by store ID; a component name cannot be the key. A stub's return value must be the contract's Promise/value/error; do not let the default undefined pass as success by chance.
With a real createPinia, use vi.spyOn to replace only the relevant action; when the spy returns a Promise, keep it consistent with the component's await contract.

Create an independent Pinia per case; restore spies/mocks when the test ends and do not reuse the previous case's store.
Widen the fixture scope only when there is clearly no mutable shared state and the lifecycle is controlled.
Patch a mocked module at the import boundary the caller actually uses, and mind Vitest's mock hoisting rules; do not access closure variables that are initialised only later.
Module caches/module-level stores may survive across cases; fix the setup boundary first and do not abuse resetModules to cover up a singleton design.

## Composable lifecycle

A pure-computation composable can be called directly and its public return asserted.
A function that uses watch/effectScope without component hooks can be placed in an effectScope and stopped at the end;
when it uses onMounted/onUnmounted/inject, create it inside setup through a minimal host component and install the actual provider. effectScope itself does not simulate component mounted/unmounted.

Steps: prepare the provider/synthetic read function -> mount the host -> drive public parameters -> resolve/advance timers by source
-> assert refs/events/external side effects -> unmount -> let delayed callbacks complete and confirm no work continues.
The creator of a returned resource states the cancel/release responsibility; the case where a delayed resource is created only after unmount must be handled too.

For timers/subscriptions, count the register/unregister pairing of the real injected functions;
for late requests, look at the result matching the latest parameters instead of peeking at a private request sequence number.
A cancellation test checks both that the dependency received the signal and that the late result is ignored; signal.aborted cannot be equated with the server undoing a write.

## Examples and failure recovery

Normal example: the component test stubs the save action and asserts the submit payload and the failure message;
the store test uses the real save action, simulates a 409 and asserts the draft and conflict state; a browser case separately verifies dialog focus.

Counterexample: createTestingPinia with default stubActions while asserting the cache was really written; all cases using the same Pinia so that they pass only when run alone;
calling onMounted in an effectScope and then claiming it mounted; removing the plugin under test to get rid of an injection error.

For a missing injection, fix the test app/provider first; for an unsettled Promise, confirm the stub's return and the call first; for shared pollution, verify ownership and cleanup first.
Without the plugin, continue on the existing serial/real Pinia path; when a real dependency is outside the allowed scope, record it as unverified and do not connect to a live service ad hoc.
