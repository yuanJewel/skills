# Plan review report

- Object: {{plan location, version/content identifier; identifiers before and after review and whether they match}}
- Type: {{author self-check / independent review; reviewer and whether they took part in writing}}
- Scope: {{goal, original requirements/approval source, evidence read; state the uncovered parts explicitly}}
- Conclusion: {{pass / has blockers / pending evidence; one sentence on what it means for the next step}}

## Requirements and scope check

| Original requirement/constraint location | Corresponding plan task/acceptance | Current evidence and status | Omission or added cost |
| --- | --- | --- | --- |
| {{exact location}} | {{task/acceptance location}} | {{CONFIRMED / UNVERIFIED}} | {{omission or cost; state if none}} |

## Findings

Write each as an independent, actionable issue; order by impact, not by review time spent.

- Issue identity and level: {{blocker / non-blocker / pending evidence}}
- Location and trigger: {{version, file/section, concrete input or state}}
- Difference: {{what the original requirement expects, what the current plan arranges}}
- Impact: {{behaviour that would fail, scope overstepped or added cost}}
- Evidence status: {{CONFIRMED / UNVERIFIED; evidence location and missing items}}
- Suggestion: {{minimal fix and trade-offs; who must decide or rewrite}}
- Re-verification: {{how to prove the issue is gone, which adjacent items need re-verifying}}

## Four-dimension coverage and remaining unknowns

Briefly note what was verified for architecture, quality, testing and performance; give a reason for any not applicable.
Keep existing implementation and proposed additions separate; commands not run, unknown scale or missing protocols cannot be filled in as pass.

## Rework and handover

List open items, writer, recovery conditions and next step. If the original plan changed, state the applicable scope of the old conclusions.
The report only suggests; it does not replace user approval or rewrite the plan.
The project's overall status and the user's pending-decision entry reference this report and do not copy it into another plan.
