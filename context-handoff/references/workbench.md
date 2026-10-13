# User workbench

Read this page before creating or refreshing the user page. Use [the template](../assets/user-update.md) for its shape; this page is the rule authority.

## 1. Fixed shape and version

Use `# User workbench — {{current_development_version}}`, followed by `Updated: {{date_time_timezone}}`.
Keep these four sections in this order: `Q Waiting on you`, `N In progress`, `P Scheduled`, `E Ended this cycle`.
Keep the letters when localising titles. Write `None` in an empty section; never remove its heading.
The update line contains only time, with no commit, version-source explanation or Git state.
Read the current development version from the project's declared version source on every refresh; do not infer it from a changelog, tag or memory.
Missing version source -> write `Version unknown` in the title and add a Q item explaining what the user must resolve.
A cycle runs from that development version's start to its close-out.
Do not add entry or continuation sections; the material root's README holds the reading entry.
A necessary user-forwarded handover is a Q operation, using the project's collaboration contract.

## 2. Task states and requirement labels

The project task register is the state authority; the workbench maps it rather than keeping the only record.

| State | Meaning | Workbench position |
| --- | --- | --- |
| backlog | Registered for later, outside this cycle | Count only at the end of P, with the register link |
| scheduled | Planned for this cycle, no stage started | P |
| started | Any stage has begun, including waiting for user acceptance and close-out after acceptance | N |
| ended | User accepted and close-out is complete, or user cancelled (label `cancelled`) | E |

States move forward. Record a reason in the task register before any regression, such as reopening an ended task; then display its new state.
A task waiting for user acceptance remains in N with stage `Awaiting acceptance` and also gets a Q acceptance item.
After acceptance, keep the task in N at stage `Close-out` until close-out is complete; then move it to E.
Every Q/N/P/E item carries `[{{requirement_id}}]`, preferably the register's requirement ID; combine IDs as `[R1+R2]` when needed.
Without an ID, use the originating task, such as `[Export review]`.
Unknown origin -> use `[Origin unregistered]` and register that gap in the task register; never invent a source.

## 3. Q Waiting on you

Collect every real user dependency: decisions, result acceptance and manual operations the agent cannot execute.
Number entries Q1, Q2 and so on, and mark the type `Decision`, `Acceptance` or `Operation`.
Do not manufacture approval requests for work already authorised, or demand acceptance when the task does not require it.
Decision items give a recommendation with reasons, real numbered alternatives (1, 2, 3) and an exact choice the user can make by number.
Keep all six decision-basis rows from the template: scope, why now, affected artefacts, verification/recovery, time/resources and consequences.
The user must be able to decide from this page; links provide evidence, not missing reasoning.
Acceptance items give a viewable result entry, pass criteria, verified coverage and limits.
Operation items give the exact action, object and observable result after completion.
After an answer, save the conclusion at its formal decision location and read it back before removing the Q item.
Save failure -> keep the item and explain the gap; never delete the only record first.
After the user reports an operation done, verify its result (for example with read-only commit history) before removing it.
For forwarding, show receiver, purpose and one locating sentence per the project collaboration contract.
Reported sent but entry still pending -> keep Q marked `Forwarded, awaiting reception`; remove only after reception is verified.

## 4. N In progress: stages and commitments

Use columns `Task`, `Stage`, `Executor`, `Committed completion`, `Remaining`.
Stage names follow the project workflow (design, implementation, review, awaiting acceptance, close-out).
Write the executor as `{{responsibility}} · {{tool}}`.
Completion is an absolute date/time in the project's local timezone; read a real clock on refresh to calculate remaining time.
Stages waiting on the user, including a pending decision or acceptance, are untimed: write `Waiting on you: see Q{{n}}` and `—` for remaining.
Where a project collaboration contract exists, follow it for stage negotiation; otherwise the stage executor estimates using `estimation` and records the result in status.
The plan proposes each stage's limit. Before starting, its executor confirms it in status or records a revised limit with reasons; an unconfirmed stage must not start.
A revision that moves total completion later than the plan goes to Q for the user's decision before the dependent stage starts.
When completion will miss its commitment, add a Q decision before the deadline with cause, new estimate and options: extend, split, reduce scope or pause.
Use the calibration method of `estimation`; preserve the original estimate and record the current forecast separately.
Once Q is reported, work may continue past the deadline; reaching the budget triggers a decision, not automatic closure or termination.
After the deadline, retain the original commitment and add `Overdue; new estimate {{time}}; see Q{{n}}` in N.
Record the overrun in the status calibration record for the user to resolve afterwards.
Overdue with no prior Q is a rule violation: any refresher immediately adds Q and marks N `Overdue (not reported in advance)`.

## 5. P Scheduled and E Ended this cycle

P uses columns `Task`, `Next stage and executor`, `Planned start`, `Estimate`, `Dependencies`; include only scheduled tasks.
Sort by planned start, with work starting in the next few days first; keep unknown starts explicit rather than inventing dates.
Estimates are ranges (for example `2–4h`); missing evidence -> `Awaiting estimate`. At stage start, negotiate a commitment per section 4.
End P with `{{count}} backlog items: see {{task_register_link}}`; do not list backlog tasks individually.
Each E item is one line: `{{task}} [{{requirement}}] — {{one_sentence_result}}, {{end_date}}, {{archive_or_result_link}}`.
Include only the current cycle. Clear E during version close-out once the results are retained in the changelog and archive.
Do not put hashes, revision rounds or review finding IDs in E.

## 6. Refresh and writing discipline

Refresh on task-state/stage changes, executor changes, commitment changes or deadlines, Q answers, reports of completed operations, and version changes.
Ordinary Q&A does not refresh the page.
Rebuild the entire page from current facts; do not append to the old page as a log.
One writer holds the workbench, the same integrator as for the current batch.
Write a temporary file in the same directory, read back and verify the full page, then rename it over the old page; never truncate the live page.
Save/read-back failure -> retain the previous page and report the incomplete refresh.
Recycle only this run's temporary files under the local resource cleanup rules of `task-implementation`.
Write for the user's judgment: hashes, candidate identities, revision rounds, finding IDs, file-count checks and resource ledgers stay in status or archive.
Link to those details only when useful to the decision.

## 7. Pre-publish self-check

Run this as the final refresh step, before publishing; do not add the check results to the page.

1. Version came from the declared source; all four headings exist in the right order.
2. Every item has a requirement label; state and section match the task register.
3. Each Q decision is complete enough to decide here; answered items are saved and removed.
4. Every N row has stage, executor and absolute commitment (or an explicit user wait); no overdue row lacks its Q report.
5. Each E item is one line; the whole page has no hashes, revision rounds or internal check counts.

## Counterexamples

- Appending daily tool results keeps obsolete actions alive. Rebuild Q/N/P/E from verified facts instead.
- Putting a commit hash and several review-round IDs in an E result makes the user read an internal ledger. Keep them in status and give the result link.
- Silently moving an overdue N commitment hides the miss. Preserve the original, add Q, mark the overdue state and record calibration.
