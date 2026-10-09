---
name: ai-trace-audit
description: Review a specified change for collaboration traces that only serve an AI session, false comments and ineffective template content, giving evidence and reasonable exceptions per the project content boundary. Does not detect authorship and does not automatically delete or rewrite code.
metadata:
  version: "0.1.0"
---

# Collaboration-trace and content-truthfulness check

Separate the business content users need from temporary collaboration records. Judge by purpose and facts, not by the appearance of "AI", model names, Chinese or a particular writing style; this package does not estimate an "AI-generated ratio".

## Inputs and scope

Use the specified candidate list, change intent, project conventions for code/comments/documents and related context you are allowed to read. Candidate identity reuses `change-review` or an existing list, including approved but uncommitted new files; without Git, check by file. Unless a full-repository scan is specified, review only the candidates and necessary related locations.

First identify business source files, generated artefacts, third-party licenses and any collaboration-record location the project designates. If the project designates such a location, collaboration records and this package's audit artefacts go there; the existence of that location is not a violation, and never hand-edit third-party/generated files to strip provenance information.

## Decision flow

1. Filter candidates by the project content boundary: roles/prompts, session IDs, task handoffs, model or tool division of labour, instructions to the next agent, and copied templates lacking business explanation. Keywords are only locating clues and cannot yield a violation verdict directly.
2. For each item ask "which real behaviour does this help product users or maintainers understand". Read the surrounding implementation, call chain, default configuration and provenance; choose the applicable judgment from [Markers and counterexamples](references/markers.md).
3. Verify factual assertions in comments/documents: whether there really is retry, permission checks, encryption, cache invalidation or fault tolerance; whether a default value stated in a comment is the value actually in effect. When the implementation cannot be seen, mark it unverified; never fill evidence with a plausible guess.
4. Check whether suspected empty shells, duplicated templates, assertion-less tests and unjustified defensive code affect the goal. First verify real callers, how it runs and the product fault-tolerance contract, then distinguish missing implementation, legitimate stub, generated code or optional style; do not expand into refactoring for "quality".
5. Use the [audit template](assets/audit.md) to give location, project rule, semantic criterion, real impact and minimal suggestion, and record reasonable exceptions too. With no substantive finding, report no finding directly; do not pad the issue count.
6. At the end, verify the content identity of the candidates. Reviewed files are not changed; fixes are handed to an implementer with write permission per `task-implementation` or the existing process, and changes to behaviour or generation sources are verified per impact.

## Failure and recovery

Without project content rules, clear factual falsehoods or temporary session instructions may still be reported; everything else is listed only as boundaries pending confirmation; never derive a blanket ban on terms. When the generation source cannot be found, record the locating gap; do not delete generated output directly. If candidates change during review, mark the old conclusions and re-verify the related items; sources stay read-only and hypotheses are never tested by temporarily changing code.

An audit may deliver three kinds of facts: "confirmed issue / reasonable exception / clue pending verification"; the overall conclusion depends on whether there is substantive impact. Inference must never be escalated into an authorship judgment or a plagiarism accusation.

## Resources and examples

low/low is for filtering clues within allowed files; normal/high for confirming purpose and code facts; grade words map to actual execution configuration through the project resource mapping. A small check with exact locations already known can be done by the main task. Look at related context by risk; do not dispatch more tasks because there are many keywords.

- Issue example: a business function comment says "hand this to the next Codex session" with no business explanation. If the project designates a location for collaboration records, move it there, and the implementer fills in the actual to-do.
- False-statement example: a comment claims three retries while the real path calls once with no outer retry. Point out the behaviour difference; never add retries on your own.
- Reasonable exceptions: legitimate AI product modules, incident background, algorithm formulas, Chinese explanations, third-party copyright and licenses. None may be deleted on a keyword hit.

## Sources

1. Pinned source: [AD01 code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/1401c8b8030e023baeebb31781a6653fe8e93026/skills/code-review-and-quality/SKILL.md).
2. Borrowed only the Context -> review axes -> Verification -> Verdict organisation and the distinction between evidence and preference; semantic traces, fact checking, false-positive rules and the read-only boundary are own-authored for this package.
   Dropped mutating reviewed code, Git operations, mandatory model combinations and unrelated cleanup; correctness is not inferred from star counts.
3. License: shipped with the package as [LICENSE-AD.txt](LICENSE-AD.txt) (AD, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license file along when copying this package alone.
