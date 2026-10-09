---
name: task-implementation
description: Execute an approved task; implement within the single write scope, compare expected against actual verification, record deviations and recover from checkpoints. Does not auto-escalate design or review requests into implementation.
metadata:
  version: "0.1.0"
---

# Implementing per approved task

Turn an existing approval into verifiable file changes and results. A simple change the user states explicitly can itself constitute the task and its authorisation; do not build a full plan to satisfy a format. When a plan exists, consume its exact version, acceptance and dependencies instead of redesigning one.

## Start or resume

Read the current goal/mode, approved scope, tasks and dependencies, writable files, sole writer, existing checkpoints and relevant project commands. Missing approval blocks only implementation; read-only clarification may proceed. Missing write permission means that file is not touched. When the plan still has open questions, separate those that block this task from work that can be completed independently.

On resume, compare the checkpoint against the actual candidate files, run evidence and related execution state. Parts marked done whose content or dependencies changed need re-verification; parts truly done and still applicable are not redone. While it is unknown whether an old execution has stopped, stay read-only and verify in-flight work through `subtask-dispatch` or the existing execution-status flow; never give the same file a second writer.

## Loop per task

1. Verify the task is not yet done and its dependency artefacts and interface versions are satisfied. Read the task's real inputs and existing implementation; do not guess function signatures, field semantics or command parameters from earlier summaries.
2. Define observable expectations: what the user will see, how errors are rejected, how boundaries or state recovery behave; reduce the gap between plan requirement and current state to the minimal change. Ordinary implementation details follow existing project patterns at your discretion.
3. Implement within the authorised scope. A regression case for a bug fix or new behaviour should first be observed failing, then pass after the fix; the failure must come from the target behaviour, not a missing dependency or syntax error. For pure copy/style/generated artefacts choose a meaningful check; do not build a mechanical TDD ritual.
4. Run the relevant lint, build, tests and necessary manual checks the project prescribes, read the results and compare each against expectations. Save candidate identity, environment/inputs, full log location and key assertions. Exit 0 is only the process result; wrong data, a failed business assertion or a skipped case is still not a pass.
5. When expectations are not met, use [Deviation handling](references/deviation.md) to decide whether it is an implementation error, a verification problem, a plan conflict or a missing environment item; fix the cause, then re-verify affected items. Necessary checks and fixes within scope continue to completion; do not re-request already given authorisation at every step.
6. Reclaim containers, images, processes, temporary files and test data produced this run per [Local resource cleanup](references/cleanup.md): register on creation, delete only registered own objects at wrap-up, and list retained evidence and cleanup failures in the receipt.
7. Use the [implementation receipt](assets/implementation-receipt.md) to give actual changes, expected/actual, unverified items, deviations and the recovery entry. Hand to `change-review` / `verification-gate` or the project's existing review flow; author self-tests are not independent acceptance, and one passing log does not declare everything finished.

## Completion and handover

Before declaring completion confirm: artefacts within the approved scope are complete, necessary checks actually ran with matching results, deviations are explained, temporary resources from this run are reclaimed or remaining items have stated reasons, and unfinished items have accurate impact and next step. Checks that cannot run are marked unverified; if such a check is an acceptance prerequisite, the task still awaits evidence. Whether old verification still applies after a change is judged by impact; never reuse a report that does not match the current candidate.

Hand only this task's necessary facts to the existing status maintainer; the current user workbench/checkpoint is carried by `context-handoff`. This package keeps no second progress store. After stopping writes, state the write handover and remaining in-flight work. Without the companion packages, use the project's existing plan, status and verification gate.

## Resources and examples

Ordinary implementation starts the estimate at `normal/high`; `low/low` suits only mechanical items whose inputs, outputs and change location are precisely fixed. Grade words map to actual execution configuration through the project resource mapping. When cross-interface complexity rises, re-estimate dependencies and risks first; use `subtask-dispatch` only when independent work is genuinely needed and the host allows it. Do not bypass approval by switching model or tool.

Normal example: an approved fix for empty-list pagination first reproduces the out-of-range error with an empty list, then changes the boundary handling, runs the necessary checks and gives evidence tied to the candidate. Counterexample: refactoring another module without write permission "to make testing easier" must stop and report the boundary. Resume example: the checkpoint has data-layer changes and valid tests but the UI is unfinished; after verifying the candidate matches, complete only the UI and the affected integration checks. Failure example: the command exits 0 but the returned record count does not match acceptance; record the failure and keep investigating, do not fill in pass.

## Sources

1. Pinned source: [SP04 executing-plans](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/executing-plans/SKILL.md).
2. Adopted the per-task loop, real inputs, expected-versus-actual comparison and completion evidence; approval boundaries, reuse of existing checkpoints, deviation classification and single-writer recovery are own-authored for this package.
   Dropped automatic Git/worktree and upstream scripts, mechanical TDD, self-adjudication of arbitrary conflicts and a default highest-cost final review.
3. License: shipped with the package as [LICENSE-SP.txt](LICENSE-SP.txt) (SP, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license file along when copying this package alone.
