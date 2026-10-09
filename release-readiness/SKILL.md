---
name: release-readiness
description: When the user is preparing to go live, move from a pinned candidate, reviews and local full-suite evidence into human acceptance, handle acceptance changes and give a pre-release recommendation. In ordinary phases it only assesses the current state and does not start a full suite automatically; this skill does not release, cut over traffic or replace the user's final decision.
metadata:
  version: "0.1.0"
---

# Pre-release readiness check

Deliver an explicit recommendation such as "ready for human acceptance", "needs fixes or more evidence" or "awaiting final human decision".
Automated tests, human acceptance and the actual go-live each have their own evidence; green tests do not mean released.

## Inputs and start

Inputs:

- The user's intent to prepare for go-live.
- The reviewed candidate.
- Requirements/acceptance.
- Known defects.
- The full-suite set and run conditions.
- Simulated environment records.
- The human acceptance path.
- The recovery plan.
- Real external boundaries.

Missing inputs and phases:

- No candidate or necessary environment -> supply the corresponding prerequisite first.
- No go-live intent (ordinary development phase) -> continue the relevant regression; do not start a full suite because this skill was opened or someone said "the feature is written".

Consume the existing plan, test strategy and candidate records; build no second status board.
The concrete deployment strategy comes from `deployment-patterns` or the project's existing approach;
this skill verifies evidence and order, and neither picks another platform nor executes production steps.

## One full suite through to the human decision

1. **Pin the actual candidate.** Identify source/artefacts, dependencies/generated artefacts, configuration structure and test environment identity;
   confirm how changes are restricted during this acceptance round.
   Verify the actual content per [Candidate and evidence](references/candidate-and-evidence.md); a tag or an old commit must not hide uncommitted fixes.
2. **Verify prerequisites and scope.** Against review conclusions, known defects and acceptance items, give the source or the gap for each required piece of evidence.
   When the environment is not ready, a key defect is unexplained or the candidate is unclear, do not treat "try one run" as a complete full suite. Independent preparation work continues.
3. **Complete one full suite when preparing to go live.** Execute against the agreed set, the current candidate and isolation conditions, keeping shard and first-run/rerun results;
   verify valid final states with `verification-gate` or equivalent rules.
   A single required item that is BLOCKED, not run or FAILED means "all passed" cannot be written. Retest failure fixes by impact; do not turn every small fix into a second full suite automatically.
4. **Enter human acceptance after it passes.** Provide a re-verifiable path, expectations, the candidate and limitations,
   and keep a real acceptance record per [Human and external boundaries](references/acceptance-and-external-boundaries.md).
   Author self-check or agent testing must never sign the user's acceptance on their behalf.
5. **Handle acceptance changes.** Keep the original candidate and evidence and create a new candidate relationship;
   retest by behaviour/dependency impact, re-review where necessary and update the applicable evidence.
   A copy-only change usually gets content/necessary page checks; an authentication/authorisation change must re-verify permissions and adjacent paths.
   When the candidate changes substantially, the environment is no longer equivalent or the impact cannot be bounded, state the basis, scope and estimate for an additional full suite;
   no routine double full suite.
6. **Summarise for the final human decision.** Use the [readiness summary](assets/release-readiness.md)
   to present the candidate, full suite, reviews, acceptance, residual risks and real external manual items;
   where necessary evidence has gaps, state exactly what must be supplied.
   The conclusion is a recommendation: it does not replace approval and does not execute a release, image push, real trigger, traffic cutover or production rollback.

## Recovery and time

When execution is interrupted, first confirm whether shards, in-flight handles, the candidate and the environment are still consistent;
keep valid completed shards and do not restart unknown in-flight work.
For the same candidate under the same applicable conditions, continue the unfinished shards; a session change is not a new full-suite round.
If the candidate or environment has changed, state the invalidation and recovery scope by impact.

Give automated test elapsed time, expected manual work and external waiting separately; parallel shards are not simply summed.
The go-live window is only an estimate conditional on prerequisites; when manual or external durations are unknown, mark them unknown, and do not promise go-live from the tests' expected end time.
Resource/history samples follow the project's existing estimation records; avoid copying run logs.

## Resource suggestions

Executing existing deterministic shards is usually low/low; reviewing acceptance coverage is normal/high; grade words map to actual execution configuration through the project resource mapping.
The main task owns candidate consistency, aggregation and the summary.
Parallelism requires that host limits given by project configuration, such as executors, concurrency quota and machines/environments, jointly allow it, with ownership isolated per shard;
recovery drills run only in an authorised synthetic environment.

## Sources

1. Pinned sources: [EC10 deployment-patterns](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/skills/deployment-patterns/SKILL.md), [SP06 verification-before-completion](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/verification-before-completion/SKILL.md).
2. From EC10, borrowed the health, recovery and release evidence categories, leaving concrete strategy implementation to the dedicated method; from SP06, borrowed binding conclusions to evidence.
   Human acceptance after one full suite, change impact and the human boundary are own-authored for this package.
   Dropped fixed platforms, default strategies, production commands, the all-in-one unified checklist and rerunning on every statement.
3. License: shipped with the package as [LICENSE-EC.txt](LICENSE-EC.txt) (EC, MIT), [LICENSE-SP.txt](LICENSE-SP.txt) (SP, MIT);
   library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license files along when copying this package alone.
