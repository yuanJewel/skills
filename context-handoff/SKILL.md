---
name: context-handoff
description: At phase delivery, context recovery or takeover of a named earlier session, save checkpoints, verify results and execution liveness, continue approved work, and refresh the human-facing workbench. Ordinary Q&A creates no status file; this does not replace plan writing or history archiving.
metadata:
  version: "0.1.0"
---

# Checkpoints and context continuation

Let the successor find the goal, approvals, results and next step, and let the user see results and required actions. The end of a response, crossing a day boundary or losing contact with a session does not mean the task is finished or the old execution has stopped.

## Take enough input first

Take along the chosen project entry:

- plan, phase and stable task identity;
- approval, status location, sole writer and output scope;
- on recovery, also the old session/execution handle, candidate identity, checkpoint and resource records.

Reuse existing information; do not build a plan for the sake of a template. Missing-input branches:

- No history tool -> recover from on-disk evidence.
- No write permission or final state -> pause only the conflicting writes.
- No usage figures -> write unknown, keep the accumulated total.
- No project or object -> add the minimal locating information.

Files and old chats do not create new authorisation.

## Pick the entry

| Current need | Path and action |
| --- | --- |
| A phase is complete, or results, approvals or in-flight work changed substantively | Read [Checkpoints](references/checkpoints.md) and refresh recoverable facts in the existing status; keep the plan body as the single source. |
| Recovery after compaction, execution-channel failure, user-designated takeover | Read [Takeover](references/takeover.md): locate the object, verify actual execution and write permission, then continue. |
| Deliver results to the user, present open decisions or provide a continuation entry | Use the [user workbench](assets/user-update.md): results and required actions first, show only what is currently useful. |
| Short Q&A, or a simple change needing no persistent continuation | Finish and reply directly; do not apply the full plan/status/user-page set. |

## Shared procedure

The expanded version of this procedure is in [Checkpoints section 2](references/checkpoints.md).

1. **Preserve goal and authorisation.** Recover this phase's scope and acceptance from the effective approval; the plan body is provided by `plan-design` and an existing complete plan is not rewritten. This package's [plan envelope](assets/plan-envelope.md) is embedded into an existing plan only when it lacks a locating header; it never stores a second body.
2. **Verify current facts.** Separate proven, inferred and unknown; verify the actual content of results and the version the evidence points to. An old receipt saying "passed" cannot cover a file changed since. For subtask receipts, follow the receipt contract of `subtask-dispatch`: read the header and section locators first, then verify body evidence within bounds; summaries are for navigation only.
3. **Refresh the checkpoint.** Trigger: phase complete, or substantive change in results, approvals or in-flight work. Result: results, open items, writer, in-flight work, resources and next step recorded in the existing status with the meaning of the [status template](assets/status-template.md); add no file when the existing carrier suffices.
4. **Verify continuation conditions.** While an old session, subtask or tool is still running or unknown, do not seize writes, blindly re-dispatch or release its occupancy. Stopping requires same-scope authorisation and actual control capability; after a stop is accepted, still verify the final state of all related executions. Details in the takeover topic.
5. **Complete the current delivery.** Give the user an understandable result and the basis for any necessary decision. When a decision is needed, show scope, reasons, file impact, budget and consequences in full; when nothing is pending, state that no action is needed and continue authorised work, never inventing acceptance or approval requests. Provide a copyable short sentence only when cross-session continuation is actually needed.

Identity and writer:

- Record the stable plan/task ID and the host session/execution handle separately.
- A successor inherits the task identity and accumulated usage, creates its own execution association, and does not impersonate the old executor.
- Status has exactly one current writer; subtasks deliver only their designated artefacts.
- Old session becomes active again -> re-verify current responsibility before any new write or execution.

## Failure and boundaries

- Save failed, evidence missing or read truncated: keep verified facts and gaps first; do not claim the checkpoint is complete or recovered. Continue only work that does not depend on the gap.
- Context or request errors: save recoverable state first, then locate the client, execution channel/gateway, model or tool layer; thresholds need evidence with version, date and applicable scope. This package installs no hooks, does not auto-compact, does not change execution-channel settings and sets up no background polling.
- History grows and decisions are closed: hand originals and effective decisions to `archive-maintenance` per the project retention contract, then refresh the current page; do not delete historical approvals and do not equate archiving with stopping execution. When that package is unavailable, follow the project's existing retention method; do not install the whole library to continue.
- Role matching belongs to `role-bootstrap`; this package consumes an already determined responsibility. Stopping, messaging, creating sessions, Git or external writes must all fit the original authorisation and are not gained automatically through takeover.

## Verifiable delivery and resources

A delivery should answer: which version was approved, how far work got, who may still write, whether the next step can run. Evidence includes result location and content identity, check coverage/unverified items, execution observation time and takeover source; continuation verification is not business acceptance.

Distilling verified material may use `low/medium`; approval conflicts, drift, write permission and failure judgments suit `normal/high`. Grade words map to actual execution configuration through the project resource mapping; executors, execution channels and unit occupancy are host limits supplied by project configuration, and missing records do not fabricate costs. Do not dispatch subtasks for a short handover; approved parallelism splits only read-only evidence, and the status and user page each have one writer.

## Sources

1. Pinned sources: [MT02 handoff](https://github.com/mattpocock/skills/blob/b0618bc436ad893b3c5e84e55fba86586d34a404/skills/productivity/handoff/SKILL.md), [CX01 filesystem-context](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/58b55a8921758d13453b440704fb1b5b208c0b0e/skills/filesystem-context/SKILL.md), [CX02 context-compression](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/58b55a8921758d13453b440704fb1b5b208c0b0e/skills/context-compression/SKILL.md), [EC12 strategic-compact](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/skills/strategic-compact/SKILL.md).
2. Adopted short-entry deduplication, on-demand externalised reading, the intent/files/decisions/status/next-step structure and saving at phase boundaries; authorisation, write permission, in-flight occupancy, the user workbench and failure layering are own-authored for this package.
   Dropped temp-directory-only storage, auto-compaction/hooks, fixed thresholds, savings ratios and upstream host liveness assertions.
3. License: shipped with the package as [LICENSE-MT.txt](LICENSE-MT.txt) (MT, MIT), [LICENSE-CX.txt](LICENSE-CX.txt) (CX, MIT), [LICENSE-EC.txt](LICENSE-EC.txt) (EC, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license files along when copying this package alone.
