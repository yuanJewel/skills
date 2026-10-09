---
name: plan-review
description: Review a designated design or pre-approval plan against the original requirements, checking scope, architecture, quality, testing and performance, and report evidence-backed blockers and unknowns. Does not implement the plan and does not write a second plan on the author's behalf.
metadata:
  version: "0.1.0"
---

# Plan review

Judge whether the current plan is sufficient to enter its declared next step.
The review result is separate from user approval: technically feasible does not mean implementation is authorised; author self-check does not mean independent review.

## Pin the object and evidence

Obtain the target plan, version/content identifier, original requirements and decision sources, current facts, task boundaries, the report location and its owner.
First record the identifier of the reviewed body, and verify at the end that it has not changed.
If the author updates it during review, the report marks the old version and re-verifies the affected items; old conclusions are not applied to the new file.

Without an exact target, locate it first; confirm in one batch only if several candidates remain.
Without the original requirements, internal consistency can still be reviewed, but "are requirements missing" is marked pending evidence;
when key interface, permission or recovery facts are missing, do not guess a pass.
The reviewer writes only its own report and does not change the reviewed plan or code. If the user wants an implementation diff reviewed, use the method of `change-review`.

## Review order

1. From the original requirements, list the behaviours, boundaries and acceptance that must be achieved, and point each to the corresponding plan section.
   Separate user requirements, author suggestions, existing implementation and assumptions pending verification; identical names do not prove identical semantics.
2. Challenge scope and premises: what minimal change achieves the goal, which existing capabilities can be reused, which work the plan newly adds.
   Verify the reused object's real inputs/outputs, errors, permissions, side effects and deployment boundaries; "the plan intends to add a caller" cannot pose as "the code already has a caller".
   For optional extensions found, give a suggestion; do not write them into the approved scope yourself.
3. Check architecture, code quality, testing and performance per the [review dimensions](references/review-dimensions.md).
   A simple plan may merge the narrative or mark a dimension not applicable with a reason; do not expand the task to fill sections.
   Cross-interface, state-changing and irreversible paths need failure and recovery spelled out.
4. Try to disprove each suspicion: check the real files/interfaces and original decisions, construct a concrete input or state that triggers the problem, then judge impact.
   Mark confirmed facts `CONFIRMED`; mark insufficient evidence `UNVERIFIED` and list what is missing. Model agreement, report titles and high-confidence wording never upgrade anything to fact.
5. Use the [report template](assets/review.md) to record location, trigger, expected vs current plan difference, impact, evidence and minimal suggestion.
   List as blockers only problems that would prevent the goal/acceptance, cross the approval boundary or create substantive risk; keep format preferences and optional optimisations separate.
6. Choose the conclusion "pass / has blockers / pending evidence" and state the coverage. Suggestions may carry trade-offs; plan changes are decided and written by the original writer.
   After rework, re-verify only the affected requirements, interfaces and evidence; fixing one problem must not drop earlier open items.

## Failure and recovery

The original plan changes, the original requirements are lost or environment evidence is unavailable:
keep the current results and the exact version, suspend conclusions that depend on that evidence, and continue checking the independent parts.
The report states the missing evidence, its impact and the recovery condition; do not create a new plan to fill the gap.
For conflicting rules, list both locations and their applicable scope and hand them to the existing decision process; necessary checks that are already explicitly authorised are not asked again.

The output is an independent review report and a locatable issue list; the plan body stays with `plan-design`.
Current status/user pending decisions consume the conclusion through `context-handoff`; this package builds no separate user workbench.
Without the companion packages, follow the project's existing contract.

## Resources and examples

Independent review starts at `normal/high`;
when multiple contracts are crossed or failure states are complex, raise to `normal/xhigh` if the concurrency quota in project configuration allows, preferring to verify evidence in segments.
Grade words map to actual execution configuration through the project resource mapping.
Pure formatting cleanup needs no high-cost review or extra agents; independence means not having actually taken part in writing.

Normal example: the approved goal is a new query; the plan reuses the existing permission gateway, specifies empty-result and timeout responses, and has acceptance evidence;
it can pass after checking the four dimensions.
Blocker example: for query convenience the plan adds a data connection that bypasses the authorisation layer; point out the specific layer-skipping edge and the original constraint.
Counter-example: a heading switches to another numbering style without changing meaning; record only an optional cleanup, not a blocker.
Unknown example: another reviewer also says the interface is idempotent, but there is no implementation or protocol evidence; keep it UNVERIFIED.

## Sources

1. Pinned source: [GS01 plan-eng-review](https://github.com/garrytan/gstack/blob/c7edf46bcf6e8d1ccd2f58ffb0800a4e8119e805/plan-eng-review/SKILL.md) and the same version's [review sections page](https://github.com/garrytan/gstack/blob/c7edf46bcf6e8d1ccd2f58ffb0800a4e8119e805/plan-eng-review/sections/review-sections.md), sections Scope Challenge, Architecture, Code quality, Test, Performance.
2. Adopted the scope challenge and the four-dimension structure; two-state evidence, sole writer, version pinning and recovery are own-authored for this package.
   Dropped telemetry, brain, startup scripts, per-issue voting, the fixed-section-count flow, promotional figures and automatic write-back to the plan.
3. License: shipped with the package as [LICENSE-GS.txt](LICENSE-GS.txt) (GS, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).
   Copy the license file along when copying this package alone.
