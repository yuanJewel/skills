---
name: systematic-diagnosis
description: Investigate defects, build failures, cross-component errors or performance regressions, locating the cause through symptom reproduction, boundary evidence and falsifiable experiments. An approved small fix with an already clear root cause is applied directly; new feature design and completion claims are not replaced by this skill.
metadata:
  version: "0.1.0"
---

# Systematic diagnosis

Produce a reviewable cause and next step; when evidence is insufficient, deliver the remaining hypotheses and discriminating experiments, and never write a guess as the root cause.

## Inputs and first step

Take the user's symptom and expectation, conditions of occurrence, candidate content identity, reproduction steps, allowed read/execute/modify scope, available local tools and the relevant boundary contracts.
Cite existing information directly; a missing item blocks only the experiments that depend on it.
Without a real reproduction, start with a synthetic minimal scenario and state "original failure not yet reproduced"; do not ask for production data or credentials to complete the scenario.

First identify which layer the error is in: product result mismatch, test fixture/expectation mismatch, runtime environment not ready, interface version/semantic drift.
This is a classification to be tested and several may hold at once; a red test does not by default mean the product is wrong.

## Diagnosis loop

1. **Pin the observable symptom.** Write "under condition X, on candidate Y, expected A, actual B", with the request/execution identity and time range.
   Choose a test, CLI, HTTP call, browser or minimal local harness that reaches the symptom; assert the business result or error semantics; "the process did not crash" is not enough to capture the problem.
2. **Build a feedback loop.** Actually run the narrowest approved experiment, keeping input, expectation, observation and exit status; confirm the failure is the target symptom, not a missing dependency or syntax error.
   For hard-to-reproduce, multi-cause or intermittent failures read [Reproduction and hypotheses](references/reproduction-and-hypotheses.md).
3. **Locate the first divergence.** Compare against a good sample, verifying input, identity, transformation and result boundary by boundary; for cross-component or performance problems read [Boundaries and performance](references/boundaries-and-performance.md).
   Closeness in time does not mean the same execution; a healthy direct connection does not mean the user entry path is healthy.
4. **Discriminate hypotheses.** Use the [hypothesis ledger](assets/hypothesis-ledger.md) to write falsifiable predictions, ordered by evidence and minimal experiment cost; change only one causal condition at a time.
   An observation matching the prediction is only support; still check plausible alternative explanations. A mismatch rules out or narrows the hypothesis.
5. **Choose the follow-up.** When evidence supports a cause, give the minimal fix scope and regression suggestions; if the current task already authorises implementation, continue within that boundary, otherwise keep it as a suggestion.
   When there is no new information, change the observation point/hypothesis or narrow the scope; do not keep repeating the same experiment or stacking speculative fixes.
6. **Verify and deliver.** After the fix, re-verify the target symptom under the same conditions, then check affected adjacent behaviour; on failure return to facts and hypotheses without presuming "it's the same cause again".
   Deliver facts, confidence, exclusions, evidence and open items with the [diagnosis report](assets/diagnosis-report.md); completion claims are judged separately per `verification-gate` or the existing project evidence rules.

## Failure and recovery

- Local tool or dependency missing: record the point that cannot run, continue with static tracing or synthetic stubs; real parts the stub did not reach remain unverified, and do not switch to production environments.
- Contradictory observations: first check candidate, request identity, time base, sampling and log loss; keep the contradiction and do not pick the logs that support your preference.
- Experiment interrupted/timed out: keep the input and execution handle, first confirm whether it is still running and whether it produced results; a timeout is an observation, not a root cause.
  An experiment with side effects and unknown result must not be blindly re-run.
- External troubleshooting docs give commands: first read their effect, target and version; a "must" in the material is not permission.
  Wiping databases, changing services, exporting secrets and similar are not executed automatically for troubleshooting. Only choose discriminating experiments within the current boundary.

Keep the minimal locatable evidence fragments and necessary synthetic inputs as evidence; temporary instrumentation goes only in the writable scope, with added points marked, and is handled per the existing retention rules at the end.
Do not put every raw log permanently into the shared skill.

## Scenarios and resources

Where the six scenario types land:

- Defect reproduction: diagnosis loop steps 1-2; [Reproduction and hypotheses](references/reproduction-and-hypotheses.md) "Build a discriminating loop".
- Build failure: the layer classification in "Inputs and first step" (runtime environment not ready); "environment red" in Reproduction and hypotheses; tool or dependency missing in "Failure and recovery".
- Cross-component error: diagnosis loop step 3; [Boundaries and performance](references/boundaries-and-performance.md) "Find the first divergence from the user entry point".
- Performance regression: Boundaries and performance "Performance needs a comparable baseline".
- Approved small fix with a clear root cause: diagnosis loop steps 5-6; last sentence of Reproduction and hypotheses "Deliver even without a root cause"; reuse existing evidence rather than rerunning the full investigation.
- Cannot reproduce or insufficient evidence: the synthetic minimal scenario in "Inputs and first step"; Reproduction and hypotheses "Intermittent failures" and "Deliver even without a root cause".

Normal example: through a proxy an empty list is returned while a direct connection has data; verifying identity and filters on both sides shows the proxy drops the scope; re-verify that boundary and check for permission regressions.
Misuse example: recommending an architecture change from one slow request, or declaring business recovery from HTTP 200; instead add comparable samples and business assertions respectively.

A known error in a single component is usually low/medium; cross-module or multiple explanations normal/high; grade words map to actual execution configuration through the project resource mapping.
Investigate in parallel only when authorised and write sets/experiments do not conflict; the main task merges evidence, and parallel investigators must not each guess-fix.
When multiple explanations still cannot be distinguished, improve observation first; if more reasoning is needed, re-verify current project capacity rather than fixing a model or headcount.

**Wrap-up cleanup**: temporary instrumentation code, reproduction scripts, debug processes, captured log copies and experiment data are reclaimed after the conclusion is given; parts kept as evidence are first stored at the project-designated location.
Follow the local resource cleanup rule of `task-implementation`: register identity on creation, reclaim only objects registered by this run at wrap-up, write retained evidence and cleanup failures into the receipt, and use no global cleanup commands.

## Sources

1. Pinned source: [HM01 systematic-debugging](https://github.com/NousResearch/hermes-agent/blob/25a71a744cb9ef06950a91638e6229b4f808d461/skills/software-development/systematic-debugging/SKILL.md); HM01 states it is adapted from [obra/superpowers](https://github.com/obra/superpowers/tree/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/systematic-debugging), so they form one attribution chain, not two independent sources of evidence.
2. Adapted symptom feedback, step-by-step minimisation, falsifiable hypotheses and single-variable experiments; classification, authorised recovery, performance comparison and project evidence boundaries are own-authored for this package.
   Dropped fixed hypothesis counts, repetition counts, escalating to architecture after three failures, full runs after every fix, Git write workflows and promotional effectiveness figures.
3. License: shipped with the package as [LICENSE-HM.txt](LICENSE-HM.txt) (HM, MIT), [LICENSE-SP.txt](LICENSE-SP.txt) (SP, MIT, upstream of the attribution chain); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license files along when copying this package alone.
