---
name: docker-local-environment
description: Set up, diagnose or clean up local Docker/Compose environments for development and testing, managing dependency readiness, resources and parallel isolation. Production operations, remote Docker endpoints and release decisions are out of scope for this package.
metadata:
  version: "0.1.0"
---

# Local container environment

Deliver a local environment that starts repeatably, explains its failures and has a bounded cleanup scope. An image that starts does not prove the business is ready.

## Inputs

- Workspace and permitted operations
- Service dependency graph
- Image identity and CPU architecture
- Resource budget and node ownership
- Configuration interfaces and synthetic data
- Expected readiness conditions

Missing branches:

- Budget or ownership missing -> block only startup; configuration can still be prepared.
- No local engine evidence, or the endpoint is remote/of unknown identity -> stop engine operations, deliver only the candidate and gaps; do not switch context automatically.
- Local image missing -> report the acquisition gap; pull or build only within the task's permitted scope, and do not run upstream install scripts.
- Readiness conditions missing -> do not sign off readiness; report only the observed layers (`running`, port, HTTP).
- Environment manifest missing -> do no cleanup, no global prune, and do not guess ownership from name prefixes.

## Choose the current path

- **Create or add parallel nodes**: read [Isolation and resources](references/isolation-and-resources.md) and fill in the [environment manifest](assets/environment-manifest.md) first.
- **Configure, start and reset**: read [Compose and readiness](references/compose-readiness.md). The [synthetic Compose file](assets/compose-local.yaml) is a single-service example using a verified local image and a dedicated loopback port; it cannot replace the project dependency graph.
  Services attached only to an internal network get no host port mapping; the example attaches services needing host access to a separate non-internal publish network, while dependency services stay on the internal network only.
- **Locate failures**: read the [diagnostic tree](references/diagnostic-tree.md); pin the failing node and minimal observation; do not rebuild the whole environment by default.
- **Finish and clean up**: per the manifest, verify actual resource identities, writers and evidence to keep, then delete the objects owned this time and approved for cleanup.

## Execution order and stop points

1. **Verify the engine**
   - Do: verify the effective Docker endpoint and the source of the context; check explicit command flags and environment overrides, not just the default context name.
   - Stop condition: remote or unknown identity -> stop engine operations; do not switch context automatically.
   - Artefact: local engine evidence.
2. **Pin inputs and resources**
   - Do: pin the candidate Compose files, explicit file set, image identity, synthetic configuration, directories/networks/volumes/ports and budget; check for existing resources with the same names.
   - Stop condition: on finding someone else's resources, do not take them over; continue only after switching to this run's own names.
   - Artefact: planned resources in the environment manifest.
3. **Resolve and start**
   - Do: resolve the configuration first, then start dependency by dependency. Configuration expansion may display values; handle only explicitly synthetic inputs.
   - Stop condition: image not local and pull/build outside the task's permitted scope -> stop and report the acquisition gap.
   - Artefact: rendered configuration summary and actual image identity.
4. **Wait for readiness**
   - Do: use bounded probes to wait for this version, seed and the real call chain to be ready.
   - Stop condition: stop on timeout, keep state and minimal logs, and distinguish service errors from environment errors; do not extend waits to mask failure.
   - Artefact: readiness evidence or the first failure.
5. **Verify parallel isolation**
   - Do: confirm the second node's ports, files, persistent state and stubs are independent, and test that they do not contaminate each other. AI concurrency and environment node count are two different budgets; do not convert one into the other.
   - Stop condition: isolation not proven -> do not sign off parallel use.
   - Artefact: two-node isolation evidence.
6. **Record and close**
   - Do: record start/reset/cleanup entry points, actual readiness evidence, versions and capabilities not simulated.
   - Stop condition: after abnormal termination, first verify in-flight processes and resource ownership; do not start another node with the same name until that is clear.
   - Artefact: completed environment manifest.

## Criteria, counter-examples and resources

Normal path: two nodes each write their own synthetic seed and each read back their own identifier; cleaning up one does not affect the other.
Adjacent misuse: a local reproduction request that points at a remote context should deliver only the candidate and gaps; on finding a port in use, do not kill the occupant.
When seeding fails, health must be not-ready. When a volume directory is not writable, do not solve it by loosening permissions on the whole host directory.

| Scenario | Expected | Evidence location |
| --- | --- | --- |
| First start ready | Internal healthcheck reads the expected content, and the host loopback probe passes separately | Manifest dependency table; [Compose and readiness](references/compose-readiness.md) |
| Dependency or seed not ready | Health stays not-ready; a 200 degraded page does not count as whole-system ready | Failure/recovery column of the manifest dependency table |
| Port conflict | On bind failure switch this node's port; do not kill the occupant; with empty `docker port` output do not sign off the conflict check | Manifest port row; [Isolation and resources](references/isolation-and-resources.md) |
| Two nodes in parallel | Each writes and reads its own identifier; after cleaning up one, the other can still read | Manifest "two-node isolation" item |
| Resource limit exceeded/OOM | Stop new load from this task; record as an environment failure, not a business assertion failure | Manifest budget and measurement items; [diagnostic tree](references/diagnostic-tree.md) |
| Old data remains after reset | Reset only dedicated resources you are entitled to; do not delete similar volumes | Manifest volume row; diagnostic tree |
| Image platform mismatch | Switch to the matching architecture image or record emulation; do not call it equivalent to native | Manifest image item; diagnostic tree |
| Points at a remote context | Stop engine operations; deliver only the candidate and gaps | Manifest local engine evidence item |
| Bounded cleanup | Delete only manifest objects owned this time; on failure report remaining IDs; do not escalate to global prune | Manifest closing item; "Bounded cleanup" in Isolation and resources |

Resource guidance: configuration rendering/known probes use `low/low`; topology and recovery design use `normal/medium`; mount, concurrency or readiness-semantics conflicts use `normal/high`. Grade words map to actual execution configuration through the project resource mapping.
Read the execution configuration and node budget the project provides; on exceeding resources, first stop this run's new load and preserve evidence; do not squeeze unrelated services.
Re-verify affected paths when the image/Compose/host changes; Linux containers cannot prove native macOS/Windows behaviour. Local health or a passing CI build does not mean releasable.

**Closing cleanup**: containers, Compose projects, networks and volumes created this time, plus untagged images and temporary builders left by builds, are cleaned up on finishing or abandoning. Follow the local resource cleanup rules of `task-implementation`: register identities at creation, at closing clean up only the objects registered this time, write evidence to keep and cleanup failures into the receipt, and use no global cleanup commands.

## Sources

1. Pinned source: [EC09 docker-patterns](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/skills/docker-patterns/SKILL.md).
2. Referenced networks, volumes, loopback ports, readiness and container limits; the resource manifest, ownership, node isolation and diagnostic method are own-authored for this package.
   Dropped plugin installation, real credential injection, global prune and production commands.
3. License: shipped with the package as [LICENSE-EC.txt](LICENSE-EC.txt) (EC, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license file along when copying this package alone.
