# Test scope for this change

Embed into the test part of the existing plan; do not generate a second overall plan. Scope/candidate: {{changed behaviour, candidate identity, approved acceptance reference}}.
Risk rationale: {{L0-L3 suggestion and the concrete failure consequence; no quality score}}.

| Behaviour/acceptance | Failure mode | Minimal effective layer and reason | Independent assertion | Fixture/dependency boundary | Cases/evidence |
| --- | --- | --- | --- | --- | --- |
| {{behaviour}} | {{how it would go wrong}} | {{which layer can catch it}} | {{expectation source and observable result}} | {{data ownership/stub limitations}} | {{stable ID and location}} |

Untested items and reasons: {{basis for no impact / already covered by a smaller layer / excluded from this phase}}.
Still required but not covered: {{missing prerequisite, items to add and impact; do not disguise as N/A}}.

| Shard | Prerequisites/mutually exclusive resources | Execution conditions and output ownership | Estimated time/resource basis | Status and first-run/rerun evidence |
| --- | --- | --- | --- | --- |
| {{set}} | {{dependencies, environment locks}} | {{entry point, version, data/directory}} | {{range and samples; state unknowns explicitly}} | {{not run or PASSED/FAILED/BLOCKED/N/A}} |

Completion criteria: {{no omissions from the planned set, valid final states and independent assertions; basis for N/A}}.
Recovery/change: {{in-flight verification, contaminated items, retest scope after candidate/acceptance changes}}.
Simulated/real limitations: {{what can be proven locally, what is verified later}}.
