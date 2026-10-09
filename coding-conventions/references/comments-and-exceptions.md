# Comments, exceptions and false positives

Read this page for comment cleanup, rule conflicts or static-check exceptions.

## What comments should keep

Keep information the code cannot express directly but maintainers need: business reasons, third-party protocol constraints, algorithm invariants, performance trade-offs, failure-recovery boundaries.
Parameters/returns/errors/side effects of public interfaces are documented per language and project conventions, not just "does some feature".
After changing behaviour, update the comments; when a comment conflicts with code, verify the real contract first rather than deleting the comment by default.

Good: "This vendor treats an empty string and an omitted field differently, so the empty value is kept." Bad: "increment count" right next to `count++`, adding no information.
Necessary incident background may briefly state the constraint that prevents recurrence and link the long-term issue record; do not write session logs, model attribution or this task's number.
Which collaboration-process content is banned from product files is a project-policy input; do not expand the banned-word list on your own.

Chinese punctuation, natural-language comments and legitimate AI product names do not prove AI generation and are not traces to delete.
Copyright licenses, third-party requirements and real business fields are kept even if they contain the word AI.
If content only serves the current session (e.g. "model X fixed this in this round"), move it within the authorised scope to the collaboration-record location designated by the project; do not mix it into business logic.

## Exception decisions

1. Find the exact rule, applicable tool/version and warning location; confirm it is not a misread configuration or a check of generated files.
2. State the concrete problem following the rule would cause, such as breaking third-party fields, wrongly changing reactive updates, or losing a necessary compatibility branch.
3. Prefer local adaptation or more accurate types/structures so the semantics are correct and still checkable.
   When suppression is truly needed, use only the project-allowed form at the smallest scope, with the reason and removal condition.
4. Record the exception basis, impact, verification and review condition; do not disable rules in bulk or change repository-wide configuration to hide this warning.
5. When a rule conflicts with language semantics and cannot be safely resolved locally, give the maintainer a concrete counter-example and options; stop the conflicting change until decided, and continue other authorised items.

A reasonable exception is not exempt from verification: compatibility fields need contract or caller verification, mutable state for performance needs ownership/concurrency evidence.
An exception the user already approved is consumed within its scope and conditions without asking again; re-verify when conditions change.

## Impact categories

- Formatting differences: tool-determinable; affecting only presentation, usually not reported as a runtime defect.
- Convention suggestions: improve understanding; state the rule source and benefit, without pretending there is a bug.
- Semantic defects: give the trigger, expected, actual and evidence; hand to `change-review`.
- Design trade-offs: list benefit, cost, callers and compatibility impact; out-of-scope suggestions wait for the current process and are not implemented automatically.

A single-file naming task does not bring a repository-wide refactor along.
When tool output adds many diagnostics, first separate what this change introduced from existing issues, then decide the necessary verification and report.
Do not count all existing debt as this change's failure, and do not use "historical issue" to mask impact this change made worse.
