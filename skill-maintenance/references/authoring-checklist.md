# Authoring checklist

For anyone adding or modifying a package: work through sections 1–5 before and during writing, then section 6 before handover.
Detailed author rules live in [Design and authoring method](design-and-authoring.md); this page tells you what to check and how.
`lint` means `skill-lint.py` reports the check; `manual` means you verify it and record how.

## 1. Package structure

| Check | How | Detail |
| --- | --- | --- |
| Directory name equals frontmatter `name`. | lint | [Lint scope](compatibility-and-upgrades.md#lint-inputs-and-outputs) |
| `SKILL.md` exists at the package root. | lint | [Lint scope](compatibility-and-upgrades.md#lint-inputs-and-outputs) |
| No nested package directories. | manual: inspect the tree for additional package roots. | [Authoring method](design-and-authoring.md) |
| Root `LICENSE-<abbr>.txt` is byte-identical to upstream at the pinned version. | manual: compare SHA-256 with the pinned upstream file. | [Convention 2](design-and-authoring.md#library-wide-author-conventions) |
| Apache-2.0 sources ship root `NOTICE.md` with a modification record. | manual: inspect the source license and notice. | [Convention 2](design-and-authoring.md#library-wide-author-conventions) |
| Optional directories are only `references/`, `assets/` and `scripts/`. | manual: inspect the package tree. | [File split](design-and-authoring.md#write-one-complete-path-first-then-split-files) |

## 2. SKILL.md body and frontmatter

| Check | How | Detail |
| --- | --- | --- |
| `name` matches the directory. | lint | [Lint scope](compatibility-and-upgrades.md#lint-inputs-and-outputs) |
| `description` is at most 1024 Unicode characters; no generic 120-character hard gate applies. | lint | [Lint scope](compatibility-and-upgrades.md#lint-inputs-and-outputs) |
| Description states capability, applicable conditions and adjacent exclusions. | manual: identify each element in the description. | [Description design](design-and-authoring.md) |
| Each adjacent exclusion owned by another package names that package, e.g. "handled by `docker-local-environment`". | manual: map exclusions to their owner packages. | [Convention 6](design-and-authoring.md#library-wide-author-conventions) |
| `metadata.version` is semantic and bumped for every published change. | manual: compare the version with the previous published package. | [Handover](#6-before-handover) |
| Body gives required inputs, key branches, missing-X -> do-Y, completion conditions and when to read linked supporting pages. | manual: walk a concrete request; resolve every "see the docs" reference. | [Authoring method](design-and-authoring.md) |
| Resource paragraph uses cost/reasoning grade words and the project resource mapping. | manual: inspect the recommendations and host-limit inputs. | [Convention 7](design-and-authoring.md#library-wide-author-conventions) |
| `## Sources` contains exactly three numbered items. | manual: count items and check their required content. | [Convention 1](design-and-authoring.md#library-wide-author-conventions) |

## 3. Author conventions 1–11

These are check summaries; the [full conventions](design-and-authoring.md#library-wide-author-conventions) remain the rule authority.

| # | Check | How | Detail |
| --- | --- | --- | --- |
| 1 | Sources has three items covering pinned source, adaptation and license. | manual: count and inspect the items. | [Convention 1](design-and-authoring.md#library-wide-author-conventions) |
| 2 | License naming, byte identity and Apache notices follow the source. | manual: inspect filenames and notices; compare hashes. | [Convention 2](design-and-authoring.md#library-wide-author-conventions) |
| 3 | No explicit unfinished author scaffolding markers remain in the checked text. | lint | [Marker coverage and exemptions](compatibility-and-upgrades.md#lint-inputs-and-outputs) |
| 3 | Fields use `{{field}}`; tool-native syntax stays unchanged; no unfinished TODO/TBD remains, including templates. | manual: inspect fields, examples and template prose. | [Convention 3](design-and-authoring.md#library-wide-author-conventions) |
| 4 | Scripts use only exit codes 0/1/2, with subdivisions in JSON `status`. | manual: run pass, noncompliant and error branches on synthetic input; inspect output. | [Convention 4](design-and-authoring.md#library-wide-author-conventions) |
| 5 | Each sentence makes one judgment; inputs use lists; source lines stay around 200 characters. | manual: read the prose and inspect line lengths. | [Convention 5](design-and-authoring.md#library-wide-author-conventions) |
| 6 | References name the owner package; definitions have one authority. | manual: compare references with section 5. | [Convention 6](design-and-authoring.md#library-wide-author-conventions) |
| 7 | Wording avoids internal governance terms; resources use grade words and project-supplied host limits. | manual: inspect terminology and resource recommendations. | [Convention 7](design-and-authoring.md#library-wide-author-conventions) |
| 8 | Project entities appear only as project inputs, examples or conditionals. | manual: inspect specific names and configurations. | [Convention 8](design-and-authoring.md#library-wide-author-conventions) |
| 9 | Fragment anchors are verified, otherwise link only the page. | manual: check actual target headings or explicit anchors; lint does not check fragments. | [Convention 9](design-and-authoring.md#library-wide-author-conventions) |
| 10 | Methods creating local resources name `task-implementation` for cleanup. | manual: inspect created objects and the cleanup reference. | [Convention 10](design-and-authoring.md#library-wide-author-conventions) |
| 11 | Published prose is English; `README.zh.md` is the Chinese twin. | manual: scan for CJK and inspect other non-English prose, allowing the README language selector. | [Convention 11](design-and-authoring.md#library-wide-author-conventions) |

## 4. Spelling and terms

Use British spelling in prose: artefact, authorise, organise. Write license (the spelling used in filenames and existing package prose).
Keep filenames as `LICENSE-*.txt`; preserve code and tool identifiers exactly as the tool spells them.

| Term | Definition |
| --- | --- |
| adjacent exclusions | Easily confused neighbouring package scopes that the description excludes. |
| candidate / content identity | The specific version under review or delivery, identified by its content hash. |
| grade words | Cost/reasoning tiers such as `low/low` or `normal/medium`, resolved through the project resource mapping. |
| host | The environment that runs the Skill, such as Claude Code or Codex. |
| independent review | Review by someone who did not author the candidate and does not change the reviewed object. |
| own-authored | Material written for this package rather than adopted from a source. |
| pinned source | An original source fixed to a specific version or commit, rather than a moving branch tip. |
| placeholder | A field written as `{{snake_case}}` for a consumer to supply; tool-native variable syntax is preserved. |
| progressive disclosure | Keeping the entry body concise and reading supporting pages only when needed. |
| receipt | A structured report of a subtask or implementation result. |
| resource mapping | Project configuration mapping grade words to actual execution settings. |
| sole authority / single source of truth | The one package that maintains a concept's definition. |
| sole writer / write seat | One writer holding a file's write responsibility at a time. |
| stub | A local substitute for an external dependency. |
| synthetic | Explicitly constructed data or examples, rather than real project or account facts. |
| task brief | The instructions supplied when dispatching a subtask. |

## 5. Sole-authority index

When another package needs one of these concepts, reference its owner by package name under convention 6.
Change the definition only in its owner; the links below locate the existing contract.

| Concept | Owner package | Anchor or page |
| --- | --- | --- |
| Local resource cleanup | `task-implementation` | [Cleanup](../../task-implementation/references/cleanup.md) |
| Plan template and boundaries, recovery, estimates and review | `plan-design` | [Template](../../plan-design/assets/plan.md); [boundaries](../../plan-design/references/task-boundaries.md#boundaries), [recovery](../../plan-design/references/task-boundaries.md#recovery), [estimates](../../plan-design/references/task-boundaries.md#estimates), [review](../../plan-design/references/task-boundaries.md#review) |
| Takeover flow | `role-bootstrap` | [Takeover](../../role-bootstrap/references/role-contract.md#takeover) |
| Verification status meanings | `verification-gate` | [Statuses and wording](../../verification-gate/SKILL.md#statuses-and-wording) |
| Candidate content identity and manifest script | `change-review` | [Candidate manifest](../../change-review/scripts/candidate-manifest.py) |
| History retention and archive verification | `archive-maintenance` | [Retention and references](../../archive-maintenance/references/retention-and-references.md) |
| AI working-material root: core structure, material classes, selective memory, retention configuration contract and acceptance-owner archiving | `ai-workspace-governance` | [Canonical layout](../../ai-workspace-governance/references/canonical-layout.md); [material model](../../ai-workspace-governance/references/material-model.md) |
| Author conventions and lint | `skill-maintenance` | [Conventions](design-and-authoring.md#library-wide-author-conventions); [lint](compatibility-and-upgrades.md#lint-inputs-and-outputs) |
| Official fact-check method | `mysql-migration-safety` | [Official fact check](../../mysql-migration-safety/references/ddl-and-locks.md#official-fact-check) |

## 6. Before handover

1. Run lint with an explicit library root and trusted parser; require exit 0. Exit 2 is not a pass. Use the [lint contract](compatibility-and-upgrades.md#lint-inputs-and-outputs).
2. For new or changed scripts, run normal, noncompliant and error branches on synthetic input; record commands and exit codes.
3. Bump `metadata.version`; append a modification line to `NOTICE.md` for Apache packages.
4. Update the package row in both root READMEs, `README.md` and `README.zh.md`.
5. After acceptance, add an entry under Unreleased in the root changelog naming the package and new version.
6. State what was author self-check and what remains unverified.
