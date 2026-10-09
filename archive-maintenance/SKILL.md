---
name: archive-maintenance
description: When active documents, rules, decisions or evidence need archiving, a shorter current entry, or history recovery, classify the retention contract, verify references and prove recoverability. Use for material lifecycle governance; does not perform business data migration and does not auto-clean files because they grew large or old.
metadata:
  version: "0.1.0"
---

# Archiving, retention and recovery

Keep the current entry short while preserving original material that can be found, verified and restored. Archiving is a migration with a manifest; a summary only navigates and cannot replace the original approval or sole evidence.

## Start and inputs

First confirm whether the user needs a classification proposal, an actual archive run, or a recovery; complete steps already covered by existing authorisation directly. Ask only for missing items that block the next action; do not start archiving for ordinary edits or short Q&A.

| Input | Use and missing-item handling |
| --- | --- |
| Chosen workspace, active root, archive root, file list and sole writer | Locate scope; missing object -> locate it first; missing write permission -> read-only classification is still possible; never guess cross-project roots. |
| Category, age/capacity policy, legal or project retention contract | Decide whether an object may be moved out; without a period give a proposal only, never set a retention period yourself. |
| Current activity/in-flight state, sensitive no-read scope | Active or unknown objects stay in place; when the old writer cannot be stopped, do not copy it into a "confirmed version". Do not open no-read files to compute a hash. |
| Reference consumers, historical reference intent, recovery purpose and authorisation scope | Decide which pointers to change and which old entries to keep; with incomplete consumers, note the gap and never claim there are no references anywhere. |
| Free space, writable target, verification output location | Copying needs source and new copy side by side, recovery scratch space and headroom; when short, never delete the source first to free space. |

## Lifecycle order

Execute each step as "What / Stop condition / Artefact":

1. **Classify and freeze candidates.**
   - What: read [Retention and references](references/retention-and-references.md); separate open items, current rules, completed decisions, raw evidence and rebuildable caches. Save confirmed decisions to their existing authoritative destination first and re-read them; refresh the current workbench/status per the existing `context-handoff` contract, without creating a separate user-page template.
   - Stop condition: the object is still active or its state is unknown, or no retention contract applies.
   - Artefact: classification table; old rules that are still referenced are preserved by version.
2. **Build an auditable manifest.**
   - What: use the [archive record](assets/archive-record.md) to record source, versioned destination, size, SHA-256, references and recovery requirements. Hashes come from actual reads of a stable source; record verified evidence of activity state separately from author claims.
   - Stop condition: the target is not unique, or the source changes during reading.
   - Artefact: a manifest that is unique per item; confirmed archive items are frozen, revisions use a new item and record the lineage.
3. **Read-only verification before copying.**
   - What: prepare the manifest per the JSON contract in the references topic and run the [verifier](scripts/archive-verify.py) in `precopy` mode.
   - Stop condition: source missing or changed, target already has a file of the same name, path or activity state abnormal; stop that item.
   - Artefact: precopy result; its old-reference hints are migration to-dos and do not prove the object may be moved out.
4. **Perform the approved copy.**
   - What: an executor with write permission copies item by item into a new version directory with a project-approved tool. The destination file must be created exclusively and rejected if it already exists; never check for absence and then write with overwrite. Verify only after writing and closing. The script does not copy.
   - Stop condition: interruption or insufficient space. Keep the source and the partial target, verify per [Failure and recovery](references/recovery.md), and never delete leftovers by file name.
   - Artefact: actual copy result per item.
5. **Verify and migrate references.**
   - What: run `verify` to check the stable size/hash of source and archive and that they are independent copies; then update only approved, non-frozen referencing files to point at the exact version; rerun `verify` after updating.
   - Stop condition: any error blocks move-out. Historical references inside frozen originals are not rewritten; keep a reachable old entry or an explicit new index.
   - Artefact: verify result; manual verification records for consumers that cannot be resolved automatically.
6. **Prove recoverability.**
   - What: per the recovery topic, copy selected samples into an empty approved recovery directory, use `restore` to compare hash and byte-for-byte content between archive and the real restored copy, and check each actual consuming entry.
   - Stop condition: bytes differ or the entry cannot be opened.
   - Artefact: recovery record. Sole non-rebuildable evidence and approvals are verified in full; for the rest, spot checks state basis, ratio and unsampled items.
7. **Complete the approved move-out.**
   - What: when the retention contract allows it, copy/references/recovery all meet acceptance, and the source has not changed since the last verification, an authorised executor moves it out of the active area.
   - Stop condition: objects under a keep-old-source contract, part of a complete audit set, or still referenced are not deleted.
   - Artefact: this batch's manifest and results, logical bytes before and after (may use verifier `summary.bytes_by_role`) and actual space change; unfinished items stay in their current state. Leftovers from subtasks are taken over by the main task; the end of a response does not mean cleanup is complete.

A successful `verify` is only a checkpoint within the manifest, not delete permission, a concurrency lock, or proof of library-wide references. Before final move-out, keep writers stopped and verify the latest state; if a stable window cannot be established, keep the source.

## Scenarios and resources

- Normal: the original text of a completed decision is filed under a version directory, the current index points to that version, and the restored copy is byte-for-byte equal; when refreshing the workbench, handled items are removed and the original approval can still be read back via the index.
- Misuse: the user page is too long but contains items awaiting decision; only reorganise the display, do not move undecided content out. Another plan still uses an old rule version; keep that version and a reachable pointer.
- Failure: same-name target, concurrent source change, cross-root symlink or restored bytes differ; keep the source and fix the cause. Never sign off integrity based on "summaries match" or "file exists".

Classification and pinning manifest hashes use low/low; cross-plan conflicts and knowledge distillation use normal/medium; grade words map to actual execution configuration through the project resource mapping. Estimated disk reads cover at least source, archive, scanned files and recovery comparison; read large files in chunks. Use parallelism only with independent targets and a settled write seat; never verify concurrently with copying/modifying the same file.

## Sources

1. Pinned source: [CX01 filesystem-context](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/58b55a8921758d13453b440704fb1b5b208c0b0e/skills/filesystem-context/SKILL.md), sections `Core Concepts`, `The Static vs Dynamic Context Trade-off`, `Pattern 1` and `Gotchas`.
2. Adopted externalised originals, short pointers, targeted retrieval and staleness classification; lifecycle, permission boundaries, manifest format and the verifier are own-authored for this package.
   Dropped default automatic cleanup by age/count.
3. License: shipped with the package as [LICENSE-CX.txt](LICENSE-CX.txt) (CX, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license file along when copying this package alone.
