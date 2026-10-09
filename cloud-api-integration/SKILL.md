---
name: cloud-api-integration
description: Design or test cloud provider HTTP/SDK client boundaries, pagination, rate-limit retries, async operation state and resource normalisation. Use for wrapping an established API set and local synthetic verification; does not perform real cloud discovery, tests or operations, and does not automatically replace existing direct calls with an SDK.
metadata:
  version: "0.1.0"
---

# Cloud API integration method

Implement only the API surface the project needs; follow the existing direct-HTTP or SDK pattern and separate transport, authentication, protocol mapping and domain merging. A simulated success does not prove real cloud permissions, quotas or network behaviour.

## Inputs and missing items

Take the public API/SDK version and the actual call inventory, the pagination/error/idempotency and final-state contracts, domain identity/field mapping, allowed local endpoint/transport injection, synthetic auth and seeds, and request/page/time budgets. Without the exact API version, do not guess fields/signatures; without transport injection, design an isolation interface first instead of filling the gap with the default credential chain.

A project's direct HTTP calls may stay as they are. For an existing SDK, verify whether construction can disable environment/file/metadata credentials and inject fake auth and a controlled transport. Missing real credentials is not a reason to block local tests. An explicitly missing API item blocks only the related calls; existing normalisation/pagination synthetic tests can continue.

## Method

1. Per [Client boundary](references/client-boundary.md), pin method/endpoint/version, authentication and response mapping, and verify that every request goes only through the synthetic transport; forbid any metadata or real cloud fallback.
2. Per [Pagination, retries and polling](references/pagination-retry-and-polling.md), define completion criteria, loops/budgets/partial failure, bounded retries and cancellation; when a write response is unknown, reconcile first.
3. Per [Provider normalisation](references/provider-normalization.md), align on provider x account x region x kind x immutable ID. Before a complete snapshot, no disappearance judgments; manual resources and existing relationships are protected.
4. Use the [provider contract](assets/provider-contract.md) to list versions, fields, identity, errors/final states and the scope of proof; use the [synthetic provider](assets/synthetic-provider.md) to build pages/failures/duplicates and cancellation. It may be combined with the external dependency stub method of `external-dependency-simulation`; no need to install a whole new tool set.
5. Run authorised local verification and record whether it was real HTTP/SDK or a pure transport model. List unknown fields, unknown states, partial failures and unverified real behaviour explicitly; do not call one HTTP 200 a complete synchronisation.

## Failure, resources and recovery

- Failure classification: distinguish authentication/permission, parameter, rate limit, transport, business failure, cancellation and unknown async state; do not retry everything or downgrade everything to success.
- Completeness: maintain completeness state independently for each account/region/resource kind; a failed scope does not release existing resources.
- Save on interruption: save request/operation identity, pages fetched, continuation token, budget and in-flight work.
- Re-read: token expired or snapshot consistency cannot be guaranteed -> re-read that scope; do not stitch together pages from different times and call it complete.

Resource guidance: mechanical response mapping uses `low/low`; pagination stalls, idempotency, cross-region identity, permissions and async state use `normal/high`. Grade words map to actual execution configuration through the project resource mapping. Allocate parallelism by provider quotas, connections/pages, and host limits such as machine and executor concurrency quotas (given by project configuration); do not bypass rate limits with more workers.

Positive example: an empty page with a nextToken keeps going; if the second page fails, that scope is not aligned and nothing is deleted. Counter example: the SDK cannot find fake credentials and reads the environment or metadata; overwriting a same-named manual resource by display name.

**Wrap-up cleanup**: synthetic provider processes, ports, recorded responses and local caches are reclaimed after verification ends. Follow the local resource cleanup rule of `task-implementation`: register identity on creation, reclaim only objects registered this run at wrap-up, write evidence to keep and failed cleanup items into the receipt, and use no global cleanup commands.

## Sources

1. Pinned sources: [EC11 api-connector-builder](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/skills/api-connector-builder/SKILL.md), [EC06 api-design](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/skills/api-design/SKILL.md); the Azure async summary is checked against the [ARM official documentation](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/async-operations) (read 2026-10-09); specific providers/APIs follow the input version.
2. From EC11, adopted existing-pattern-first, narrow interfaces, and the transport/mapping/registration/test loop; from EC06, the method/response/error, pagination and compatibility topics. Cloud identity, signing, retry/polling and completeness methods are own-authored for this package, with no full attribution for idempotency specifics.
   Dropped the mandatory reading of a fixed number of similar components. After adding a provider or version, re-verify the actual call contract and synthetic counter examples; do not expand permissions based on historical collection success.
3. License: shipped with the package as [LICENSE-EC.txt](LICENSE-EC.txt) (EC, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license file along when copying this package alone.
