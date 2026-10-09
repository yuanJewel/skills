# Triggering, queue and callbacks

## Identity before side effects

Create an operation identity and save the approved parameter/artefact/script snapshot, with state pending initiation.
A job's canonical identity includes the local server identity and the full job path; the basename alone is not enough.
After a successful POST, save the queue ID; query its executable, then bind the build number/URL.
Queued is not running; the job's "latest build" cannot stand in for this operation's build.

On initiation timeout/disconnect keep unknown, and query by operation parameters and the saved queue/build.
The Jenkins trigger API must not be assumed idempotent; if there is no evidence whether it happened, do not trigger a second time automatically.
After a restart, resume querying from non-final operations; do not re-render moving inputs or initiate again.

| State | Acceptable facts | Action |
| --- | --- | --- |
| preparing | Identity and snapshot persisted | One controlled initiation |
| submitted/unknown | HTTP sent but the result may be unknown | Query queue/build; keep as in-flight |
| queued | Queue identity trusted and no executable | Record the queue reason; queue cancellation allowed |
| running | Matching build with building=true | Query/receive progress; verify timeout and cancellation |
| cancelling | Cancel intent saved | Send the matching cancel/stop; keep reconciling |
| finished | Matching build ended and the result is determinable | Record success/failed/cancelled per contract and save evidence |

This table is a business state model; it does not pretend Jenkins has fields with all these state names.
An expired/404 queue item or a missing callback does not automatically mean cancelled; verify via the bound build/operation first.
Without a unique match keep pending verification, to avoid attaching to the wrong build.

## Cancellation races

Persist cancel intent first, then determine whether it is still queued or already became a build.
A failed queue cancel may mean it already started; re-query and stop the matching build.
A successful stop request only proves the request was received; still verify the build's final state and downstream resources.
Late running/success callbacks after cancel intent must not overwrite state directly.
The final model must distinguish "cancel request later than actual completion" from "success callback still in the post stage".

Do not forge final results: if cancellation came too late and the build genuinely succeeded, save the actual result and the race explanation of the cancel request per the established contract.
If the business rule says cancel intent takes precedence, keep the business state and the Jenkins result separately.
A final state must not be revived by stale callbacks. Rollback/compensation is a separate action; cancellation does not equal undoing side effects.

## Callbacks and reconciliation

Callback authentication and permissions follow the project contract. The payload associates at least the operation, job, build and event identity/sequence number or verifiable ordering.
Duplicate identical events must be idempotent; reject foreign jobs/builds, stale operations or bad signatures.
Callback URLs may come only from approved configuration; never accept arbitrary user input that would create SSRF.

A post callback is still inside the build lifecycle; a body saying success does not equal building=false.
Reconcile with the matching build's building/result and the business state machine; duplicates/out-of-order events only add allowed facts and never move a final state backwards.
Without a monotonic sequence number use legal state transitions and authoritative queries; do not order by local receive time.

Reconciliation covers restarts, disabled callbacks, a success callback during cancellation, the queue-to-build race and two operations in parallel on the same job.
Result artefacts contain non-secret identities and checksums; the full console may contain sensitive values, so keep only authorised links/redacted excerpts, never a full copy.

Normal: the callback arrives first while the build is still building; keep it pending reconciliation and archive only after a later query shows it finished.
Counter-example: after an HTTP initiation timeout, re-sending twice as "not successful", ending with multiple builds. Recovery should first bind existing facts and mark unknown gaps.
