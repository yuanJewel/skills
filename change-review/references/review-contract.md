# Candidate and review contract

## Explicit scope

Input is JSON known to contain no secrets. Only relative POSIX file paths are supported; no globs, directory expansion, symlinks, parent paths or absolute entries.
The project root must be an explicit absolute canonical path without symlinks; dot segments, repeated slashes or trailing slashes are not accepted. Each component is opened with directory descriptors and no-follow, and root identity is re-verified at the end, so parent links are never followed after a mere pre-check.
Control files are also confirmed by the caller as readable and non-secret; never use real configuration as the scope file.
Both scope and compare open no-symlink paths component by component and accept only regular files; non-blocking open keeps FIFOs/devices from being read; limit 4 MiB, read twice and verify file identity.
The root itself, its ancestors and control file paths must not match secret patterns; this still does not guarantee recognising arbitrary secret content.
JSON rejects duplicate keys, floats/non-finite numbers, wrong field types, lone surrogates and overly deep structures; failures give only structured errors.

```json
{
  "entries": [
    {"path": "src/new.go", "kind": "added"},
    {"path": "src/handler.go", "kind": "modified"},
    {"path": "src/old.go", "kind": "deleted"},
    {"path": "schema/service.proto", "kind": "context"},
    {"path": "gen/service.go", "kind": "generated", "sources": ["schema/service.proto"]},
    {"path": "config/credentials.json", "kind": "excluded", "secret": true, "reason": "secret content is no-read; verify only the configuration interface"}
  ]
}
```

A rename is expressed as two entries: "old path `deleted` + new path `added`"; the old path may carry `previous_sha256`, and when content is identical the reviewer explains it is a pure rename from the hashes on both sides.

`added/modified/context/generated` must exist and be regular files; `deleted` must not exist, which also holds when the parent directory is missing; a symlink cannot stand in for absence. `added` is the provider's claim about history; the script does not query Git, and proving an addition needs old-baseline evidence. The current hash of `deleted` is empty; it may carry a `previous_sha256` (lowercase SHA256) from a known public baseline; otherwise state explicitly that old content is unverified. Never read no-read historical content to fill a hash.

`generated.sources` has at least one item, and each source must also be in entries (or excluded with a reason); the script only records the relation, does not prove the output is reproducible and does not run the generator. Undeclared generated identity is not detected automatically; the reviewer is responsible for identifying it. Other approved exclusions also use `excluded + reason`; never exclude user-specified scope by default as "generated" or "WIP".

The secret flag and the no-read rule for common secret directories/extensions are a first line of defence and cannot recognise secrets in arbitrary files. Legitimate business sources containing secrets should be replaced by a user-provided redacted stub or trusted redacted evidence, recording the coverage limit of the substitute; never read first and then claim the secret was not touched.

## Running and return

```sh
python3 scripts/candidate-manifest.py --root {{approved_project_root}} --scope {{scope_file}} > {{before_manifest}}
python3 scripts/candidate-manifest.py --root {{approved_project_root}} --scope {{scope_file}} --compare {{before_manifest}} > {{after_manifest}}
```

`{{...}}` is replaced by the consuming task with approved locations. `--root` must be a real absolute path without symlink components: on macOS `/tmp` and `/var` are symlinks to `/private/...`; obtain the real path first with `realpath` or similar. The caller does the redirection; the script writes JSON only to stdout/stderr; never overwrite the before manifest or the scope file. It uses only the Python standard library and needs a platform supporting `dir_fd` and `O_NOFOLLOW`; without them it fails rather than silently degrading to following links. Default limits are 1000 entries / 16 MiB per file; when exceeded, first shrink to a reviewable batch or explicitly pass `--max-files` / `--max-file-bytes`; do not retry endlessly.

