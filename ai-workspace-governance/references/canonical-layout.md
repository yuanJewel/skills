# Canonical layout

Read this page when creating, restructuring or reviewing a material root. It defines what every root contains, what each place is for, and how a project adds its own directories without breaking the core. The root path and name are project input; nothing below depends on the name `ai/`.

## 1. Core skeleton

```text
<root>/
├── README.md                 reading entry
├── user.md                   user workbench
├── governance/
│   ├── README.md             governance index: scope, authoritative files, which pages exist
│   ├── policy.md             current effective constraints and operating requirements
│   ├── collaboration.md      responsibilities, task/subtask management, writer contracts
│   ├── retention.yaml        retention, close-out, archive and cleanup configuration
│   ├── memory/
│   │   ├── README.md         index of effective policy/operating adjustments
│   │   └── <topic>.md        one topic per file: verbatim words, distilled rule, reason, pointer
│   └── roles/                optional: long-lived role contracts and mappings
├── knowledge/                verified project facts and domain contracts; README.md as index
├── plans/
│   ├── README.md             active plan index
│   └── <plan-id>/
│       ├── plan.md           the single plan body
│       ├── status.md         execution facts: writers, candidates, evidence, next step
│       ├── decisions/        actual approvals, when there are any
│       ├── reviews/          independent review reports, when there are any
│       └── verification/     evidence, when there is any
└── archive/
    ├── plans/
    │   ├── README.md         index of accepted plans: id, date, version, where to restore from
    │   └── <plan-id>/        the complete plan directory as accepted, plus an archive record
    └── <other categories>/   preserved backups, superseded versions, historical originals
```

Fixed: the four top-level core directories, the two root files, the five governance items (`README.md`, `policy.md`, `collaboration.md`, `retention.yaml`, `memory/`) and the plan paths. Optional: `governance/roles/`, named policy pages, plan attachment directories (create them when material exists, not before), extension directories.

On initialisation, create the core and its indexes; write real contracts where the project has them and an explicit "not configured" line where it does not. Do not fill the skeleton with sample tasks, sample approvals or sample retention periods.

## 2. What each place holds and must not hold

| Place | Holds | Must not hold |
| --- | --- | --- |
| `README.md` | Entry: which files to read for which kind of task, declared extensions, where the authoritative files are | Rule bodies, task state, duplicated policy |
| `user.md` | Results of main tasks and decision-carrying subtasks, blockers, choices or manual steps for the user, continuation entries | Full status tables, approval history, internal progress logs, management contracts |
| `governance/policy.md` and named policy pages | Current effective constraints: what the AI may and may not do, operating requirements, user-set boundaries | Chat transcripts, daily progress, several contradictory "current" versions |
| `governance/collaboration.md` | Who is responsible for what, how responsibilities map to tools or hosts, how main tasks and subtasks are assigned, received, handed back and closed, acceptance ownership | Permission inferred from a tool name, session handles, dispatch permission that was never granted |
| `governance/roles/` (optional) | Stable role contracts: input, processing, deliverable, boundary, method; registration or alias mapping if the project uses it | Mandatory per-session registration; a host permanently owning a role |
| `governance/retention.yaml` | Protected material, plan and subtask close-out conditions, archive responsibility and paths, cleanup preconditions, user-confirmed limits | Current execution state, approval wording, unconfirmed defaults, thresholds that act as delete permission |
| `governance/memory/` | Effective user adjustments to policy, operating rules or maintenance constraints and their distilled basis, traceable to current text | All user statements, ordinary Q&A, progress, one-off task approvals, round-by-round discussion, transcript backups |
| `knowledge/` | Verified project facts, domain contracts, terminology, inter-module handovers | Plans, approvals, rules that belong in governance |
| `plans/<plan-id>/` | The plan body, execution status, approvals, reviews and evidence of one active plan | Long-lived rules that should be distilled into governance or knowledge |
| `archive/` | Every archived original, superseded version and preserved backup, each with a record or manifest | Active material; anything that is still the single current copy of a rule |

## 3. Governance in detail

`policy.md` is the current text. When a policy changes, edit `policy.md` and update the matching `memory/<topic>.md` with the user's words and the reason; do not keep the old and new rule side by side in `policy.md`. Large projects split policy into named pages (`security.md`, `data-handling.md`, `preferences.md`); `governance/README.md` lists them. Do not create a page that repeats an existing current text.

`collaboration.md` separates responsibility from tool. It states the project's model (fixed assignment, per-task assignment or a single maintainer), the current mapping, and the rules for main tasks and subtasks: how a subtask is briefed, who receives its result, what happens to its leftovers, and that a subtask ending does not close the parent. See [Collaboration contract](collaboration-contract.md).

`memory/` follows the selection and merge rules in [Material model section 3](material-model.md).

