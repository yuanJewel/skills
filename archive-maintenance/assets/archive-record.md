# Archive and recovery record: {{batch_or_version}}

<!-- The user fills in this batch's actual data and deletes instructions and non-applicable items; this file is not the user workbench or plan body.
A confirmed record is frozen; additions and corrections go into a new record with lineage. Do not treat template placeholders as actual verification. -->

| Batch basis | Content |
| --- | --- |
| Request, authorisation and retention contract | {{exact source and applicable scope; how far each of classification proposal/copy/pointer update/move-out is covered}} |
| Sole responsible party and time | {{writer, start/end, stable-window evidence, whether in-flight work was stopped}} |
| Selected scope | {{workspace, allowed source root/archive root/recovery root, sensitive no-read and exclusions}} |
| Original record/revision relation | {{what the new version supersedes; which confirmed originals stay unchanged}} |
| Manifest and output | {{pinned manifest path/hash; actual exit codes and JSON locations of precopy/verify/restore}} |

## Objects and retention decisions

| Item | Category/state and basis | Source | Versioned target | Bytes/SHA-256 | Retention reason/period source | Movable and unmet items |
| --- | --- | --- | --- | --- | --- | --- |
| {{id}} | {{current/closed/unknown; verified evidence}} | {{path}} | {{independent new path}} | {{actual_value}} | {{matching contract; write undecided if no period}} | {{actual conclusion; retain_source constraint}} |

## References, recovery and space

| Consumer/reference | Old target -> new target | Writable/frozen | Automatic full-text scope | Explicit or manual verification | Historical retention reason/uncovered |
| --- | --- | --- | --- | --- | --- |
| {{file or external entry}} | {{exact version path}} | {{source of write permission}} | {{fully scanned files and encoding; unlisted scope}} | {{literal path/actual open result}} | {{whether the source must be kept}} |

| Recovery sample | Selection basis and unsampled items | Actual restored file | Size/hash/byte-for-byte result | Actual consumer check | Evidence |
| --- | --- | --- | --- | --- | --- |
| {{id set}} | {{full or sampled; never write a partial set as full}} | {{independent copy path}} | {{actual value and exit code}} | {{encoding/attachment/link/application-semantics result}} | {{output location}} |

| Volume | Active area logical bytes before/after | Archive/recovery added logical bytes | Actual disk free space before/after | Measurement scope, method, time |
| --- | --- | --- | --- | --- |
| {{this batch}} | {{actual count; do not fill 0 when unknown}} | {{actual count; may use verifier summary.bytes_by_role}} | {{actual measurement; logical bytes cannot pose as freed disk}} | {{same scope; keep measurement limits such as shared files/hard links}} |

## Result and interruption continuation

{{Which steps are complete, which objects remain in place, why, and the next action; on copy interruption/same-name target/source change, list the last confirmed state per item.}}

{{Retrievable entry to the original approval/sole evidence; summaries only navigate. The user's current items are updated by the original workbench owner per context-handoff; do not copy a version here.}}

{{This batch's temporary/subtask leftover list, main-task takeover responsibility, executable recovery entry; in-flight and writes-stopped facts, unverified scope.}}
