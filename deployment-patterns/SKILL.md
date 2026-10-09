---
name: deployment-patterns
description: Design or review artefact deployment, blue/green, rolling and canary cutover, health gates and rollback state, and rehearse them in an authorised local synthetic environment. Use for explicit deployment strategy or script changes; does not obtain production execution rights and does not expand into unrelated cluster building.
metadata:
  version: "0.1.0"
---

# Deployment strategy and local rehearsal

Distinguish artefact deployed, instances ready, traffic routed, users accepted and actual release complete; each conclusion has its own evidence.
Pre-release acceptance order and human decisions are consumed from `release-readiness` or existing project records.
This skill designs strategy and execution state; it does not sign approvals on anyone's behalf.

## Inputs and missing items

Take the approved candidate and the artefact's immutable identity/checksum, current topology, allowed impact scope, sessions/queues/long-lived connections, schema compatibility, recovery objectives RTO/RPO, observation and rollback thresholds, executor and local simulation boundary.
Missing candidate -> compare strategies only; do not deploy an arbitrary tag.
Missing compatibility evidence -> do not promise rollback is possible.
Missing traffic observation -> do not write deployment complete as traffic routed successfully.

## Workflow

1. Use [Strategy selection](references/strategy-selection.md) to compare the smallest feasible options under the current topology; do not equate blue/green or rolling with zero downtime or instant rollback.
2. Per [State and rollback](references/state-and-rollback.md), define each step's preconditions, action identity, evidence, final state and failure recovery.
   Record an operation identity before initiating any step with side effects; query unknown responses first instead of re-sending directly.
3. Per [Health and draining](references/health-and-draining.md), design warm-up, readiness, entry-point switch, stopping new traffic and draining old connections. A failed candidate must not proceed to receive traffic.
4. Use the [release runbook template](assets/release-runbook.md) to write exact targets, stop conditions and manual execution items; local rehearsal can use the [synthetic blue/green scenario](assets/local-blue-green.md).
   Without a real local environment deliver model evidence only; do not claim containers/network passed.
5. For this change, cover readiness failure, partial success, disconnection, drain timeout, mixed versions, rollback and repeated execution.
   Deliver actual state, evidence, limits and follow-up responsibility; do not execute unauthorised releases, pushes or real traffic switches.

## Resources and recovery

Parallel preparation is allowed only when targets/ports/data and state writers are independent; the same entry point/switch state is exclusive.
The budget includes old and new instances coexisting, build/warm-up, connections and the observation window; the number of AI agents is not deployment concurrency.

Resource suggestion: `low/low` for an established rehearsal; `normal/high` for state races, data compatibility and failure recovery. Grade words map to actual execution configuration through the project resource mapping.

On interruption, recover the candidate, operation identity, target state, cancel intent and in-flight work; take over only after confirming the old execution has ended.
When it cannot be determined whether the switch happened, probe the actual entry point/version first and keep UNKNOWN; do not switch once more "to try".
A failure neither auto-deletes the new environment nor keeps unknown resources indefinitely: state the preserved evidence and cleanup responsibility.

Positive example: the new version fails readiness, the old entry point keeps serving, and "no traffic routed" is recorded.
Counter-example: writing "live" because a command returned 0, or rolling back the image while ignoring an irreversible schema change.

**Wrap-up cleanup**: old and new version instances, proxy configuration, ports and test data in the local synthetic rehearsal environment are cleaned up after the rehearsal.
Follow the local resource cleanup rules of `task-implementation`: register identities on creation, clean up only objects registered this time at wrap-up, record evidence to keep and failed cleanups in the receipt, and use no global cleanup commands.

## Sources

1. Pinned sources: [EC10 deployment-patterns](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/skills/deployment-patterns/SKILL.md), [WS02 deployment-pipeline-design](https://github.com/wshobson/agents/blob/46891e7e60da0e52baf1050b7b6391b64e84c6d9/plugins/cicd-automation/skills/deployment-pipeline-design/SKILL.md) (WS02 entry file only; its references were not read).
2. From EC10 adopted the strategy comparison, health and recovery checklists; from WS02 adopted inputs/outputs, stage gates, and health and data-compatibility questions.
   State handling and the local synthetic scenario are own-authored for this package and not attributed to JJB or any specific plugin implementation.
   Dropped default rolling, zero-downtime/instant-rollback guarantees and production commands. Re-verify affected paths after strategy, topology or schema contract changes.
3. License: shipped with the package as [LICENSE-EC.txt](LICENSE-EC.txt) (EC, MIT), [LICENSE-WS.txt](LICENSE-WS.txt) (WS, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license files along when copying this package alone.