`retention.yaml` follows the configuration contract in [Storage and migration section 3](storage-and-migration.md).

`roles/` exists only when the project keeps long-lived role contracts. A library maintained by one or two sessions with a default responsibility does not need it, and this package never generates a role table to make a root look complete.

## 4. User workbench and plan status

`user.md` stays in the root. It shows what the user needs now: main-task results, subtask results that carry a decision, blockers, choices or manual steps, and the entry to continue. Once the user confirms an item, remove it from the open-decisions area; the formal record goes to `plans/<plan-id>/decisions/`.

`plans/<plan-id>/status.md` is the execution fact file: stable task and subtask identities, exact writers, candidate identity, in-flight items, accumulated evidence, hand-back and next step. `governance/collaboration.md` is the management method; `user.md` is the user's current view; `retention.yaml` configures when a plan may close. Keep these four roles distinct; existing checkpoint and workbench templates from `context-handoff` are reused rather than duplicated here.

## 5. Project extensions

Projects add top-level directories for responsibilities the core does not cover. Typical examples: `maintenance/` (release procedure, pending commit text), `sources/` (external originals with their provenance), `testing/`, `runtime/`, `documents/`. Rules:

- Declare each extension in the root `README.md`: purpose, maintainer responsibility, which file is authoritative, when it is read, where its material is archived.
- Create an extension only when material for it exists. Two roots using this layout may have different extension sets; neither must create the other's.
- An extension never takes over a core responsibility. Role contracts stay in `governance/roles/`, user policy adjustments in `governance/memory/`, archived material of any extension in `archive/`. Do not create a root-level `roles/`, `memory/`, `backup/` or a second archive area.

## 6. Archive root and accepted plans

All archived material of the root lives under `archive/`. Sub-structure by purpose, plan id, date or version is allowed; a second archive area inside `plans/<plan-id>/`, inside `knowledge/`, inside an extension, or outside the root is not. Symbolic links that point archived content outside the root are not archives.

A completed plan is archived when its full scope is done, the project's required verification and final acceptance have passed with evidence, and remaining items are closed or explicitly moved out of scope by the user. Design approval, a passed review, a phase delivery or a finished subtask does not trigger it. The plan's status names the acceptance owner; that owner performs the archive as the last step of acceptance, after confirming that all writers have handed back their scope.

Two guarantees hold at every stopping point, and the order below exists to keep them:

- **Until the source is removed, the active entry points at the source.** The plan's row in `plans/README.md` keeps a working link to `plans/<plan-id>/` and `user.md` keeps one too; the row in `archive/plans/README.md`, if present, is marked `switch pending`.
- **The archive index registers completion last.** The row state `archived` in `archive/plans/README.md` is the final write of the whole procedure; any earlier failure leaves it `switch pending` or absent, so a `switch pending` row never counts as a completed close-out.

How each file is written, so that a crash inside a write cannot lose the current entry or fake a finished one:

- Navigation files (`plans/README.md`, `archive/plans/README.md`, `user.md`) are rewritten by writing the complete new content to a temporary file in the same directory, reading it back, and renaming it over the old file; never by truncating in place.
- The archive record is **published, not grown**: its initial content (all required fields and the complete file manifest, ending with the line `manifest: complete <n> files`) is written to a temporary name, read back and checked, and only then renamed to the record's final name. A file at the final name without a `manifest: complete` line is not a record; it is a leftover and is treated as "no record".
- Appended lines (`status.md` progress, record `close-out:` lines) are single lines ending with a newline. A trailing fragment without a newline, or a line that is not one of the defined vocabulary strings, is a torn write: it carries no state, is left in place or trimmed before the next append, and the resumer looks at the actual files instead.
- If a write succeeded but its progress line was not appended, the next step or the resume rule sees the file content, not the missing line.

