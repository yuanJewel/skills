---
name: ai-workspace-governance
description: Establish, maintain or review AI working materials under a project-selected root. Keep a common core for governance, selective policy-change memory, knowledge, active plans, a user workbench and retention configuration; allow project extensions and archive accepted plans under one archive root. Ordinary retrieval, implementation and isolated archive runs use their existing methods.
metadata:
  version: "0.1.1"
---

# AI workspace governance

Give every project one predictable place for the material that AI sessions and humans share: current rules, who is responsible for what, verified facts, active plans and frozen history. The root directory may be called anything; what stays constant is the core structure under it, where each kind of material belongs, and that archived material lives in exactly one place.

## Start and inputs

First decide which of three modes the request is in; a method existing does not grant write permission.

| Mode | When | Output |
| --- | --- | --- |
| Design | The user wants a structure proposal, a migration map or a decision about where a new rule belongs | A proposal and a filled [workspace map](assets/workspace-map.md); no files under the root are created or moved |
| Implementation | The user has approved a proposal and granted write scope under the root | The root conforms to the [canonical layout](references/canonical-layout.md); material is placed, merged or archived per the approved map |
| Review | A fixed candidate root is to be checked against the layout and contracts | A report only; the reviewer does not edit the reviewed root |

Inputs and missing-item handling:

- Material root path or the decision to choose one. Missing -> locate an existing root along the project entry (for example, the project README or declared agent entry); if none exists, ask the user to choose; never create a root in another repository or outside the granted scope.
- Current writers, in-flight tasks and the state of any file to be moved. Unknown -> pause only the conflicting files, keep the rest of the work moving; do not treat "no reply" as "writer stopped".
- Project contracts that already exist: Git policy, language rules, release procedure, role assignments, retention periods. Missing -> record "not configured" in the relevant file; do not invent periods, roles or approvals to fill the skeleton.
- The question "does this new requirement belong to the task, the project or the shared method?" Unclear and it would change behaviour across projects -> ask before placing it; clear -> place it and record the basis.

Ordinary requests do not trigger this package: looking up a fact (`project-context`), implementing a feature (`task-implementation`), saving a checkpoint (`context-handoff`) or archiving one batch of files (`archive-maintenance`) each use their own method. Use this package when the shape of the material itself, its ownership or its lifecycle is the subject.

## Core structure in one view

Under the chosen root the following always exist once the root is initialised; the full placement contract is in [Canonical layout](references/canonical-layout.md).

```text
<root>/
├── README.md            reading entry: what is here, in which order to read it
├── user.md              user workbench: Q waiting on you, N in progress, P scheduled, E ended, for the current version
├── governance/          policy, operating rules, responsibilities, retention config, policy-change memory, optional roles
├── knowledge/           verified project facts and domain contracts
├── plans/               active plans: <plan-id>/plan.md, status.md and attachments
└── archive/             every archived original, superseded version and preserved backup; accepted plans under archive/plans/<plan-id>/
```

`governance/` always carries `README.md`, `policy.md`, `collaboration.md`, `retention.yaml` and `memory/`; `roles/` is added only when the project maintains long-lived role contracts. Projects may add top-level directories for responsibilities the core does not cover (for example `maintenance/`, `sources/`, `testing/`, `runtime/`, `documents/`) and must declare each one in the root `README.md`. An extension never takes over a core responsibility: role contracts stay in `governance/roles/`, user policy adjustments stay in `governance/memory/`, and nothing is archived anywhere but `archive/`.

## Method

Execute each step as "what / stop condition / artefact".

1. **Fix the object and mode.**
   - What: read the entry the user named, confirm root, mode and write scope; identify the plan this work belongs to.
   - Stop: no entry and no permission to look for one; cross-root scope unclear -> pause that part only.
   - Artefact: root, mode, plan identity and allowed paths stated in the task status.
2. **Inventory and classify.**
   - What: list existing material and classify each item per [Material model](references/material-model.md): first its scope (one task, this project lasting, shared method), then its class (current rule, project fact, active task material, historical evidence, rebuildable output, user policy adjustment). Mark the single authoritative file for each contract and every file that references it.
   - Stop: a file cannot be opened within the allowed scope -> record the exclusion, do not guess its content.
   - Artefact: the "Inventory" table of the workspace map.
3. **Decide placement of new or moved requirements.**
   - What: for each requirement decide the scope first — task / lasting project rule / shared method — then the destination under the canonical layout. A task-scoped permission, restriction or approval goes to `plans/<plan-id>/decisions/` and stays with that task even when it is phrased as a prohibition; a lasting project rule goes to `governance/policy.md` or a named policy page; an adjustment the user made to a lasting policy or operating rule is also distilled into `governance/memory/<topic>.md`; a change to a shared method goes to the method's own package under its own write authorisation.
   - Stop: placement unclear and it would change behaviour in other projects -> ask; a clear user instruction is placed directly, with the instruction recorded as basis.
   - Artefact: each change has one destination and a stated scope.
4. **Configure collaboration.**
   - What: record responsibilities, the host or tool currently filling each one, the sole writer per file and the acceptance owner per plan in `governance/collaboration.md` and the plan status, following [Collaboration contract](references/collaboration-contract.md).
   - Stop: two writers claim the same file -> keep both claims visible and freeze that file until the user decides.
   - Artefact: a successor can tell who may write what without asking.
