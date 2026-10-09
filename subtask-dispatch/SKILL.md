---
name: subtask-dispatch
description: When the host allows dispatch and the task can close independently, split subtasks, reserve resources, dispatch and verify results, and handle unknown in-flight work and recovery. Does not dispatch automatically because there are several files or for the sake of concurrency.
metadata:
  version: "0.1.0"
---

# Subtask dispatch and acceptance

Split an authorised goal into independently acceptable work while every write location always has exactly one executor. If the host allows dispatch only when the user explicitly asks, satisfy that condition first; this package itself grants no dispatch permission.

## Decide first whether splitting is worth it

Start from the current goal, approved scope, dependencies and acceptance:

- Several problems can each be solved with their own minimal input, their artefacts accepted separately, and they do not contend for written files or run resources: parallel is possible.
- Two items depend on the same undecided interface, the same database state or the same written file: one writer fixes the boundary first, then hand over serially; read-only review may run in parallel, but never sign off an old version while it is being modified.
- A single small change, a shared root cause not yet understood, or integration cost above the parallel gain: the main task does it directly. When independent review is valuable, split only the review; do not split root-cause work by test-file count.

Without a goal/approval boundary, dispatch no implementation; read-only organisation may continue. Without resource-pool configuration, real run state or stop evidence, do not guess that capacity is free.

## Dispatch loop

1. Give every task a stable logical ID, goal, minimal sources and exact artefacts; use the [task brief template](assets/task-brief.md) to state readable/writable scope, sole writer, acceptance, failure and stop conditions. Do not paste the whole history; whether context is inherited depends on host capability and task need.
2. Verify dependencies are satisfied. Check for conflicts on the same file, environment or resource pool; resource conversion, main-task accounting and unknown in-flight work follow [Resource accounting](references/resource-accounting.md).
3. Reserve first, then call dispatch. Record the mapping from request to real execution handle; when the result is unclear keep the occupancy and query the same request first — never send a replacement directly.
4. Record the requested grade words (cost tier/reasoning tier) and the actually verifiable result per [Host adapters](references/adapters.md); start only when both host slots and resource-pool units suffice. If either is short, wait, shrink the task or adjust resources per approval.
5. The main task continues independent integration preparation. On a block, stop only actions depending on it; when the estimate clearly deviates, report the reason, usage so far and remaining expectation, and offer continue / shrink scope / keep results and end — never treat a timeout as new authorisation.
6. On receiving a [receipt](assets/task-receipt.md), read the header first, then verify key body, changes and verification evidence via the locators. Check that the content identifier still matches the current result; if stale, refresh the receipt before review. A summary or "done" label is not acceptance.
7. Confirm the author has stopped writing before taking over changes. Check artefact conflicts, omissions and interface consistency; run the necessary combined verification by impact, not a mechanical full run because an upstream example asked for it. Arrange independent review by risk and project requirement; do not treat author self-checks as independent conclusions.
8. Release occupancy only after all related executions are confirmed terminated; keep the accumulated actual usage. Hand pass, rework, abort and unverified separately to the existing status maintainer; build no separate status store outside the package.

## Recovery and output

On recovery, read existing checkpoints, approvals and the task-to-handle mapping first and query in-flight work; context compaction, message interruption or a business block does not prove execution stopped. While the old writer may still be running stay read-only; hand over write permission only after a confirmed stop. Retries continue the logical task record; a new execution attempt gets its own handle, and existing usage is not counted twice.

Output is the designated result files, a verifiable receipt and the necessary update to the current task status. The plan body belongs to `plan-design`, the user workbench and continuation status to `context-handoff`; consume only their locators and approvals, do not copy their templates. Without those packages use the project's existing contracts.

**Wrap-up cleanup**: containers, processes, temporary files and test data created by subtasks are listed with the receipt; on acceptance the dispatcher takes over unreclaimed items and handles them per the local resource cleanup rule of `task-implementation`. A subtask ending does not mean cleanup happened.

## Resources and counterexamples

Coordination and routine tasks may start the estimate at `normal/high`; fully mechanical tasks may use `low/low`; cross-domain root causes or high-risk integration raise reasoning or verify serially. Grade words are suggestions mapped to actual execution configuration through the project resource mapping. Executors, weights, independent resource pools, slots and budgets are host limits supplied by project configuration; insufficient resources cannot be drawn again under another name.

Normal example: two independent documents with fixed interfaces go to different writers, dispatched after reservation and integrated once receipts confirm stop-writing. Misuse example: two test files fail from the same shared-state bug and two implementers are told to change the same module at once; the root-cause investigation should be merged first. Failure example: a dispatch request times out without returning a handle; keep the reservation and query the execution, do not infer failure from a missing receipt and re-dispatch.

## Sources

1. Pinned source: [SP03 dispatching-parallel-agents](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/dispatching-parallel-agents/SKILL.md).
2. Adapted independent problem domains, self-contained task briefs and conflict acceptance; resource reservation, unknown in-flight work, stop-writing, accumulated usage and recovery are own-authored for this package.
   Dropped fixed task counts, never inheriting full history, splitting by test file and automatic full test runs.
3. License: shipped with the package as [LICENSE-SP.txt](LICENSE-SP.txt) (SP, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license file along when copying this package alone.
