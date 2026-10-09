# Retention judgment, reference coverage and verification manifest

## Category decides the action; thresholds only trigger a check

| Category | Retention and move-out criterion | Verification focus |
| --- | --- | --- |
| Active plans, items awaiting decision, in-flight artefacts | Stay at the current entry; verify the execution final state first; never move out because of age or size | Current owner, unfinished items and actual execution |
| Current rules | Keep a single authoritative location; old versions are frozen as separate items, noting effective/expiry dates and supersession | Whether a reference means "latest" or a pinned old version; never mix them |
| Completed decisions, original approvals | Save the original to the authoritative decision location, then remove the handled display from the current workbench | Approval's applicable object, exact version, evidence chain; never substitute a summary |
| Raw evidence, non-rebuildable material | Retain per the owning contract; confirmed archives are never overwritten, revisions go into a separate item | Content identity, consumers and recoverable original bytes |
| Rebuildable caches, drafts, intermediates | First give rebuild inputs/tools/cost and reference status; clean up only when contract and authorisation allow | No sole facts, no unmigrated references, rebuild feasibility verified |

When age, capacity or count crosses a threshold, first count and classify; without configuration give an auditable proposal and never set a default period yourself. Contracts such as legal hold, complete audit sets, or no-modify/no-delete apply only to their own objects. A business audit requirement of "complete and queryable online + archive" does not mean all AI drafts are kept forever, and grants this package no business migration permission. Old directories the current task explicitly keeps are not put on the move-out list.

Each fact has a single current authoritative destination; historical originals may be preserved in multiple copies, but the index marks version and state. Errors in a confirmed item are linked to a new erratum item, never patched in place. The current workbench/checkpoint uses the existing `context-handoff` contract: move handled items out only after a successful save; with nothing pending, keep no empty sections or internal logs. This package provides archive evidence only.

## Reference coverage must be reported separately

1. **Establish consumer scope.** List cross-plan indexes, rule entries, script arguments, external pages and frozen historical items. Put explicitly chosen readable text files into `scan_files`; never recursively read the whole disk from the current directory. Unlisted files, no-read scope and external consumers form the uncovered table.
2. **Automatic full-text scan.** The verifier stream-reads each declared file completely with strict UTF-8 decoding, and searches for each old source's absolute path and its canonical path relative to that file. This is raw literal substring search and also reports same-name paths in code samples or plain prose. It does not truncate the body and does not parse Markdown; it does not recognise URL encoding, anchors, concatenated paths, symlink aliases or text in images. Not finding a literal cannot prove there is no semantic reference.
3. **Explicit reference verification.** Each `references` item declares the file, the exact literal path and the manifest target it points to; the check confirms the literal actually appears, its canonical resolution matches the target, and the target passes this phase's size/hash verification. Raw absolute paths and canonical relative paths are supported; URLs, percent encoding, anchors/queries and reference-style Markdown identifiers are not resolved. Those forms need separate manual or real-consumer verification. A path appearing does not prove it is a clickable link.
4. **Historical references.** Deliberately keeping an old source path requires both `historical: true` with a reason, and `retain_source: true` on the entry as a commitment to keep the source reachable. A "historical" mark alone cannot let a broken link pass. An ordinary old reference is a migration to-do warning in `precopy` and an error in `verify/restore`. Historical references in the archived version itself may point directly at the archive item with a recorded reason.
5. **Handle overlapping paths.**
   - When the old path literal is wholly contained in a declared archive/restore path that passed this phase's size/hash verification, that occurrence does not count as a leftover old reference. Example: `decision.md` is contained in `archive/v1/decision.md`.
   - Judge per position: other independent occurrences still error; undeclared new paths or new paths whose target is not verified cannot exempt.
   - Output keeps both the raw `matches` and the `uncovered_matches` not covered by those new paths; cross-chunk and nested repeated references are handled the same way.
   - Longer undeclared paths and plain prose may still produce false positives. The author checks the actual text and records the coverage limit; never fake a historical reference to "turn it green".
   - Forms that cannot be resolved must be listed manually item by item with target and actual open result; a script pass covers only declared supported forms.

## JSON input: all top-level fields are required

Each mode change is saved as a new execution manifest; the original manifest and confirmed results are not overwritten. Below is an illustration for an independent workspace; the user replaces root values with the actual allowed **absolute real directories**; the digest in the example must be filled with the actual value from the stable file.

```json
{
  "schema_version": 1,
  "phase": "verify",
  "roots": {"work": "{{allowed_root_real_absolute_path}}"},
  "entries": [{
    "id": "decision-1",
    "source": {"root": "work", "path": "active/decision.md"},
    "archive": {"root": "work", "path": "archive/version-1/decision.md"},
    "size": 12,
    "sha256": "{{actual_64_char_lowercase_sha256}}",
    "state": "closed",
    "retain_source": false
  }],
  "scan_files": [{"root": "work", "path": "index.md"}],
  "references": [{
    "file": {"root": "work", "path": "index.md"},
    "entry": "decision-1",
    "kind": "archive",
    "literal": "archive/version-1/decision.md",
    "historical": false,
    "reason": "current index points to the archived version"
  }]
}
```

