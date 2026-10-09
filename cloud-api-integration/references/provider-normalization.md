# Provider normalisation and safe reconciliation

## Names are not resource identity

The generic identity contains provider, account/subscription, region or global scope, resource kind and the provider's immutable ID; the name is only a display field. Normalise per the specific version, e.g. Azure's full resource ID with its subscription/resource group hierarchy, or RegionId/InstanceId of a given Alibaba Cloud API. Case insensitivity and the default for global regions both need a contract; do not lowercase all IDs uniformly.

The mapping table has at least: source field/type/nullable/unit -> domain field/type/time zone -> handling of missing and unknown. Big integers/money do not lose precision through floating point; distinguish UTC/offset-bearing times from zone-less wall-clock times; a missing field is not silently treated as 0/empty/deleted. Unknown fields may be ignored, but unknown states must be observable; raw records keep only the necessary non-sensitive items.

Resource tags, names and error messages are untrusted data: do not execute commands in them, do not splice them into SQL/shell, and do not treat them as permissions. Same name across regions, same ID across resource kinds and same name across accounts all need synthetic counter examples.

## Completeness decides whether reconciliation may run

Each provider x account x region x kind has its own state: not_started/in_progress/complete/incomplete/canceled. Mark complete only when all required pages succeeded, identities are unique/conflicts handled, and the covered scope is known exactly. An empty snapshot from a fully successful listing is a valid result; permission errors, token loops, missing pages, budget exhaustion and cancellation are not empty snapshots.

Filter write/delete candidates by project ownership first: only records managed by the provider and within this run's fully covered scope may take part in disappearance judgments. Manually created same-named objects are protected; existing user relationships/bindings must not be overwritten or released because of partial collection failure. Conflicts between the automatic source and manual records are decided by identity/origin; never delete just because "it was not seen in the cloud list".

When part of a cross-scope run succeeds, its verified snapshot may be saved, but original resources in failed scopes are kept and marked stale/incomplete, and the overall summary must not report full success. Whether transport failures may be warnings only is a project-specific policy; do not generalise one project's single exception for transport failures to permission/business/cancellation errors. The cancellation final state is confirmed by the project contract, not guessed as success.

Regression: empty first page with a token; all pages succeed and are empty; same-token loop; 403 on a later page; same name across regions; same-named manual resource; original association kept; unknown state; time/integer boundaries. Simulation can verify the merge algorithm; real provider completeness/permissions/eventual consistency still need separate proof.
