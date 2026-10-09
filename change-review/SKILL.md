---
name: change-review
description: Review whether a specified candidate change meets requirements, correctness and project standards, binding the content identity of new files, modifications, deletions and generation sources. Use for delivery re-review or an explicit change review; does not replace implementation, release approval or a full-repository security audit.
metadata:
  version: "0.1.0"
---

# Candidate change review

Produce review conclusions that are locatable, reproducible and tied to the actual candidate. Specification compliance and code quality are two axes: passing one cannot mask a gap in the other.

## Determine inputs and boundaries

Needed: project root, user-specified candidate scope, approved specification and its version, applicable project standards, a readable baseline and actual verification evidence. Obtain material through the workspace's existing entries; do not default to reviewing only HEAD or only committed files. User-specified WIP, new files, deletions and generation inputs/outputs are all candidates.

- No root or scope given: locate an explicit object first; never recursively scan an unbounded directory to guess scope, and never sign a coverage conclusion.
- Missing specification: code correctness and existing project standards can still be reviewed; mark the specification axis "insufficient material" and never invent requirements.
- Missing old version: the current content can be reviewed; deletion impact and compatibility differences are marked unverified.
- Secret paths: list them as excluded with a reason that contains no secret; never read the content to decide whether it is secret. Extension rules are not complete secret detection; the caller must provide the list of known secrets.

## Pin the candidate and review

1. First read the [candidate and review contract](references/review-contract.md) and settle each path's kind, generation relation and exclusion reason. Manually check for omissions against the requirements, the delivery list and existing change lists; the script does not discover unlisted new files.
2. Capture the explicit scope with the [read-only candidate script](scripts/candidate-manifest.py). Identity is produced only when two content reads agree; if unstable or a read fails, resolve the input or wait for the writer to finish. The manifest does not lock files and does not prove full-repository coverage.
3. Specification axis: link each requirement -> implementation -> actual evidence; look for missing, partial and out-of-scope implementation. Standards axis: follow the call chain for error propagation, permissions, boundaries, concurrency and resource release; expand only the technical topics this change affects.
4. Each issue needs file/line, trigger condition, actual vs expected, impact, evidence, minimal fix and confidence. Doubts that cannot be reproduced are marked pending verification; code smells are suggestions only and cannot force refactoring on preference alone. For style issues already checked automatically, citing the tool result is enough.
5. After review, recapture and compare with the previous manifest. When content or scope changed, analyse affected paths and dependencies, invalidate the corresponding conclusions and re-review; before that analysis, never call the whole package passed.
6. Use the [review receipt](assets/review.md) to summarise both axes, actual runs/static analysis/unverified items and the candidate identity. With no findings write "no confirmable issue found in this scope"; with an empty scope write "no reviewable candidate", which does not mean all requirements are implemented.

Review authorisation does not include fixing, Git writes, running generators or releasing. Even when an existing task authorises fixes, re-pin the candidate after modification. Sensitive boundaries needing a specialised review may combine with security-review; admission of verification evidence may combine with verification-gate; a simple review needs no other package installed.

## Recovery, resources and examples

On interruption keep the scope, both candidate identities, files read and unfinished issues. On recovery first verify whether the old execution is still writing and recapture the candidate; an old pass cannot be reused directly. An independent review should be done by a person or execution unit not involved in authoring; author self-review must be labelled explicitly; whether to delegate depends on user authorisation and host capability.

Mechanical scope checks suit low cost and lighter reasoning; ordinary change review uses standard capability with deeper reasoning; raise it for concurrency, authentication, compatibility or conflicting evidence according to complexity. Split independent read scopes by candidate dependencies; do not force multiple execution units by file count.

Normal example: a new handler is added, an old route deleted and a generation input modified; all three plus the generated output are in scope; locate an old caller still using the deleted route and give the triggering request and minimal fix.

Counterexample: an existing function is slightly duplicated but meets an explicit project convention; it must not be reported as a blocking defect. Another counterexample is halting the whole review for a missing specification; the correct approach is to complete the reviewable axis and keep the specification gap.

## Sources

1. Pinned source: [MT01 code-review](https://github.com/mattpocock/skills/blob/b0618bc436ad893b3c5e84e55fba86586d34a404/skills/engineering/code-review/SKILL.md).
2. Adopted the specification/standards split, project standards first, and smells as heuristics; the candidate script, missing branches, evidence invalidation and templates are own-authored for this package.
   Dropped the fixed HEAD diff, mandatory tracker and mandatory parallel subtasks. On upgrade, re-verify the adopted scope; script changes require rerunning the synthetic boundary cases.
3. License: shipped with the package as [LICENSE-MT.txt](LICENSE-MT.txt) (MT, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license file along when copying this package alone.
