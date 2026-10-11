# Workspace map: {{root_path}}

<!-- Filled by the designer or implementer of a governance task and kept in that task's plan directory. Delete instructions and rows that do not apply. A filled map is a design artefact; it does not prove that files were created or moved. -->

| Item | Content |
| --- | --- |
| Project and entry | {{project_name}}; entry files: {{entry_files}} |
| Material root | {{root_path}}; chosen because: {{root_basis}} (existing root / user choice / shared workspace root) |
| Mode and authorisation | {{design_or_implementation_or_review}}; source of write scope: {{authorisation_source}}; allowed paths: {{allowed_paths}} |
| Plan identity | {{plan_id}}; status file: {{status_path}} |
| Writers and in-flight work | {{writers_and_state}}; frozen at: {{freeze_time}} |

## Core and extensions

| Core place | Present | Authoritative file | Note |
| --- | --- | --- | --- |
| `README.md` | {{yes_no}} | — | {{note}} |
| `user.md` | {{yes_no}} | — | {{note}} |
| `governance/policy.md` | {{yes_no}} | {{path}} | {{note}} |
| `governance/collaboration.md` | {{yes_no}} | {{path}} | {{model: fixed / per-task / single}} |
| `governance/retention.yaml` | {{yes_no}} | {{path}} | {{schema_version; migrated keys}} |
| `governance/memory/` | {{yes_no}} | {{index_path}} | {{topics}} |
| `governance/roles/` | {{yes_no_or_not_needed}} | {{path}} | {{why}} |
| `knowledge/` | {{yes_no}} | {{index_path}} | {{note}} |
| `plans/` | {{yes_no}} | {{index_path}} | {{active plan ids}} |
| `archive/` and `archive/plans/` | {{yes_no}} | {{index_path}} | {{other archive categories}} |

| Extension | Purpose | Maintainer responsibility | Authoritative file | Read when | Archived under |
| --- | --- | --- | --- | --- | --- |
| {{extension_dir}} | {{purpose}} | {{responsibility}} | {{path}} | {{condition}} | `archive/{{category}}` |

## Inventory and migration

| Old path | Class | Identity | New path | Action | Consumers | Status |
| --- | --- | --- | --- | --- | --- | --- |
| {{old_path}} | {{rule / fact / task / memory / history / rebuildable / extension}} | {{sha256_or_equivalent}} | {{new_path}} | {{keep / move / rewrite-merge / archive / retire}} | {{referencing_files}} | {{pending / done / blocked: reason}} |

## Governance text and memory provenance

| Current rule | Authoritative file | Memory topic | Basis state |
| --- | --- | --- | --- |
| {{rule_summary}} | {{path}} | {{governance/memory/topic.md or none}} | {{confirmed / open}} |

## Acceptance and archive responsibility

| Plan | Acceptance owner | Final acceptance by | Archive target | Preconditions met |
| --- | --- | --- | --- | --- |
| {{plan_id}} | {{responsibility, current holder}} | {{project contract designate}} | `archive/plans/{{plan_id}}/` | {{list or pending}} |

## Backup, references and unverified items

- Batch backup: {{archive_path}}; identity {{sha256}}; restore check {{result_and_time}}.
- Reference updates: {{files_updated}}; left frozen: {{historical_files}}.
- Unverified or pending: {{items_with_reason}}.
