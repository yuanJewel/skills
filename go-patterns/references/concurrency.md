# Bounded concurrency and exit

## Is concurrency needed

First estimate whether tasks are independent, whether the bottleneck is I/O or CPU, and whether order affects the result.
If a synchronous implementation meets latency, do not add goroutines.
When concurrency is needed, define the maximum active count, queue capacity, overflow policy and upstream backpressure; "one goroutine per item" is not bounded concurrency.

`errgroup` may be used when an existing dependency includes it and its version supports the required API; if absent, do not install it automatically.
The standard-library WaitGroup only waits; it does not propagate errors, cancel tasks or limit concurrency, so the caller designs those semantics.
Do not adopt source examples that lack a cancellation branch.

## Contract for each goroutine

Fill one line: starter -> input/output -> blocking points -> exit signal -> who closes -> who waits -> how failures are returned.
Check every `send/receive/lock/I/O`; ctx cancellation cannot interrupt arbitrary I/O that is not ctx-aware.
Both an upstream that stops producing and a downstream that stops reading must allow termination.

```go
// Fragment: shows only the cancellation boundary of a send; the outer owner must still wait for the task to exit.
select {
case out <- result:
case <-ctx.Done():
    return ctx.Err()
}
```

When the send case is ready, it may send one last item even if ctx is cancelled at the same time.
If the contract requires absolutely no side effects after cancellation, it needs atomic state or authoritative-side validation; this select alone is not enough.
A bounded buffer only postpones blocking; it does not prove exit.
Send failures or upstream errors must deliver a final state to the consumer; do not return a channel that nobody will ever close.

A typical flow: the producer closes jobs; workers only consume and send results; the coordinator waits for all workers and then closes results; the consumer drains it.
A receiver must not close a channel while senders are still running.
On cancel-on-first-error, still wait for all workers; if the consumer exits early, worker sends must be cancellable.
If the cancellation signal cannot reach the underlying call, mark it explicitly as still in flight; do not claim resources were released.

## Shared state and ownership

- If work can be partitioned, each worker writes its own result slot and the coordinator reads after waiting.
  A fixed-length slice with non-overlapping indexes still does not make shared objects inside the slots safe.
- A mutex protects the whole invariant, not a single field.
  Holding an old pointer after a copy, iterating a map outside the lock, or a read-modify-write across two mismatched locks can all race.
- Atomics suit single-variable state or a deliberately designed protocol; multiple atomic fields do not automatically form a transaction.
- Channels are for handoff/coordination and mutexes for shared state; choose by semantics, and do not treat the slogan as a ban on sharing memory.

Verify loop-variable capture against the project's language version.
When old semantics must remain compatible, pass the value into the goroutine as a parameter rather than assuming every module uses the newer range semantics.
`WaitGroup.Add` must happen before the task can be observed by Wait; the common pattern is Add before starting the goroutine and defer Done inside it.

## Shutdown and failure recovery

The service owner stops accepting new tasks -> signals existing tasks to cancel or drain -> waits -> closes dependencies.
Closing dependencies too early makes normal wrap-up fail; closing only the queue while producers remain causes a panic.
When the shutdown deadline expires, report which tasks have not terminated and the next step; do not treat the timeout as normal completion.
The exit policy belongs to the task; generic helpers must not call `log.Fatal`, which skips all defers.

Before retrying after an error, judge side effects and idempotency; cancellation/timeout does not mean "the remote side certainly did not execute".
With shared external state, query/reconcile first, then recover within the approved scope.

## Verification path

Use controllable channels/barriers so the task actually reaches its waiting state, then cancel and assert within a bounded deadline that the owner receives completion; do not use `time.Sleep` to guess that a step has run.
Cover zero tasks, one failure, full queue, consumer exit, repeated cancellation and slow I/O.
Run the race detector over shared state within the applicable scope; no race report only proves none was observed in this run, not that no path races.
Keep the command, version, timeout, exit code and actual coverage.

Normal: bounded workers exit via cancellation-aware I/O and sends, and the coordinator closes results after waiting.
Counter-example: one worker has failed while other tasks are still blocked, and the caller immediately returns "all cancelled"; it must keep waiting or report in-flight work.
