# Collaboration contract

Read this page when several tools, hosts or sessions share one material root, or when main tasks and subtasks must be assigned, received and closed. It defines what `governance/collaboration.md` and each plan's `status.md` must make answerable, and separates responsibility from the tool that happens to fill it.

## 1. Responsibility is not the tool

A responsibility is a role in the work: design, implementation, independent review, acceptance, integration of shared files. A tool or host is whatever session performs it today. Record them in separate columns; never infer a permission from a tool name, and never infer a role from a session being present.

Three project models are supported; the project chooses and records one in `collaboration.md`:

| Model | How roles are decided | Record |
| --- | --- | --- |
| Fixed assignment | The project has confirmed that one party always designs and another always implements | The mapping, who confirmed it, and that task authorisation is still checked per task |
| Per-task assignment | Each task names its designer, implementer, reviewer and acceptance owner, and each one's write scope; roles may swap between tasks | The current task's assignment in its `status.md`; `collaboration.md` records the rule that assignments follow the task, not the tool |
| Single maintainer or default responsibility | One session maintains the root; no role table | The statement that the default responsibility applies and that the mode is set per task |

Per-task assignment allows both directions: A designs and B implements, or B designs and A implements. In every direction the implementer self-tests, the implementation reviewer did not write the reviewed implementation and writes a report only, and fixes go back to the implementer. A designer reviewing the implementation may check conformance to the design but this is not an independent review of the design; if the project requires one, arrange it separately.

Switching session or tool restores the original assignment and approvals; it does not widen write scope. When the final state of a previous writer is unknown, do not take over the conflicting files.

## 2. Writers and write scope

Each file has one writer at a time. `status.md` records, per task: the exact file set each writer may change, the candidate identity being produced, and the hand-back condition. Public files shared across tasks (root `README.md`, indexes, library ledgers) have a sole integrator named for the current batch.

A reviewer never edits the reviewed object. A request to review grants no write permission; a review finding is fixed by the writer of that file.

## 3. Main tasks and subtasks

A main task may split work into subtasks for parallel execution, isolation of unrelated context, or independent review. The project's dispatch and implementation methods (`subtask-dispatch`, `task-implementation`) define briefs and receipts; this contract adds only what the material root must make visible:

- **Identity**: each subtask has a stable identity under its parent (for example `<plan-id>/S3`). A subtask that grows into an independently accepted scope gets its own plan id and the parent records the link.
- **Brief and receipt**: the subtask receives only what it needs; the parent records what was handed out and what came back, including evidence location and leftovers.
- **Reception**: the parent verifies the subtask's result and final state before counting it as done. An external execution whose state is unknown is recorded as unknown, not as handed back.
- **Closing**: a subtask ending does not close the parent; the parent closes when its own scope, verification and acceptance are met. Subtask leftovers (temporary files, scratch directories, half-written candidates) are taken over by the parent.
- **Visibility**: `user.md` maps tasks through the four states; subtasks appear in Q only when they require a user decision or operation. The full subtask table stays in `status.md`.

`governance/retention.yaml` configures the generic close-out conditions (see [Storage and migration section 3](storage-and-migration.md)); `collaboration.md` holds the method; `status.md` holds the facts of one plan.

## 4. Acceptance owner and close-out

Each plan names an acceptance owner in `status.md`. Final acceptance is given by whoever the project contract designates (often the user); the acceptance owner confirms the evidence, confirms all writers have handed back, and then performs the plan archive described in [Canonical layout section 6](canonical-layout.md) as part of completing the plan. An implementation reviewer may hold this responsibility; it does not let them sign the user's final acceptance on the user's behalf.

## 4.1 Task states and stage commitments

The project task register holds the authoritative state: backlog (later, outside this cycle), scheduled (this cycle, not started), started (any stage begun, including user waits and close-out after acceptance), ended (accepted and close-out complete, or cancelled).
`user.md` maps these states under `context-handoff` [Workbench rules](../../context-handoff/references/workbench.md); regression reasons belong in the register.
The plan proposes stage limits; before starting, the executor confirms or revises the limit with reasons in status.
A revision delaying planned total completion goes to Q first. User-wait stages are untimed.
Before a likely miss, report Q with reasons, a new estimate and handling options; reported work may continue, with the original commitment preserved and overrun recorded for later user resolution.
Unreported overdue work is a violation: immediately add Q and mark it as not reported in advance.
Detailed negotiation, deadline display and calibration rules have one authority: `context-handoff` Workbench rules.

## 5. Handing the next step to another agent: entry and locating sentence

When another agent must review an implementation, implement an approved design, archive an accepted plan or fix a finding, write the handover once in the plan's `status.md` Handovers section.
The user forwards only the locating sentence; a bare report link or "hand to the reviewer" cannot locate a complete handover.
Use [the handover entry template](../assets/handover-entry.md).