5. **Design the layout and the migration.**
   - What: map every old path to a new path and an action (keep, move, rewrite-and-merge, archive, retire); state the single preserved backup for the batch and how it is restored; follow [Storage and migration](references/storage-and-migration.md).
   - Stop: no write scope -> deliver the design only; an object whose writer is unknown stays where it is.
   - Artefact: migration table with per-item status.
6. **Implement or review.**
   - What: in implementation mode execute the approved table, verifying byte identity for moved originals and restorability for the backup before retiring any old file; in review mode check the fixed candidate against the layout and the contracts and write a report.
   - Stop: a target already exists with different content -> never overwrite; source changed since the backup -> list the real difference, do not claim the earlier backup covers it.
   - Artefact: changed files, verification evidence, the list of items left in place with reasons, and — when the next step belongs to another agent — the handover entry and locating sentence described below.
7. **Maintain and close.**
   - What: new material goes to its class without a new design round; update only the indexes that changed. When a plan is complete and the project's final acceptance has passed, the acceptance owner archives it in the order of [Canonical layout section 6](references/canonical-layout.md): mark pending; copy to `archive/plans/<plan-id>/`; verify bytes and links; write the archive record with the file manifest; mark the three navigation files provisionally (`switch pending`) while the source and its links stay; remove the source by the manifest; finalise `user.md`, then the active index, then the record; and set the archive row to `archived` as the very last write.
   - Stop: design approval, a passed review or a partial delivery does not close a plan; a subtask ending does not close its parent. Until the source is removed, every failure leaves the source with working links from the active index and the workbench, and the archive row at most `switch pending`. Navigation files and the archive record are published atomically (temp, read back, rename), never truncated; a record without its manifest-complete line is a leftover, not a record, and a torn progress line is not a state. After a stop, resume by verifying the record against the archived files and observing the actual source directory and the file contents — not by the presence of a file, of `status.md` or of a single progress line — and never by deleting the archive copy or re-creating the source.
   - Artefact: one archive root, complete originals, working indexes.

## Memory, workbench and retention in brief

- `governance/memory/` records only effective adjustments the user made to policy, operating rules or maintenance constraints, and the few open points that directly belong to such an adjustment. One topic, one file: a later conversation on the same topic updates that file rather than creating a dated or per-session one. Each topic keeps the minimal verbatim words, the distilled rule, a one-line reason and a link to the current authoritative text. Ordinary Q&A, progress, one-off task approvals and full transcripts are not memory.
- `user.md` shows Q waiting on you, N in progress, P scheduled and E ended this cycle for the current development version.
  Format and refresh rules belong to `context-handoff` [Workbench rules](../context-handoff/references/workbench.md).
  Task states are authoritative in the project task register, not in the workbench; settled Q items leave only after their formal records are saved and read back.
- `governance/retention.yaml` is real YAML configuration: what is protected, when a plan may close and be archived, how a parent task receives its subtasks, when material may be cleaned and under what user-confirmed limits. Unset values are written as not configured; the file does not run anything by itself.

## Handing work to another agent

When a different agent must do the next step, write the nine required fields once in a handover entry in that plan's `status.md`.
Use [the handover template](assets/handover-entry.md); field definitions and reception rules belong to [Collaboration contract section 5](references/collaboration-contract.md).
The user forwards only the locating sentence, giving the working directory, reading entry, status path, entry ID, plan and responsibility.
If the receiver cannot read project files, fall back to pasting all nine fields and mark the entry accordingly.
Drafting is not sending or dispatching, and the entry cannot widen existing authorisation.
A step needing no other agent gets no invented handover.

## Scenarios and resources

- Normal: a project with a declared agent entry and `docs/` chooses `docs/agent-notes/` as root; the package proposes the core skeleton plus the one extension the project needs, the user approves, the skeleton is created with real contracts or explicit "not configured" lines, nothing else is invented.
- Misuse: a request to "tidy the plans folder" while two plans are still being written by other sessions -> move only the completed and accepted plan, record the others as active with their writers; a request to review a root -> report, do not fix.
- Failure: an old memory file says one tool always designs and the other always implements, but the user has since said the roles swap per task -> the current instruction wins, the memory topic is corrected with both the old wording and the new one, and no file is "adapted" by rewriting a frozen original.

Classification and path mapping use low/low; placement decisions, collaboration conflicts and migration of live material use normal/high. Grade words map to actual execution configuration through the project resource mapping. Temporary restore directories used to prove a backup are recycled per the local resource cleanup rules of `task-implementation`.

## Sources

1. Pinned source: [CX01 filesystem-context](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/58b55a8921758d13453b440704fb1b5b208c0b0e/skills/filesystem-context/SKILL.md), sections `Core Concepts`, `The Static vs Dynamic Context Trade-off` and `Gotchas`.
2. Adopted locating material along a short entry, externalised originals with pointers and detection of stale references. Own-authored and pending behaviour verification: the canonical layout, the material classes, selective policy-change memory, the separation of responsibility from tool, the single archive root and acceptance-owner close-out.
   Stage commitments, the Q/N/P/E workbench and handover entries are own-authored. Dropped unlimited storage, full re-reads every turn, self-modifying instructions, cleanup by age and append-only writes as a concurrency answer.
3. License: shipped with the package as [LICENSE-CX.txt](LICENSE-CX.txt) (CX, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license file along when copying this package alone.
