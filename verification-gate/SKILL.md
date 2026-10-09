---
name: verification-gate
description: Before claiming something is done, fixed or passing, verify that the claim matches the candidate, the acceptance, the execution state and the evidence scope. Reuse evidence that is still valid and add only the necessary checks; does not invent a separate test strategy or automatically rerun the full suite.
metadata:
  version: "0.1.0"
---

# Claim and evidence verification

State the provable scope precisely. Code produced, tests passing, human acceptance, release-ready and actually released are different conclusions and cannot substitute for each other.

## Five-step loop

1. **Make the claim and criteria explicit.** Split "done" into verifiable items and take the approved acceptance/task scope.
   A small change may have only one item; without a basis, do not add full-suite gates yourself. Test scope is decided by `test-strategy` or the project's existing strategy.
2. **Bind candidate and conditions.** Take the actual artefact identity, runtime/dependencies, environment, cases/commands, inputs and execution records;
   verify that it is the content intended for delivery.
   The current directory name, tag text or a subtask's self-report cannot alone prove the candidate matches.
3. **Read and interpret the execution.** Verify final state, exit code, executed/failed/skipped counts and assertions.
   Per the [evidence semantics](references/evidence-semantics.md), rule out misreadings such as zero cases, unfinished background runs, truncated output and pipeline exit-status masking.
   Static reasoning, preflight and simulation each prove only the level they reach.
4. **Close gaps with minimal checks.** If the evidence is compatible with the current claim, cite it; do not rerun for every success message.
   When the candidate/acceptance changes, analyse the affected part and keep unaffected evidence.
   If an artefact, prerequisite or result is missing, narrow the conclusion or run the minimal necessary check within current authorisation.
   If execution has not finished, save/verify the in-flight work first; do not blindly restart.
5. **Give a scoped result.** Use the [verification summary](assets/verification-summary.md) or the existing receipt to list claim, evidence, status and limitations,
   and name the remaining manual steps.
   The final owner verifies the actual artefact and necessary results; author self-check, independent acceptance and user acceptance are each signed as they actually happened.

## Statuses and wording

- `PASSED`: the prerequisites for the claim hold, and valid execution/review evidence bound to the candidate meets the criteria.
  State whether it is a static check, simulation, partial regression or full suite; a green tick alone cannot widen the scope.
- `FAILED`: a valid observation contradicts the criteria; give the failed item and evidence.
  A successful rerun after a failure does not delete the first run; explain the difference or keep a flakiness limitation.
- `BLOCKED`: a prerequisite is missing, results are incomplete, execution was interrupted or the evidence does not apply, so no judgement is possible yet.
  State what is missing, what it affects and how to recover. It is neither "the product failed" nor a pass.
- `N/A`: an acceptance/applicability basis proves the item does not apply; record the reason. A tool skip, lack of time or an unavailable dependency is never automatically N/A.

Items not yet started are marked "not run"; that is execution progress and must not be recorded as PASSED.
When aggregating, keep each item's status: any required FAILED means the scope does not pass; any required not run/BLOCKED means verification is incomplete.
Only when all required items are validly proven and N/A reasons hold may the scope be given a pass conclusion.

## Failure and continuation

With only linter output, say "format check passed, compilation unverified"; with exit 0 but zero cases, verify the discovery rules and planned set, and do not say "all tests passed".
A subtask says it is done but there is no file/result: verify its artefact location and in-flight work; missing evidence still blocks the related claims.

When old-candidate evidence, after impact analysis, still covers currently unchanged behaviour, keep the original candidate identity and the applicability argument; do not rewrite history.
On session change, recover from existing evidence/checkpoints and do not reset checks that are already valid.
When evidence conflicts, first verify time, candidate, tool semantics and duplicate receipts; do not pick the best-looking one.

This skill never authorises real external actions, releases or obtaining human acceptance.
Further actions follow the current user scope and project boundaries; when existing evidence cannot support a broad conclusion, still report the proven partial results clearly.

**Wrap-up cleanup**: before claiming completion, verify that the processes, containers and temporary data started by this verification
have been cleaned up per the local resource cleanup rules of `task-implementation`, or that remaining items are listed with reasons;
unlisted leftovers make the completion claim incomplete.

## Resource suggestions

Mechanical checks low/low; conflicting evidence normal/medium; key security/compatibility conclusions normal/high;
grade words map to actual execution configuration through the project resource mapping.
Independent read-only checks may run in parallel when authorisation and resources allow, finally merging on the same candidate and acceptance set; reviewers' verbal agreement is not fact.

## Sources

1. Pinned source: [SP06 verification-before-completion](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/verification-before-completion/SKILL.md).
2. Adopted the claim -> execute -> read -> judge loop; candidate applicability, tool semantics, four-state aggregation and recovery are own-authored for this package.
   Dropped rerunning for every success statement, "all partial evidence is invalid" and binding to Git actions.
3. License: shipped with the package as [LICENSE-SP.txt](LICENSE-SP.txt) (SP, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).
   Copy the license file along when copying this package alone.
