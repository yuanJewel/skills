# Meaning and applicability of execution evidence

## Evidence first answers "what does it prove"

| Evidence | Can support | Does not automatically support |
| --- | --- | --- |
| Artefact exists, content review | The specified change was produced; the reviewed static properties | Successful compilation, correct business behaviour |
| lint/format check | The static rules the tool actually checked | Build, tests, end-to-end |
| Build exited successfully plus artefact identity | The specified inputs build successfully | Correct behaviour; that the runtime uses this artefact |
| preflight/plan printout | Prerequisites checked, plan contents | Test execution, deployment or traffic cutover |
| Unit/contract/local simulation | Assertions hold under the corresponding conditions | Untouched layers or real external service behaviour |
| Full-suite report on a pinned candidate | Results of the listed set under those conditions | Human acceptance, production release or later changes |
| Human acceptance record | The scope the named person explicitly accepted | Other candidates, other environments or technical evidence gaps |

Check whether the path the claim needs was actually reached.
For example, a fake API returns success and the browser displays correctly: this only proves the page consumes the mocked response, not real backend persistence, permissions or async job final state.
A human saying "looks fine" also cannot rewrite an unrun test as passed.

## Exit codes are not a universal success signal

Read the tool's execution semantics, final state, report counts and target assertions together.
For an unfamiliar tool, check its version/help or the existing contract first; do not borrow another tool's exit-code semantics.

| Symptom | Handling |
| --- | --- |
| Exit 0, 0 cases collected | If the task requires tests, nothing is proven; check discovery rules, paths, filters and the expected set; if zero items genuinely applies, record the reason separately, never report a fake run. Tool semantics differ: `go test` exits 0 with no tests; pytest exits 5 when no tests are collected; Jest fails by default with no tests and exits 0 only with `--passWithNoTests` |
| All or some skipped | Verify the condition per item; missing prerequisite is BLOCKED, only contractual non-applicability is N/A; the other executed items may pass individually |
| Outer script/pipeline exits 0, inner check failed | Take the real status of each necessary stage or the machine report; the last pipeline stage's status does not represent earlier stages. When rerunning, invoke the affected check directly or use an exit-propagation method confirmed to be supported |
| Timeout, tool returns a session/handle | Execution may still be in flight; verify the real final state and completed shards. A timeout only means observation was interrupted; infer neither test success nor failure |
| Output truncated or only the tail received | Locate the saved full report and verify summary, failures and set; if the key range cannot be read, keep the gap, and do not use "saw no errors" as evidence |
| Succeeded on one retry | Keep the first failure, the attempt conditions and later results; if the difference is unexplained mark it flaky, do not selectively erase failures |
| Subtask self-reports "all passed" | Verify the full set of artefacts, candidate, commands and results; the receipt may serve as an index but cannot replace evidence |

Read evidence within bounds: inventory and summary first, then locate raw fragments by gap, limiting long output by both lines and bytes.
Abbreviated display does not mean key checks were skipped; when a report stores the full results, cite its location without copying the whole log into the reply.

## Current candidate and old evidence

The candidate identity must map to actual content: source tree/change set or content digest, build artefact and relevant dependencies.
When it includes uncommitted fixes, a commit ID alone does not represent the candidate;
if the running binary comes from elsewhere, looking only at the working directory cannot establish that the new code was tested.

Before reusing evidence, verify four things: the tested behaviour/acceptance is unchanged; relevant files/generated artefacts and dependencies are unchanged;
environment/fixtures are still compatible; the original execution was complete and valid.
If any is unclear, block only the claims that depend on that evidence.
You may say "check X on the old candidate still applies, because this change only touches Y, which X does not depend on"; you may not change the candidate field of an old report to the new version.

When a change affects a shared interface or consumers are hard to bound, widen verification to the possibly affected parts.
Elapsed time or a session switch alone does not invalidate static evidence;
volatile facts such as real service state, permissions and external dependencies are re-verified according to the claim's freshness needs, not replaced by a long-lived cache.

Example: after changing help text, reusing unaffected pure-algorithm results is justified; after changing the serialisation library, reusing old interface-compatibility results is usually not.
A change in build/runtime dependencies can invalidate the corresponding evidence even when source is unchanged.

## Aggregation, failure and correction

Map item by item against the acceptance set; do not hide key omissions behind pass counts or pass rates.
N/A is an applicability judgement and must be distinguished from execution results; a required item cannot be removed from the set because a tool skipped it.
One goal can have a partial PASSED and another item BLOCKED at the same time; its overall scope is still incomplete.

When an earlier conclusion turns out too broad, explicitly correct the claim, giving the reason, the valid part and the re-verification scope, and keep the old evidence as history;
never silently edit history to make it look accurate all along.
If an artefact seems to be generating but has not been returned, verify in-flight work and file integrity first; do not seize the same write set.
Output results carry no release permission; later actions still go through the corresponding boundary.