| Exit code | `status` | Meaning and action |
| --- | --- | --- |
| 0 | `captured` | Capture succeeded, or compare content identity is the same; empty entries still need a separate report of no reviewable items |
| 1 | `changed` | This capture is stable but differs from the old manifest (stdout contains `comparison: changed`); keep both, locate the change, re-review affected conclusions |
| 2 | `error` | Input or runtime condition error, no stable manifest; fix the input or environment per the `error` reason on stderr and recapture |
| 2 | `unstable` | File identity or content changed between the two reads; first coordinate with the writer/obtain an immutable snapshot, then recapture |

Successful results go to stdout, `error`/`unstable` to stderr, in the form `{"error":"<reason>","status":"error"}`. Reasons are script constants without paths or file bytes; only unclassified errors such as platform read failures give a generic sentence. Common exit-2 reasons:

| `error` reason (excerpt) | Handling |
| --- | --- |
| `root must be a real path without symlink components…` | The root path contains a symlink (e.g. macOS `/tmp`); pass the real path instead |
| `root does not exist` / `control input file does not exist` | Verify the location of the root or scope/compare file |
| `a required candidate file is missing` | A non-deletion entry lacks its file; add the file or change it to `deleted` |
| `a declared deletion is still present` | A deleted entry still exists; confirm the candidate or change the kind |
| `candidate is a symlink…` / `a candidate parent component is a symlink…` | List the real file instead; symlinks do not enter the candidate |
| `secret-like or explicitly secret paths must be excluded` | Secret-pattern paths need `excluded + reason` |
| `generated output requires explicit sources` / `each generation source needs its own scope entry…` | Add generation sources, and list each source in scope too |
| `candidate exceeds per-file byte limit` / `entries must be a bounded list` | Shrink the batch or raise the limit explicitly |
| `absolute, empty, dot and parent path components are forbidden` | Change entries to relative POSIX paths |

The hash covers the normalised scope, the explicit root, each item's content or deletion/exclusion marker, and generation relations. Per file, identity such as inode/size/times is checked before and after opening, and everything is read again; a visible replacement during the process is rejected even when content is identical. Identity data is used only for this run's stability judgment, not in the long-term content hash, so pure time changes do not change content identity.

It is not an atomic file-system snapshot: a brief change between the two reads that is then reverted, changes after reading, and external attacks on the same file system cannot be fully excluded. When a stronger guarantee is needed, obtain an approved immutable candidate copy or pause writers, and still recheck after review. It does not scan directories for omissions, lock files, write the Git index, query commits or prove full-repository coverage.

## Two-axis operation

The specification axis maps each explicit requirement to candidate locations and expected behaviour; a missing test is an evidence gap, and missing implementation is reported only when the specification actually requires it and it is not implemented. Deletions require checking explicitly provided callers/routes/build references; missing consumer material is recorded as insufficient coverage. An unchanged dependency is added as context and the scope re-pinned only when it is affected.

The standards axis first compares against applicable rules and neighbouring implementations, then constructs an actual failing input. If all you can say is "I prefer another style", list a suggestion; if you can prove a specific input causes privilege escalation, data loss or leakage, report a defect. Line numbers are bound to the current candidate, keeping old/new side identity; never give new-file line numbers for deleted lines that do not exist.

Generated differences require checking whether sources and artefacts were updated together and whether the generator/runtime version is supported; actually running the generator is outside the read-only script. Without output reproduction evidence, never claim generation is consistent.

## Conclusion and recovery boundary

Give each axis separately "no confirmable issue found / issues found / insufficient material"; the overall summary covers only the current scope. When the user requested only a review, hand fix suggestions back; do not change source code automatically. After a fix, re-hash and locate affected cases and consumers; conclusions confirmed to have no cross-impact may be carried over, but the basis must be stated.

Normal: an old route is deleted and old client material is provided; reproduce and locate the call compatibility defect. Misuse: two receipts claim a pass without candidate identity and raw evidence; this cannot count as an independent review pass. Missing input: only current files exist, without pre-deletion content; existing logic can still be reviewed, deletion impact stays pending verification.