| Field/rule | Exact meaning |
| --- | --- |
| `phase` | `precopy` checks the source and requires the target to be absent; `verify` requires both source and archive to exist; `restore` requires archive and the real restored copy to exist and compares them byte for byte; the source may already be moved out. |
| `roots` | 1-32 explicit allowed roots; keys start with a lowercase letter and contain lowercase letters/digits/underscores/hyphens, at most 32 characters. The directory must exist, must not be `/`, and path components must not contain symlinks, dot segments or backslashes. On macOS `/tmp` and `/var` are symlinks to `/private/...`; write the real path. With a symlink present the output gives a fixed hint. Never `resolve()` first to disguise a symlink as a real root. |
| `entries` | 1-4096 items; `id/source/archive/size/sha256/state/retain_source` are required. `restore` is an optional locator object, but in restore mode every item must have it; so a recovery subset can be selected and saved as a separate manifest. |
| File locator | Contains only `root` and `path`; `path` is a canonical relative file path: no absolute paths, empty components, `.`, `..` or backslashes. Source/archive/restore paths must not overlap; the manifest also rejects names that collide by case or Unicode equivalence. |
| Stable identity | `size` is a non-negative integer, not a boolean; `sha256` is the real file's lowercase digest. dev/inode/mode/size/mtime/ctime are verified before and after reading and before finishing; any change prevents a stable conclusion. Files may still change after the check, so the caller must maintain the stable window. |
| `state` | `closed/active/unknown`; the latter two are rejected. `closed` is the caller's evidence-backed claim, not proof that the script found all active writers. |
| `retain_source` | Explicit boolean; true commits to keeping the source afterwards. false does not mean delete permission. |
| `scan_files` / `references` | Must be arrays; empty is allowed but reports coverage 0 and cannot be called a full reference check; at most 4096 items each. Each reference's `file` must be in the scan list. |
| Reference item | `file/entry/kind/literal/historical/reason` are all required; kind is source/archive/restore and must point to that entry's corresponding locator. A historical reason must be non-empty. Canonical relative references may contain `..` only when they point exactly at a target inside a declared allowed root and no actual path contains symlinks. |
| Strict parsing | Unknown fields, duplicate fields, explicit null, NaN/Infinity, type errors and lone surrogates not encodable as UTF-8 are rejected; valid non-BMP characters are allowed. Manifest limit 1 MiB, general string limit 4096 characters; UTF-8 text bodies are not truncated. |

Run `python3 <package_dir>/scripts/archive-verify.py <absolute or cwd-relative manifest path>`. It uses only the Python standard library and safe file-descriptor opens, runs no shell and installs no dependencies. It needs POSIX `O_NOFOLLOW/O_DIRECTORY/O_NONBLOCK`; on hosts without them it fails and exits. The script does not copy, delete, create directories or write reports; the caller saves stdout to an approved evidence file. Reading may cause ordinary file-system atime updates; that is not a business content write.

Output is a single JSON object with `schema_version/ok/status/exit_code/issues`; when the input is usable it also contains `phase/summary/coverage/files/recovered`. File verification gives actual size/hash; `summary.bytes_by_role` gives the total source/archive/restore bytes actually read this run and can be copied straight into the volume table of the archive record. The full-text scan gives occurrence counts per literal. Verification issues contain code/context/message/severity and never output file bodies; message is a fixed explanation that does not include raw platform errno text.

| Exit code | `status` | Meaning |
| --- | --- | --- |
| 0 | `passed` | This phase passed within the declared scope (precopy may carry reference to-do warnings) |
| 1 | `noncompliant` | Verification found nonconformance; see `issues` |
| 2 | `invalid_input` / `internal_error` | Manifest, path or host capability unusable, or an internal script exception; no usable conclusion |

File-level issue codes: `missing_file` (file or parent directory missing), `symlink_or_boundary` (a path component is a symlink or not a directory; not followed, never leaves the root), `permission_denied`, `file_unreadable`. Size/hash mismatch or change during reading is `file_verification`; target conflict and recovery comparison are `target_or_recovery`.

Missing arguments also produce JSON. When the process is killed externally, or disk or stdout fails, there may be no complete result; treat it as incomplete and never interpret it as passed.

An existing archive target is always a conflict in `precopy`, even with identical bytes; when re-entering after interruption, first use `verify` to check the existing corresponding item; never overwrite. The script rejects source/archive sharing an inode and restore/archive sharing an inode; only equal ordinary copies count as evidence. Memory for full scanning and hashing grows with 1 MiB chunks and a bounded literal tail; file size itself never causes a whole file to be loaded into memory.
