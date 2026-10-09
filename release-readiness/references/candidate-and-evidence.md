# Candidate identity, evidence and change

## Pinning a candidate is more than recording a name

The identifier must map to the content actually verified:
source tree or content digest, build artefact identity, dependency lock/generated artefacts, configuration structure version, runtime image and necessary environment characteristics.
Uncommitted fixes must be included in the candidate; a single commit ID cannot represent all the content; a mutable tag must be resolved to the actual immutable identity.
An identical directory name does not establish that the binary was updated.

When testing, verify that "source content -> build artefact -> running instance -> candidate in the report" is consistent.
A missing link of evidence is listed as a gap for that claim; do not paper over it by renaming the report.
No Git write or new worktree is required here; follow the project's existing candidate mechanism.

When other writers exist while the candidate is pinned, make the sole writer and change notification explicit: a changing directory must not be treated as frozen input at the same time.
Without locking capability, verify the content identity before and after; on finding a change, mark the affected reports pending verification. Do not claim this provides a transactional snapshot.

## Verify the necessary evidence by project risk

Not every project must fill every category; first state why a category is required or not applicable. Applicable items need an evidence source or an explicit gap.

| Category | What to verify | Common shortfall |
| --- | --- | --- |
| Requirements and review | Acceptance set, review scope, known defects and their disposition | The author says "fixed" but the review issue was never re-verified |
| Build and candidate | Artefact provenance, dependencies/generated artefacts and the runtime are consistent | The workspace has the fix, the tests still run the old image |
| Local full suite | Expected set, complete set of shards, environment, valid final state, failures/reruns | Reading only the overall exit code; missing shards or skips counted as passed |
| Data/configuration/permissions | Applicable compatibility, migration prerequisites, structure validation and rejection paths | Only normal requests verified; configuration notes taken as proof of a correct real deployment |
| Health and critical paths | Separate targets for liveness, readiness and business assertions; failures observable | health 200 standing in for business success/complete state |
| Recovery capability | Availability of the previous version/artefact, rollback prerequisites, data compatibility and a synthetic drill | Treating switching the binary back as making all data reversible |
| Human and external | Acceptance object, scope, real behaviours still to be executed and responsibility | Local printouts/simulation posing as traffic cutover or user acceptance |

A recovery plan states at least the trigger condition, the executing party, prerequisites, stop/observation points, the expected final state and irreversibility limits.
Simulation verifies the permitted paths; it does not obtain production credentials or execute a real rollback.
Where irreversible data migration is involved, state what can be recovered, what cannot and which further human decision is needed; do not promise "switching back the image restores everything".

## Deciding on acceptance changes

Keep the original candidate, original evidence and original human decision, and record the new candidate and the change set.
Propagate impact through callers, shared interfaces, data, permissions and generated inputs; do not judge by changed line count alone.

| Change | Retest and re-review suggestion |
| --- | --- |
| Static copy/style only, proven not to change behaviour/build semantics | Content, links, necessary page/accessibility checks; reconfirm the affected human items, keep unrelated full-suite evidence |
| Local business fix with a clear impact boundary | Targeted regression and related integration; re-verify the original defect/acceptance item, reuse other evidence with an applicability statement |
| Authentication/authorisation, shared protocol or persistent state change | Permission rejection/out-of-scope access, consumer compatibility or state recovery and critical paths; re-review where necessary, never skipped as "just a one-line change" |
| Large candidate change, runtime dependencies/environment no longer equivalent, impact unclear | First assess the boundable scope; when an additional full suite is needed give reason, set, resources/duration and prerequisites, then execute under existing authorisation |

With no change, or evidence still valid, do not run a second full suite out of habit because human acceptance started or the session changed.
An additional full suite is not a way to cover up defects; fix first or make the blocker explicit, and avoid endlessly repeating the same invalid run.