| Step | Writes | Stop / interruption here leaves |
| --- | --- | --- |
| 1. Mark pending | Append to active `status.md`: `archive: accepted, archive pending`; set the `plans/README.md` state column if it has one | Nothing else changed |
| 2. Create target | `archive/plans/<plan-id>/`, created exclusively; refuse if it exists with different content | Source, entries untouched; conflict noted in `status.md` |
| 3. Copy | The plan directory, structure and bytes unchanged; frozen files keep their historical links | Partial target kept for inspection; source untouched |
| 4. Verify | Nothing. Read the copy back and compare byte for byte; resolve every link the record will list | Append `archive: accepted, archive pending (step 4: <reason>)`; source and entries untouched |
| 5. Archive record | `archive/plans/<plan-id>/ARCHIVE.md` (or the project's record name), published once via temporary name and rename: plan id, accepted candidate, acceptance wording and location, owner, dates, verification result, **the file manifest of the copied plan** (relative path and hash per file) closed by `manifest: complete <n> files`, uncovered scope. Then append to `status.md`: `archive: archived, switch pending` | No usable record (absent, or present without `manifest: complete`) -> the archive is not complete; source and entries untouched; a leftover temporary or truncated record is removed or set aside, never completed in place |
| 6a. Archive index, provisional | `archive/plans/README.md`: add the row with state `switch pending` and the record path (skip if the row already exists) | Source and active entries untouched |
| 6b. Active index, provisional | `plans/README.md`: keep the row, keep its link to `plans/<plan-id>/`, set its state to `archived, switch pending`, add the archive link | Row and source link still present; archive row `switch pending` |
| 6c. Workbench, provisional | `user.md`: the open item becomes "archived, close-out pending" with both the archive link and the source link | Both links present |
| 7. Remove source | Append to the record: `close-out: source removal started`. Delete the files listed in the record's manifest, `status.md` last, then the empty directories. Append to the record: `close-out: source removed` | See the resume rule: the actual directory decides, not the presence of `status.md` |
| 8a. Workbench, final | `user.md`: the item becomes the archive link only | Source gone; active row still present with archive link; archive row `switch pending` |
| 8b. Active index, final | `plans/README.md`: remove the row | Archive row `switch pending`; `user.md` points at the archive |
| 8c. Record | Append to the record: `close-out: navigation finalised` | Archive row `switch pending` |
| 8d. Archive index, final | `archive/plans/README.md`: row state `switch pending` -> `archived` | This is the only write that registers completion |

Accepted consequence of this order (a project decision, recorded with the project's governance): between 8b and 8d the plan is listed nowhere as active and the archive row still says `switch pending`; it is reached through that provisional row and the `user.md` link, and the record's `navigation finalised` line tells the resumer that only 8d is missing.

Resume rule, for any session, after any stop: do not trust a single marker; observe the files, then act.

1. Read the archive record. A **usable record** has all required fields, a manifest, and the `manifest: complete <n> files` line whose count equals the manifest rows; check that every manifest row names a file that exists in `archive/plans/<plan-id>/` with the listed hash. No file, a temporary-name file, a file without the completion line, or a record whose manifest does not match the archived files -> **no usable record**: the source is intact and nothing has been removed; set the leftover aside, re-verify the copy (step 4) and publish the record again (step 5). Never continue into 6a or step 7 on the strength of a record that fails this check.
   Then take the last **complete** `close-out:` line — a line that ends with a newline and is exactly one of `source removal started`, `source removed`, `navigation finalised`. A trailing fragment is ignored; it is not a state.
2. Usable record, last complete `close-out:` line absent or `source removal started` -> inspect `plans/<plan-id>/` against the record's manifest: **complete** (all listed files present) -> continue with 6a–6c as needed (each is idempotent: check the file content, write only what is missing), then step 7; **partial** (some listed files gone) -> compare each remaining file's hash with the archive copy, delete only files whose hash matches, keep and report any file that differs, then append `source removed` only when the directory is empty. The active `status.md` is the one exception: it keeps receiving progress lines after the manifest was taken, so its hash is expected to differ; it is deleted last once every other listed file is gone, and its archived copy remains the step-3 snapshot; **absent** -> append `close-out: source removed` if missing and continue with 8a. Never re-create the source from the archive, never delete a file that is not in the manifest or whose hash differs.
3. Last complete line `source removed` -> finish 8a–8d by content: `user.md` item is the archive link only; `plans/README.md` has no row; then append `navigation finalised`; then set the archive row to `archived`.
4. Last complete line `navigation finalised` -> only 8d may be missing; set the archive row to `archived` if it is not.
5. Archive row says `archived` -> done; a later stop can only have skipped nothing.

In every branch the record is read, never rewritten: a torn fragment is trimmed only if the next append needs a clean line end, and a historical record from an earlier completed run stays frozen. If the facts the record states (for example `source removed`) contradict the directory (the source is present and complete), the directory wins, the contradiction is reported in `status.md`, and the procedure continues from the step the directory implies.

The pending and switch markers are written to the active `status.md` only; the archived `status.md` stays as copied in step 3 (it carries the step-1 marker). Step 4 compares against that copy; the archive record states the final outcome. This is the one expected difference between source and archive and is not a verification failure.

A reopened plan gets a new linked plan id or a new archive version; the old archive stays frozen.

## 7. Two roots, same core

A library root `ai/` with `maintenance/` and `sources/` extensions and a service root `docs/agent-notes/` with `governance/roles/`, `testing/`, `runtime/` and `documents/` are both conformant: both have the four core directories, the two root files, the five governance items and `archive/plans/`; each declares its own extensions; neither needs the other's. A reviewer checks responsibilities and relative positions, not whether a given directory name appears somewhere in the text.
