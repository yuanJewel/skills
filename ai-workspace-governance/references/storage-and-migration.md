# Storage and migration

Read this page when moving an existing root to the canonical layout, writing or migrating `retention.yaml`, or performing the archive of an accepted plan. Archiving steps consume `archive-maintenance`; this page adds the layout-specific mapping and the configuration contract.

## 1. Choosing the root

1. The project already has an AI material directory -> use its location; inventory and map its content; do not keep scattered archive areas or mixed rule files just because they exist.
2. The project has none -> the user picks one (`ai/`, `docs/agent-notes/`, a separate workspace path...); the package does not add a root to a repository, and never to another repository, on its own.
3. A multi-repository workspace -> a shared root at the workspace level with a pointer from each repository entry is possible; verify visibility, write permission and sharing boundary first.
4. A wiki or external page is a source, not a root -> record provenance and access; a layout mapping for it is a design, not an implemented root.

## 2. Migrating an existing root

Produce a migration table before touching files. Columns: old path, class per [Material model](material-model.md), content identity (SHA-256 or equivalent), new path, action, referencing consumers, status.

Actions and their rules:

| Action | Rule |
| --- | --- |
| Keep | Same path; may receive updated links |
| Move | Bytes unchanged, path changed; originals, approved plans and external source copies are moved, never rewritten |
| Rewrite and merge | Current rules whose text is reorganised into the new governance files; the old file is retired only after its content is fully carried and the backup is proven |
| Archive | Bytes unchanged, moved under `archive/` with a record; historical links inside stay as they were |
| Retire | Remove an old active file or empty directory after its carrier exists, the backup restores it, references are updated and the writer's final state is known |

Order of execution:

1. Verify writers and in-flight work; freeze the file list of the old root at a stated time.
2. Preserve one complete backup of the old root for the batch inside `archive/` (a staging path under `archive/` is acceptable during packing), built strictly from the frozen list so the backup never includes itself. Verify restoration into an independent scratch directory by per-file hash before any rewrite starts. One backup per batch; do not snapshot again per file or per rule.
3. Create the new structure; move originals; rewrite current rules; create indexes.
4. Update current references and path statements in non-frozen files; keep historical originals untouched.
5. Verify: moved originals byte-identical, reading chain usable from the project entry, every migration table row has a destination and a status.
6. Retire old active files and empty directories listed in the table. Do not delete the backup, existing historical archives or anything outside the table; do not use unscoped recursive deletion.
7. Recycle scratch restore directories per the local resource cleanup rules of `task-implementation`.

If the source changed after the backup, list the real difference as a separate item; the earlier backup does not cover the new bytes. If an object's writer is unknown, leave it in place and mark the row unfinished; do not sign the migration as complete.

## 3. `retention.yaml` configuration contract

`retention.yaml` is parsed YAML, not prose. The minimal contract below is extensible: projects add fields; migrations of an existing retention file keep every effective key and its semantics and record the mapping of old keys to the common ones. Values the user has not set are written as `not_configured`; no default period, capacity or automatic deletion is invented.

```yaml
schema_version: 1              # version of this configuration contract; independent of any package version
archive_root: archive          # relative to the material root; the only archive location

plans:
  close_requires:              # all must hold before a plan may be archived
    - scope_complete
    - verification_passed
    - final_acceptance_recorded
    - writers_handed_back
  acceptance_owner: status     # "status" = named per plan in status.md; or a fixed project responsibility (not a tool name)
  archive_path: archive/plans/<plan-id>/
  pre_archive_checks: [no_active_writers, references_updated, restore_verified]

subtasks:
  parent_receives: [result_verified, final_state_known]   # a subtask counts as done only when the parent has verified both
  unknown_external_state: keep_open                         # never treated as handed back
  leftovers: parent_takes_over
  independent_plan_when: accepted_separately                # a subtask with its own acceptance gets its own plan id

materials:
  protected:                   # never cleaned by any rule below
    - archive/**
    - plans/*/decisions/**
  retention:
    governance: current_only_plus_memory_basis
    knowledge: current_only
    plans_active: until_archived
    verification_outputs: {keep: until_plan_archived, then: not_configured}
  limits:
    period: not_configured
    capacity: not_configured

cleanup:
  requires: [retention_rule_matches, backup_or_archive_verified, writer_state_known, user_confirmed]
  recursive_unscoped_delete: forbidden
```

Meaning of the blocks:

| Block | Semantics and requirements |
| --- | --- |
| `schema_version` / `archive_root` | Contract version and the single archive location relative to the root; not tied to the root name |
| `plans` | Preconditions for closing, who owns acceptance (pointer to `status.md` or a project responsibility, never a tool fixed for all tasks), the archive path pattern, checks before archiving |
| `subtasks` | What the parent must verify before counting a subtask as done, how unknown external state and leftovers are treated, when a subtask becomes its own plan |
| `materials` / `cleanup` | Protected globs, per-class retention, user-confirmed limits (or `not_configured`), and preconditions that must all hold before anything is removed |

A tool that consumes the file reads these keys; nothing is executed by the file existing. Resource parameters such as concurrency, model or cost belong to the project's runtime or resource configuration, not here. Role-specific rules belong to `governance/roles/`, general task rules to `collaboration.md`.

## 4. Archiving an accepted plan

Follow [Canonical layout section 6](canonical-layout.md) for triggers, the step table, the write discipline and the resume rule. The two guarantees it keeps: until the source is removed, `plans/README.md` and `user.md` carry a working link to the source and the archive row is at most `switch pending`; the archive row becomes `archived` only as the final write, so no earlier failure registers completion. Use the `archive-maintenance` manifest and verifier for copy, verify and restore; this package fixes only the target `archive/plans/<plan-id>/`, the three navigation files, the owner and the order. The archive record names: plan id, accepted candidate identity, acceptance wording and its location, acceptance owner, acceptance and archive dates, verification result, the per-file manifest of the copied plan, uncovered scope, and the appended `close-out:` lines.

Navigation files are replaced by write-temp, read-back, rename — never truncated in place — so a crash inside a write leaves the previous entry. The archive record is published the same way and counts as a record only when its `manifest: complete <n> files` line is present and the manifest matches the archived files; anything else is a leftover and the resumer treats it as "no record". Appended `close-out:` lines are single complete lines from a fixed vocabulary; a torn fragment carries no state. Source removal follows the record's manifest with `status.md` last; a resumer inspects the actual directory (complete, partial, absent) against that manifest and against the archive hashes, and never infers removal from a missing `status.md` alone or from an unverified record.

## 5. Scattered archives

During inventory, any backup, snapshot or archive directory found inside the project's scope for this root is added to the migration table and moved under `archive/` after its references and restorability are checked. Content outside the granted scope is reported, not moved.
