# Checkpoints: what to save, when to refresh, how to verify

Used to organise state before phase delivery and context recovery. A checkpoint is a snapshot of currently recoverable facts; the plan body, approval originals and raw evidence keep their own authoritative locations, and history is not copied again.

## 1. Refresh on changes in the work

| Trigger | Save focus | Afterwards |
| --- | --- | --- |
| Phase result reaches reviewable state | Results, verification coverage, open items, next-phase dependencies | Phase completion does not auto-approve the next phase; continue when existing authorisation covers it. |
| Effective approval, candidate content or file writer changes | New content identity, approval scope, which old conclusions lapse | Keep the original approval; current status points to the new applicable relation. |
| Long operation/subtask starts or a key state changes | Stable task, execution handle, write scope, actual resource occupancy | Reference existing dispatch status directly, do not create another task ledger; after a failed start still check for residual execution. |
| User requests handover or pause, or available context is clearly insufficient | Goal, constraints that must not be lost, in-flight work and continuation entry | Stop/hand over per the actual request; saving is not stopping. |
| Execution-channel failure, request rejection or after recovery | Last proven result, whether the action was accepted/executed, unknowns | Recover via the takeover topic; do not assume the last operation before failure did not happen. |

Do not force closure by calendar, fixed round count or fixed hours. If a phase clearly deviates from expected duration, update reason, remaining work and range; ask the user to decide only when existing scope/budget is exceeded or a real choice exists, and do not reset accumulated totals with a new session. Logging every tool call has no value; record the changes sufficient to avoid loss, redo or double writes.

## 2. How one refresh is done

1. Read the current status's revision identifier, sole writer and latest takeover record; confirm you still hold write permission for this file. Several sessions seeing the same role name does not make them all writers.
2. Preserve the effective goal, phase/stable task ID, approval entry and version. Separate suggestions from formal decisions; a summary must not supply an approval that never happened.
3. Verify this phase's real results: reachable location, exact file or content identifier, modification result, verification object and coverage; write unfinished and unverified separately. For failed commands keep error codes/fragments relevant to diagnosis; do not copy secrets or whole outputs.
4. For every parent/child session, tool or command that may be executing, record last observation, write scope, state and occupancy. Mark unknown without a complete observation; business "awaiting answer/blocked/submitted" does not replace an execution final state.
5. Write one directly executable next step and its prerequisites; list conflicting scope separately, and separately list authorised non-conflicting work. A successor should be able to tell "read evidence" from "re-run operation".
6. Update current facts and checkpoint identifier in the existing status, then re-read to verify content, links and writer. If an external modification is found while writing, do not overwrite it; keep your own candidate at an approved location and resolve the write-seat conflict. Without an approved fallback location, state in the reply that the save is incomplete.
7. Before refreshing the user workbench, confirm the current decision is saved at its authoritative destination and readable. Remove handled items only after confirmed success; on save failure keep the unsaved state and say so — never delete the only record first.

The plan envelope only locates the body; the status template is a contract of meaning, not a mandatory column set. When the project already has equivalent sections, map onto them; do not create `handoff.md`, a status JSON or a second plan. Split into topics per project convention only when a single status can no longer clearly verify task, child executions and evidence; the status stays the single entry, and the whole directory tree is not kept permanently loaded.

## 3. Header-first, then section evidence reading

When a subtask receipt exists, use its fixed header per the `subtask-dispatch` receipt contract: status, summary, section locators, results and content identity first. The header only tells you where to read next; its "done" cannot sign off acceptance. Check file size and structure before reading; limit lines and output bytes together per read; take long tables or single-line JSON by field, and never infer small size from a low line count.

Read originals according to the assertions the next step depends on: for approvals verify the original approval and its scope; for pass conclusions verify candidate identity and check output; for stop-writing verify all related executions. When a link is broken, search the known project for the moved location by stable identity and index; if not found record a gap, do not guess a similar file. Line numbers drift with revisions: verify content identity first, then locate by section name/anchor; without content identity read the current content and mark the old locator as pending verification.

Handle three kinds of reading problem separately: information never saved — go back to the source for minimal evidence; saved but missed — locate the necessary section; too much read — keep originals, narrow retrieval and return scope. For scattered material add entry pointers rather than rebuilding a full copy. Read key tool/API parameters from the current tool contract; a handover summary does not rewrite or guess the call schema.

## 4. Request or context failures

"Request too large", 413 or similar wording alone cannot tell which layer failed, still less that the old task stopped. Preserve existing results and the last action handle first, then distinguish: local client rejection, execution channel/gateway body limit, model context/output limit, tool output or attachment limit; if indistinguishable, write "to be located".

Record minimal evidence only when diagnosis needs it and access is permitted: error text and time, request/response correlation ID, whether it occurred before sending or after acceptance, relevant byte/token/attachment metrics with units. Avoid reading credentials, full private requests or configuration to assemble evidence. Query action state through the old handle; while state is unknown, never blindly retry calls that may have side effects.

Any threshold statement carries at least the applicability conditions below, stored in the project capability record or existing evidence, never as a constant of this package:

| Item | Required evidence |
| --- | --- |
| Limited object | Request body bytes, single attachment, input/output tokens or another object; units are not interchangeable. |
| Execution environment | Host/client and relevant versions, execution channel, model; when only request configuration is visible, distinguish requested from effective. |
| Source and date | Official limit or actual observation, verification date, concrete evidence entry and test conditions. |
| Conclusion scope | "This sample passed", "this size failed" or a proven boundary; one success does not prove no upper limit. |

Prefer trimming unnecessary output, reading by section and referencing stored originals. If compaction or a session switch is really needed, complete the checkpoint first and operate per available host capability and the user's existing authorisation; without the capability, give the shortest manual continuation action, never pretending compaction or session creation already happened. Do not change accounts, switch execution channels, tune gateways or auto-install hooks to get around a failure. For failures that cannot be located, report what was ruled out and the next minimal check; do not resend the same thing repeatedly.

## 5. Continuation self-check and counterexamples

Try to answer from the checkpoint: where are the goal and approval; which copy is the current result; which conclusion applies only to old content; who else may write; which occupancy could not be released; what are the next step and its failure recovery. If an answer depends on the author's memory alone, add that one evidence entry. This check is not independent review and does not prove unsampled content correct.

| Input scene | Expected judgment |
| --- | --- |
| Three-module implementation phase ends, two modules pass, one not yet verified | Status lists actual coverage and gaps separately; next phase starts from the unverified item and its dependencies; never write "all done". |
| Only midnight passed, phase work continues | Keep the same task and totals, refresh on substantive change; no daily plan, no re-authorisation. |
| Summary says approved, original contains only the author's suggestion | Record suggestion and approval gap; approved design may complete, implementation depending on that approval does not start. |
| Receipt header claims pass, file content has changed | Old conclusion applies only to the old candidate; re-verify affected results, do not treat the summary as new evidence. |
| Execution channel reports request too large, but the background command has a handle | Record channel failure and execution liveness as two problems; query the handle, do not assert the command died or a fixed gateway limit. |
