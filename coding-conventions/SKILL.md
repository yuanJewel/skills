---
name: coding-conventions
description: Choose and apply project code conventions within a decided implementation, refactor or review scope, separating formatting, conventions, semantic defects and design trade-offs. Does not automatically switch formatters or tech stacks, or refactor the whole repository.
metadata:
  version: "0.1.0"
---

# Choose and apply code conventions

Make the current change match the project's real conventions while keeping language semantics and necessary exceptions.
Convention advice does not replace the defect conclusions of `change-review`, and does not grant write permission outside scope.

## Establish the basis first

Inputs:

- The scope of this change.
- Project formatting/lint/type configuration and the actual commands.
- Language/framework version.
- The nearest similar implementations.
- Approved exceptions.

Read the configuration first, then check author code with the same responsibility. Generated files and vendored third-party copies are not free to edit by hand.

Order of authority:

- Formatting follows the current tool configuration.
- Conventions rest on explicit project conventions and stable similar implementations.
- Semantic correctness is judged by the current language/framework contract.
- When convention and semantics conflict, give the concrete runtime impact and evidence; do not silently change configuration, and do not treat old code as an absolute standard.

Missing inputs:

- No project conventions -> follow the nearest similar pattern.
- No version/semantic evidence -> mark pending verification.
- No formatter or checker -> do not introduce new tools for a style task; mark the corresponding check unverified.

## Steps

1. **Classify findings.** Split into formatting, naming/organisation conventions, semantic correctness and design trade-offs.
   Note the rule source and location for each; "I prefer" must not be written as a defect that must be fixed. Artefact: a classified list with sources.
2. **Verify naming, boundaries and errors.** Per [Naming, boundaries and errors](references/naming-boundaries-errors.md), verify that names express domain and unit, interfaces are clear, errors keep their cause, and concurrency has cancellation and resource release.
   Route language details by package name: Go to `go-patterns`, Vue to `vue3-development`.
   For Python and other languages without a general conventions package in the library, follow the project lint/type-check configuration; do not push another language's style at the general layer.
3. **Choose the smallest clear implementation.** Reuse existing stable contracts; do not build extension points for needs that have not appeared.
   For similar code, first compare behaviour, side effects and lifecycle; do not extract two unstable similarities into a complex shared layer for DRY.
   Whether to split a function depends on responsibility and cognitive load; line count is only a project tool metric, not a universal law of correctness.
4. **Handle comments.** Per [Comments and exceptions](references/comments-and-exceptions.md), keep business reasons, protocol constraints and compatibility notes; correct false or stale comments.
   Execution records that only serve the session go to the collaboration-record location designated by the project.
   Legitimate AI product terms, Chinese punctuation, licenses and necessary incident background are not deleted by keyword; semantic trace review goes to `ai-trace-audit`.
5. **Change within the write scope.** Change only the approved write scope; verify the targets and side effects of auto-format commands first so they do not traverse the whole repository by default.
   Shared files still have one writer. Problems in generated code go back to the generation source/process; do not patch the generated output to hide the source problem.
   Stop condition: on files without write permission or large unrelated formatting changes, handle per the next section.
6. **Check and record.** Run the project-required format/static/type checks relevant to the change, read the diagnostics, and do not disable warnings in bulk.
   Semantic changes also need relevant behaviour verification; pure copy/formatting changes are checked by actual impact.
   Artefact: the [convention review record](assets/convention-review.md), stating the basis adopted, substantive issues, style suggestions, exceptions, results and unverified items.

## Failure and recovery

When diagnostics disagree with the rules, first verify the tool version, file ownership and configuration override scope.
When a third-party contract forces unusual naming, use a local compatibility exception; do not break the protocol to silence a warning; adapt at the boundary where possible.
On files without write permission or large unrelated formatting changes, stop that part and hand the suggestion to the maintainer, keeping your own valid changes; do not roll back other people's work.

On recovery, compare against the current candidate, earlier checks and exception basis; after related configuration or generation sources change, re-verify the impact; old pass records do not automatically cover the new version.
Mark tools not run as unverified explicitly; "the code looks conventional" is not an actual lint pass.

## Resources and examples

Deterministic formatting/naming checks may use low/low; boundary and error contracts start at normal/medium; contested architecture may use normal/high; grade words map to actual execution configuration through the project resource mapping.
Read-only checks may be split when the host allows and there is no shared write conflict; formatting writes do not run in parallel with implementation on the same file.
A single-file task is not escalated into a repository-wide refactor.

Normal example: follow the project's existing error-wrapping style to keep the cause, and format this change's files per configuration.
Reasonable exception: a Go cache needs lock-protected mutable state and cannot copy "always immutable".
Misuse example: replacing a Vue reactive object with a uniform copy-object rule breaks dependency tracking; verify framework semantics first.
The reference pages also cover Python dynamic boundaries and third-party protocol exceptions.

## Sources

1. Pinned source: [EC03 coding-standards](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/skills/coding-standards/SKILL.md).
2. Adopted KISS/YAGNI, readable naming and comments that explain why; preserving error causes, cancellation, language differences, exceptions and project-configuration-first are own-authored for this package.
   Dropped always-immutable rules, fixed function length/nesting limits, automatic repository-wide reformatting and introducing tools. Concrete language/version facts are supplied by the project.
3. License: shipped with the package as [LICENSE-EC.txt](LICENSE-EC.txt) (EC, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license file along when copying this package alone.
