---
name: plan-design
description: Turn a clear requirement into an implementable, hand-over-ready multi-step plan with files, interfaces, dependencies, acceptance and budget; when a complete design exists, verify it and fill gaps. Ordinary Q&A or low-risk small changes do not force a full plan, and this grants no requirement-change or execution permission.
metadata:
  version: "0.1.0"
---

# Implementation plan design

Produce the single plan from which key decisions need not be guessed again. Follow the project's existing plans, directories, roles and approval rules; do not treat suggestions as user requirements.

## 1. Obtain minimal input

From the workspace, task and evidence chosen by the user take: requirement version and authorisation, facts and constraints, existing design, relevant implementation/interfaces, writer, acceptance and resources. Read per task; a missing item blocks only the decisions depending on it, other authorised design continues.

Use stable requirement IDs to separate user requirements, author suggestions, verified facts and assumptions pending verification, each with source location, date or version. Separate the user's proposed solution from the problem to solve; suggestions state benefit, cost and whether scope changes, and are never silently promoted to approved requirements.

Verify an existing design against the contract below first. When sufficient, reference the original and give the verification basis; with gaps and write permission, complete the original, otherwise hand the delta to the sole writer. Do not generate a second plan to fit a template.

## 2. Make implementation decisions

1. **Fix goal and boundaries.**
   - What: map each requirement to an observable result; state what is excluded and which users and data are affected; verify existing implementation and reuse paths, separating "already exists" from "to be added".
   - Missing branch: key fact without evidence -> keep pending; real requirement conflict, scope growth or incompatible constraints -> state the conflict and options and clarify first, continue the independently doable part.
   - Artefact: requirement-to-observable-result mapping, scope boundary and pending list.
2. **Fix files and contracts.**
   - What: list exact add/modify/verify paths and responsibilities under the real project root, marking candidate new paths; record consumed and produced interfaces, types and business semantics, with one shared contract definition across modules.
   - Missing branch: cross-module, state or migration appears -> read [Task boundaries sections 1-3](references/task-boundaries.md#boundaries) and bring failure, recovery, compatibility and required order into the design.
   - Artefact: file list and interface contracts.
3. **Split into independently acceptable loops.**
   - What: a task has inputs, artefacts, dependencies, a sole writer and a decidable result; preparation, configuration and documentation belong to the artefact they serve. Each step records decision, action and check result; keep signatures, key values and necessary algorithm notes, do not pre-write all the code.
   - Stop condition: split only when parts can be accepted or returned separately; do not end by day, and do not manufacture concurrency from file counts.
   - Artefact: task contracts.
4. **Connect verification to tasks.**
   - What: each requirement links to tasks and acceptance items, each important failure mode has an owner; give prerequisites, concrete inputs/operations or commands, expected observation and evidence location, listing automated tests and manual acceptance separately.
   - Stop condition: stop once effective verification is chosen by risk; a low-risk small change may check the diff, rendering or targeted behaviour without mechanically adding a test suite; the project's current mandatory checks are still included.
   - Artefact: acceptance items and requirement coverage.
5. **Estimate resources and elapsed time.**
   - What: per task give an hour range, resource assumptions and research/implementation/verification/integration cost; elapsed time follows the longest dependency chain and available resources, with human waiting listed separately — never total hours divided by head count.
   - Missing branch: a full estimate is needed (original estimate, current forecast, accumulated actual, visible usage) -> use the `estimation` package's template; that package unavailable -> use the minimal basis in [section 4](references/task-boundaries.md#estimates). Unknown is never filled as 0.
   - Stop condition: an estimate is not a commitment or deadline; work does not end on its own because the estimate was exceeded.
   - Artefact: hour ranges, resource assumptions and elapsed time in section 7 of the plan template.

When creating or supplementing content use the relevant parts of the [plan template](assets/plan.md); small tasks may merge sections and need no separate file. Placeholders in the template are replaced with current facts, explicit pending items or a reasoned "not applicable".

## 3. Self-check against the requirements

Go back to the original requirements rather than only reading your own plan: trace each to tasks, files, interfaces and verification; then check in reverse that every task has a requirement basis and that no author suggestion is listed as mandatory. Per [section 5](references/task-boundaries.md#review) check missed boundaries, cross-module signature consistency, failure recovery, compatibility windows and resource dependencies. On finding a difference, fix the plan you are authorised to maintain and re-verify affected relations.

"Design self-checked" states only the plan check result; "implemented", "tests pass", "independent review passed" and "manual acceptance done" each need their own evidence. Interfaces, paths, tests or approvals that cannot be verified stay pending; model consensus or past success does not replace this run's evidence.

## 4. Delivery and continuation conditions

Deliver the single plan location/version, continuable scope, real open items and next step. The approval record points to the actual user instruction or the approval original the project requires, stating covered tasks, version and conditions; author suggestions, review comments and silence never pose as approval. Keep original approval evidence; later changes state which tasks and old conclusions they affect.

With design authorisation only, deliver the design; with existing implementation authorisation and unchanged scope, candidate and constraints, continue — do not mechanically request approval because this skill generated a plan. Execution follows the method the user already chose; this skill forces no dispatch, Git, installation or external operations. New authorisation is obtained only when a concrete action really exceeds current authorisation, after completing a reviewable design. One continuous-execution authorisation does not become a default no-approval rule for other projects.

Current progress, in-flight work and accumulated usage are maintained at the project's existing status location; the plan stores only the baseline and necessary snapshots/references, no rolling log. Switching sessions does not reset usage. At wrap-up verify actual coverage and unfinished items; reaching the time estimate or sending a reply is not task completion.

Usually use `normal/high`; for complex independent technical judgment propose the expected cost and purpose of `normal/xhigh`, decided by user choice and actual configuration. Grade words map to actual execution configuration through the project resource mapping; executors, concurrency quotas and platform capabilities are host limits supplied by project configuration — no default max/max, and no self-dispatch on the strength of an estimate.

## Sources

1. Pinned source: [SP02 writing-plans](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/writing-plans/SKILL.md).
2. Adapted exact files/interfaces, independent acceptance granularity and requirement cross-check; source tracking, single plan, authorisation continuation and budget contract are own-authored for this package.
   Dropped fixed paths, step-by-step commits, worktrees, TDD everywhere and mandatory second approval.
3. License: shipped with the package as [LICENSE-SP.txt](LICENSE-SP.txt) (SP, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license file along when copying this package alone.
