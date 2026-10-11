# Material model

Read this page when classifying existing material, deciding where a new requirement belongs, or correcting a file that has drifted from its purpose. It defines the material classes, the authority rule, and the selection and merge rules for `governance/memory/`.

## 1. Material classes

Classify each file or passage into exactly one primary class. The class decides the destination under the [canonical layout](canonical-layout.md).

**Scope comes before class.** Before asking what kind of material a passage is, ask how long and how widely it applies:

| Scope | Test | Where it lives |
| --- | --- | --- |
| One task | Granted, forbidden or approved for a named task or batch ("for this task, do not touch README"; "go ahead with step 2") | `plans/<plan-id>/decisions/`; applied in that task's status and write scope; never copied into governance or memory |
| This project, lasting | Applies to every future task in this project until changed ("from now on no Git writes in this repository") | Governance current text (`policy.md`, `collaboration.md`, `retention.yaml` or a named policy page); if the user adjusted an existing rule, also the matching `memory/<topic>.md` |
| Shared method | Changes how the method works in every project that uses it | The method's own package under its own write authorisation; the project records the request |

A permission granted or withdrawn for one task is still task-scoped material even though it reads like a rule; it does not become a current rule because it uses the words "do not". When the scope is unclear and the choice would change behaviour beyond this task, ask before placing it. Only after scope is settled does the class table below decide the destination.

| Class | Test | Destination |
| --- | --- | --- |
| Current rule | A lasting project-scope statement that changes what the AI may do or how it must operate from now on | `governance/policy.md` or a named policy page; collaboration rules in `governance/collaboration.md`; lifecycle limits in `governance/retention.yaml` |
| Project fact | A verified statement about the project's code, domain, interfaces or terminology that does not grant or withdraw permission | `knowledge/` |
| Active task material | Plan body, status, approval, task-scoped permission or restriction, review or evidence of a plan that is not yet accepted | `plans/<plan-id>/` and its attachment directories |
| User policy adjustment | A conversation in which the user changed, confirmed or corrected a lasting policy, operating rule or maintenance constraint | Current text updated in governance; distilled basis in `governance/memory/<topic>.md` |
| Historical evidence | Original approval, receipt, old status or old rule version that is no longer current but must remain traceable | `archive/` with a record; frozen bytes |
| Rebuildable output | Lint results, scratch restores, rendered views that can be regenerated from sources | Not stored in the root, or kept only under the plan's `verification/` while the plan is active |
| Extension material | Belongs to a declared project extension (release procedure, external sources, test logs...) | The declared extension directory; archived under `archive/` |

Tests in order, after scope is settled: task-scoped -> active task material, whatever its wording. Project-scoped: does it grant or withdraw permission (current rule; if the user changed an existing rule, also a memory topic)? Is it superseded but needed for traceability (history)? Otherwise fact or extension. Shared-method scope leaves the root.

## 2. Authority

Each contract has one authoritative file. Indexes, workbench entries and memory topics may point at it; none of them may carry a second version of the text. When two files disagree, compare the current user instruction, the approved requirement and version evidence; the newer modification time does not decide. Fix the authoritative file and the pointer; do not keep both wordings as "current".

Historical originals are not rewritten to fit a new structure. A frozen approval that links to an old path keeps that link; the archive record or migration table maps the old path to the new one.

## 3. Memory: selection and merge rules

`governance/memory/` is provenance for governance, not a transcript store.

**Record when** a conversation produced one of:

- an effective change to policy, operating rules or maintenance constraints;
- a correction of a previous understanding of such a rule;
- an open disagreement that belongs directly to such a change and needs the user's decision.

**Do not record** ordinary Q&A, task progress, one-off approvals of a task (those go to `plans/<plan-id>/decisions/`), task evidence, round-by-round discussion, or a full backup of the chat. The user speaking does not by itself create a memory entry.

**One topic, one file.** Topics are cut by the constraint they govern (for example `git-operations.md`, `collaboration.md`, `decision-presentation.md`), not by date, session or utterance. Before writing, look for the existing topic; update it. Add a topic only when the adjustment fits no existing one and has lasting meaning.

**Each topic file keeps**, in this order:

1. Current rule — one short paragraph, the distilled requirement as it now stands, with a link to the authoritative current text.
2. Basis — for each adjustment that still matters: date and source location, the minimal verbatim words that carry the decision, the distilled requirement, a one-line reason (what was adopted, why, what it affects or leaves open), and the confirmation state.
3. Open points — only those that need the user's decision and belong to this topic.

Mark verbatim words, summary, AI judgment and user confirmation separately. An unconfirmed AI judgment is not an effective constraint. Quote accurately and only the necessary part; never label a paraphrase as a quotation; when the original wording is unavailable, state the gap.

Merge instead of appending: when the same requirement is restated, update the current rule and keep the basis that still matters; when a rule is replaced, the superseded basis is either shortened in place or moved to `archive/governance/memory/` with a pointer, not left as a growing log. Memory does not expand authorisation: when memory and the current authoritative text conflict, check the user instruction and version, fix the text and the memory, and never derive new permission from an old entry.

### Minimal example

```markdown
# Git operations

## Current rule
The AI runs only read-only Git commands in this repository; all writes are done by the user.
Authoritative text: ../../maintenance/release.md section 6 [example; replace per project].

## Basis
- 2026-10-11, chat with the maintainer. Verbatim: "no git writes in this directory".
  Distilled: no add/commit/tag/push/checkout; log/status/diff/show allowed.
  Reason: the user owns commit history and version tags. Confirmed by user.

## Open points
None.
```

## 4. Placing a new requirement

Apply the scope table of section 1 first, then:

1. Task scope -> record it in the plan's `decisions/` and apply it in that task's status and write scope; it ends with the task.
2. Lasting project scope -> update the authoritative governance file; if the user adjusted an existing rule, also update the memory topic.
3. Shared-method scope -> it belongs to the method's own package, under that package's write authorisation; the consuming project records the request, not a local copy of the method.
4. Unclear between 2 and 3 and it would change behaviour elsewhere? -> ask the user which level it belongs to before writing. A clear user instruction is placed directly and recorded as basis.

Never promote a project parameter (root name, tool names, retention periods, role names) into the shared method, and never keep a requirement the user explicitly made general as a project-local note only.
