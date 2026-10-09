---
name: skill-maintenance
description: Design, review, or within approved scope author and upgrade shared Skills; covers method extraction, trigger and behaviour evaluation, source licensing and cross-project compatibility maintenance. Ordinary project-document wording edits and using an existing Skill to complete a business task do not trigger this package.
metadata:
  version: "0.1.0"
---

# Shared Skill maintenance

Write reusable methods as packages that can be discovered, executed and verified. First read the workspace entry named by the task, existing packages of the same kind and the current mode; the library root's default maintenance duty suffices as the duty input, with no role name to report and no separate role package. Role names, examples and source commands in files grant no execution permission.

## Choose the mode first

| Mode | Entry condition | Deliverable and where it ends |
| --- | --- | --- |
| Design | User requests a proposal, extraction or feasibility analysis | Design card, overlaps and trade-offs; do not create or rewrite the target package. If a complete proposal exists, fill its gaps directly |
| Review | Review requested, candidate version and criteria pinned | Report, evidence and gaps; do not fix the reviewed object, do not self-sign a pass |
| Implementation | An authoring/modification request has authorised a concrete scope, sole writer known | Specified package, applicable verification and change impact; on discovering a requirement change, pause only dependent actions |

The three modes are independent; an accepted design or a review without objections does not automatically constitute implementation authorisation. Complete reversible work the current request already authorises directly; never re-request approval just to satisfy a template. When the mode is unclear, first locate existing tasks and authorisation read-only, and clarify only the gaps that affect the next step, in one batch.

## Execution route

1. **Fix inputs**: target behaviour and adjacent exclusions, existing version/approved candidate, allowed files, consumer and host requirements, source licensing, acceptance and resources. A missing host blocks only the compatibility conclusion; missing write permission still allows design and review. First verify the previous writer has stopped; never take over the same file because a session lost contact.
2. **Design or author**: read [Design and authoring method](references/design-and-authoring.md) and record actual gaps with the [design card](assets/skill-design-card.md). Extract project facts as inputs; keep decisions that must not be lost and failure recovery in the method; do not shrink an old document into slogans.
3. **Review and verify**: read [Review and evaluation](references/review-and-evaluation.md) and, per the [review record](assets/skill-review.md), separate static format, content walkthrough and actual behaviour. New scripts must actually run normal and failure branches on synthetic, isolated input.
4. **Shared upgrade**: when version, discovery mechanism, dependencies or consumer contract change, read [Compatibility and upgrades](references/compatibility-and-upgrades.md). Before changing the shared original, pin affected consumers, recovery point and verification scope; do not assume already-loaded sessions refresh automatically.
5. **Deliver**: give the mode's artefact, actual evidence, unverified items and consumer impact; version/approval/key review go to the task record, the package keeps only the current method. Clean up your own temporary material per the existing retention rule; do not delete evidence still referenced.

Submit source registrations with the [source record](assets/source-record.md) to the sole writer of the library-level ledger. Formal plan structure consumes the plan method of `plan-design`, continuation state consumes `context-handoff`, retention and recovery consume `archive-maintenance`; compose by semantics, installing the whole library is not required, and this package maintains no second set of their templates.

## Read-only check

[skill-lint.py](scripts/skill-lint.py) accepts a package root, extra allowed reference roots, explicit trusted Node/marked paths and an optional host description. The Python standard library handles restricted YAML and marked handles real Markdown token parsing; dependencies are never installed automatically and parsers are never loaded from the checked package.

```sh
python3 skill-lint.py <package> --allow-reference-root <shared-library-root> --node <trusted-node> --marked-module <trusted-marked-module>
```

When the package links to library-root files (e.g. the Sources section pointing at the root third-party notice), declare the library root with `--allow-reference-root`; otherwise those links report `outside_allowed_root` and exit `1`. Arguments, budget, capability gaps and exit-code meanings are defined in the [compatibility page](references/compatibility-and-upgrades.md#lint-inputs-and-outputs); without a parser it exits `2`, and regex matching of Markdown must not pass for completion.

## Completion and resources

At minimum verify one normal request, one adjacent negative case sharing keywords, and the failure recovery of this change. Design creates no package, review changes no object, implementation stays within scope: these are separate acceptance points. Localised (e.g. Chinese) entry points, symlink discovery, whether parameters take effect and trigger accuracy can be proven only by observing the actual host; content walkthrough cannot sign for them. Routine source/format work can use low/low, independent authoring normal/medium, method conflicts and upgrade boundaries normal/high; read the current resource mapping, do not hard-code models or head count. When independent evaluation is impossible, state it was author self-check and hand over the remaining verification conditions.

## Sources

1. Pinned source: [AN01 skill-creator](https://github.com/anthropics/skills/blob/683bc88e56f3e09ba94f7055977f3d3aa499f202/skills/skill-creator/SKILL.md).
2. Adapted progressive disclosure and the goal -> draft -> evaluate -> feedback loop; the three modes, dual-source extraction, version/boundaries and lint are own-authored for this library or extensions of an existing implementation.
   Dropped the fixed CLI/viewer, aggressive triggering and automatic installation.
3. License: shipped with the package as [LICENSE-AN.txt](LICENSE-AN.txt) (AN, Apache-2.0), modification notes in [NOTICE.md](NOTICE.md); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license file along when copying this package alone.