The nine required fields below define the entry's content; write the actual known values:

1. Project and working directory; the reading entry to open first (root `README.md`, the plan status).
2. Stable task identity (plan id, and subtask id if any).
3. Receiver and mode: which responsibility they take (design, implementation, review, acceptance owner) and in which mode of this package or the project's method.
4. Goal of this step: the question to answer or the result to produce; the approved object or candidate identity it refers to.
5. Exact write scope and its boundaries: files or directories they may change; files they must not touch; whether they write a report only.
6. Inputs and evidence to use, by location: status, decisions, verification files, review report, candidate hash list.
7. Completion and verification conditions: what counts as done; checks to run; what cannot be signed from this seat.
8. Failure and conflict handling: what to do on unknown writer, changed candidate, missing permission; what to pause and what to continue.
9. Receipt location and hand-back: where to record results and the stop-writing statement; who reviews next.

Existing safeguards:

- The locating sentence is a natural-language message for the receiving tool, role and project convention; it supports both directions of assignment (A designs/B implements or the reverse). Give a CLI command only when the actual client and syntax are verified and the user wants one; never guess a tool's command line or require a new session when the existing one can continue.
- Reference existing context by real locators; do not paste the whole history, and write actual values in the entry, not `{{field}}` markers where the value is already known.
- The entry cannot grant more than the current authorisation. When a writer's final state or a preceding acceptance is unknown, the instruction states the pause condition instead of assuming it is met.
- Drafting the entry is not sending it or dispatching the work; the delivery says that the user forwards it. The brief/receipt semantics come from `subtask-dispatch` and the continuation contract from `context-handoff`; this section fixes only what the handover entry must contain.
- When no other agent is needed, deliver normally; do not invent a hand-over, a subtask or a new task to satisfy this rule.

Entry lifecycle and delivery:

1. **Identity**: use `<plan-id>-H<n>`, increasing within the plan, never reusing an ID; one receiver and step per entry. No next step for another agent -> no entry.
2. **Immutable content**: after issue, change no body fields. Amend with a new entry and mark the old one `Void (replaced by <new-id>)`.
   A received entry cannot be voided until handed back or an authorised stop/write-transfer process has completed.
3. **Reception first**: pending -> verify preconditions, mark `Received (<time>)`, confirm the stage limit, then start.
   Void -> follow its replacement. Received or handed back -> do not execute again; stop and report to the user.
   Unmet preconditions (candidate drift, unknown writer) -> do not start; record the cause below the entry and hand back.
4. **Entry control fields and receipt**: the receiver's write scope always includes this entry's State field and its receipt section, even when their result is a report only.
   Field 5 must explicitly list both alongside the result write scope; receiving an entry does not transfer the rest of plan status.
   From reception until hand-back, the original status writer pauses all writes to the entire status file; the receiver writes only this entry's State field and receipt section, and the original writer resumes after hand-back.
   A report-only receiver places any follow-up handover entry inside their receipt section.
   The receiver writes the receipt below the entry, marks `Handed back (<time>)`, then stops writing that scope.
   Coordinate writes to the shared status file; the scope record is not an atomic lock and grants no writes to the reviewed candidate.
5. **Authorisation**: the locating sentence only locates; the entry stays within current authorisation. Drafting is not issue or dispatch; the user forwards it.
6. **Fallback**: unreadable project files (another machine, no access) -> paste the nine fields in full and mark the entry `Switched to pasted delivery`.
7. **Workbench**: put required forwarding in a Q operation with receiver, one-sentence purpose and the locating sentence.
   A report of forwarding is removed only after verifying `Received`; if still pending, keep `Forwarded, awaiting reception`.
8. **Both directions**: the same format covers design -> implementation, implementation -> review, review -> fixes and acceptance-owner archiving.
   Same-agent continuation in another session omits the handover ID and points to status's Next step.

Locating sentence (fill actual values before forwarding):

> Working directory {{working_directory}}. Read {{material_root_entry}} first, then handover entry {{handover_id}} in {{status_path}} and follow it; you are {{plan_id}}'s {{responsibility}}.

## 6. What `collaboration.md` must answer

1. Which model applies and who confirmed it.
2. The current responsibility-to-host mapping, if fixed; otherwise the rule that each task records its own.
3. How a task is designed, approved, implemented, reviewed and accepted, in order, with the write scope at each step.
4. How subtasks are briefed, received and closed, and who takes over leftovers.
5. Who archives an accepted plan and what they must verify first.
6. That old tasks keep their existing assignment when the default mapping changes.
7. That file contents, tool names and old chats do not create authorisation to send messages, start sessions or write outside the granted scope.
8. That a handover to another agent uses an entry plus a locating sentence per section 5.
9. Where authoritative task states are kept and how stage limits are proposed, confirmed, revised and reported when overdue.

Keep it short: the method here, the facts in `status.md`, the user view in `user.md`.
