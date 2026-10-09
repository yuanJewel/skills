# Review and evaluation

Review a pinned candidate without changing the reviewed object. Derive expectations independently from the design goal or user requirement; never use the author's output as the reference answer.

## Separate evidence levels

| Level | What is actually done | Conclusion it supports |
| --- | --- | --- |
| Static check | Really parse frontmatter/Markdown, check paths, actually run script fixtures | Format or deterministic script passes on the tested inputs |
| Content walkthrough | A person/model reads the method against a given scenario and derives the branch to take | Analysis of method coverage/conflicts; does not prove the host will execute it |
| Actual behaviour | Send real requests to the target host in a permitted isolated workspace, keep tool traces and artefacts | Actual result for that host/version/configuration/candidate and the tested scenarios |
| Independent comparison | A person or agent not involved in authoring evaluates candidate and baseline from minimal raw input | Relative effect under that evaluation design; not a generalisation guarantee for all tasks |

First record candidate file digest, host and version, inputs, available tools, licensing side effects, judging criteria and output location. With no host available, complete the static/content parts and state clearly that actual behaviour is unverified; never accept a fabricated skill list, script printout or "I will read it" as successful discovery.

## Decision points in content review

Check whether triggering yields the artefact the user needs; whether incomplete input stops only dependent actions; whether the three modes are blurred into design-then-automatically-modify; whether source commands are turned into permissions; whether supporting pages really support failure recovery; whether cross-package references only consume contracts; whether output is bound to this candidate. The independent reviewer first writes concrete findings and impact, then gives severity, avoiding a generic "suggest adding more tests". When only wording differs and behaviour is the same, do not block.

Every strong conclusion from the author needs matching evidence. In particular "compatible", "passed", "in effect" and "independent" each need corresponding verification; a format pass does not support these conclusions. List execution-validity problems separately: empty test set, only exit code zero, all cases skipped, assertions copied from the implementation, environment failure disguised as product failure, etc.

## Trigger and behaviour cases

Organise a small number of discriminating inputs from real work, covering different phrasings, localised (e.g. Chinese) entry points and implicit needs; negative cases use the same keywords with a different goal, not completely unrelated requests that inflate accuracy. Fix the development set and held-out set first, then optimise the description. With small samples report per-case observations and the denominator; do not give a seemingly precise generalisation rate.

| Input and preconditions | Action/evidence to observe | Valuable misuse counterexample |
| --- | --- | --- |
| "Design a skill split proposal", library entry exists | Outputs a design; target package tree digest unchanged before and after | Initialises the whole package directory along the way |
| "Review this version of the skill", author has stopped writing | Read-only report bound to pinned bytes; findings not fixed on the reviewer's behalf | Passing the fixed package as the original candidate |
| "Update package A within approved scope", package B is a dependency | Only package A changes; B's interface gap recorded | Directly changing B or the shared index to fix a broken chain |
| "Process data with the existing report skill" | Completes the business task without maintaining skills | Changing the description because the word skill appeared |
| Two projects reference the same original, one session already loaded the old version | New session/new phase records the version read; upgrade impact explicit | Treating the new version on disk as refreshed in all sessions |
| Real broken link in package, reference-style link, fake link in a code block | Real parsing checks only actual links; broken link fails | Regex mistakes a code example for a reference, or misses reference-style links |
| Model does not support a reasoning tier/metadata field | Records the capability gap; does not fake effect or switch service provider on its own | Signing the parameter as effective only because the call did not error |
| One external source Apache, another MIT | Each pinned version and notice ships with the distribution | Unifying to the author's preferred license |

These are executable evaluation designs, not run results. Scenario results go to task evidence. When the method is complex, evaluation may be split into its own file; short cases stay here; do not create new files to pad the count.

## Composition and cross-project

Choose real dependency relations, e.g. this package's design consumes an existing plan, and after an upgrade the archiving method preserves the old candidate. Give the evaluator the entry and necessary raw data without hinting "how many skills should be invoked"; observe whether the original user goal is lost, templates are duplicated, clarification repeats or permissions override each other. A small task must not turn into a mandatory whole-library audit because of composition.

Cross-project use takes two independent roots with different entries/parameters: one side has named roles, the other only the default duty; paths and semantics both differ. Verify the package reads no absolute paths of the old project and has no fixed role/model/resource values; let one side lack an optional tool and confirm the gap affects only dependent actions. When real consumers are insufficient, a synthetic workspace may prove portable input handling, but it must be marked synthetic and cannot sign a real installation success.

## Comparison, failure and delivery

With authorisation and the ability to run independently, run the old version/no-skill baseline and the candidate on the same input; keep resources, tools and environment as consistent as possible, and avoid leaking version preference through order/naming. Record artefact correctness, out-of-scope actions, failure recovery, necessary interaction and actually available usage; repeat observations for variance when needed. Without independent conditions, do not apply the independent label.

On failure first keep the original input/trace, then classify as not discovered, false trigger, method defect, script error, environment/capability shortfall or evaluation-design problem. After fixing, re-verify the related normal and negative cases; never delete failing cases to fit the result. Close the report as "blocking/non-blocking/unverified", listing reproduction conditions, evidence location, impact and minimal fix suggestion. An author revision forms a new candidate; old pass conclusions are reused only within scope provably unaffected.
