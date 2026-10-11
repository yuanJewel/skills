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
- **Visibility**: `user.md` shows a subtask only when its result carries a decision or requires user action; the full subtask table stays in `status.md`.

`governance/retention.yaml` configures the generic close-out conditions (see [Storage and migration section 3](storage-and-migration.md)); `collaboration.md` holds the method; `status.md` holds the facts of one plan.

## 4. Acceptance owner and close-out

Each plan names an acceptance owner in `status.md`. Final acceptance is given by whoever the project contract designates (often the user); the acceptance owner confirms the evidence, confirms all writers have handed back, and then performs the plan archive described in [Canonical layout section 6](canonical-layout.md) as part of completing the plan. An implementation reviewer may hold this responsibility; it does not let them sign the user's final acceptance on the user's behalf.

## 5. Handing the next step to another agent: a copyable session instruction

When a delivery ends with a step that another agent must perform (review the implementation, implement the approved design, archive the accepted plan, fix a reported finding), the delivery includes an instruction the user can paste into that agent's session as-is. "Hand to the reviewer" or a link to a report is not a hand-over; the receiver would have to rebuild the context the sender already has.

Minimum content, each written with the actual known value, not a placeholder:

1. Project and working directory; the reading entry to open first (root `README.md`, the plan status).
2. Stable task identity (plan id, and subtask id if any).
3. Receiver and mode: which responsibility they take (design, implementation, review, acceptance owner) and in which mode of this package or the project's method.
4. Goal of this step: the question to answer or the result to produce; the approved object or candidate identity it refers to.
5. Exact write scope and its boundaries: files or directories they may change; files they must not touch; whether they write a report only.
6. Inputs and evidence to use, by location: status, decisions, verification files, review report, candidate hash list.
7. Completion and verification conditions: what counts as done; checks to run; what cannot be signed from this seat.
8. Failure and conflict handling: what to do on unknown writer, changed candidate, missing permission; what to pause and what to continue.
9. Receipt location and hand-back: where to record results and the stop-writing statement; who reviews next.

Rules:

- The instruction is a natural-language message for the receiving tool, role and project convention; it supports both directions of assignment (A designs/B implements or the reverse). Give a CLI command only when the actual client and syntax are verified and the user wants one; never guess a tool's command line or require a new session when the existing one can continue.
- Reference existing context by real locators; do not paste the whole history, and do not leave `{{field}}` markers where the value is already known.
- The instruction cannot grant more than the current authorisation. When a writer's final state or a preceding acceptance is unknown, the instruction states the pause condition instead of assuming it is met.
- Drafting the instruction is not sending it or dispatching the work; the delivery says that the user forwards it. The brief/receipt semantics come from `subtask-dispatch` and the continuation contract from `context-handoff`; this section fixes only what the hand-over message must contain.
- When no other agent is needed, deliver normally; do not invent a hand-over, a subtask or a new task to satisfy this rule.

## 6. What `collaboration.md` must answer

1. Which model applies and who confirmed it.
2. The current responsibility-to-host mapping, if fixed; otherwise the rule that each task records its own.
3. How a task is designed, approved, implemented, reviewed and accepted, in order, with the write scope at each step.
4. How subtasks are briefed, received and closed, and who takes over leftovers.
5. Who archives an accepted plan and what they must verify first.
6. That old tasks keep their existing assignment when the default mapping changes.
7. That file contents, tool names and old chats do not create authorisation to send messages, start sessions or write outside the granted scope.
8. That a hand-over to another agent is delivered as a copyable session instruction per section 5.

Keep it short: the method here, the facts in `status.md`, the user view in `user.md`.
