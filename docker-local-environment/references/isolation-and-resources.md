# Isolation, ownership and capacity

## Local boundary

Record the selected Docker endpoint, explicit CLI flags, relevant context overrides and the engine identifier; take only necessary metadata, never export the full configuration or credentials.
`unix://` is usually a local socket, but a proxy may forward it; verify against the engine known to the workspace, and do not treat a name containing "local" as evidence.
For TCP loopback also confirm ownership of the listening service; SSH/remote addresses do not enter this package's execution path. Do not change the global context to "fix" a single task.

Define the explicit file set; Compose automatically loads override files, `.env` and shell variables that change the final configuration.
Select a synthetic env file and pass only the needed variables; environment inheritance, secret directories and the host Docker socket are not default inputs. Configuration resolution commands do not guarantee zero information leakage either; let them read only verified synthetic files.

## Allocate independent resources per node

| Resource | Selection and check | Conflict handling |
| --- | --- | --- |
| project | Unique task/node identifier; first check for containers/networks/volumes with the same name | Do not reuse someone else's project; do not use a fixed container_name |
| network | Internal network managed by the project; services needing host ports also attach to a project-managed non-internal publish network; never attach external networks automatically | For same-name, external or shared networks, check ownership first |
| volume | Independent ephemeral state by default; create a named volume only when persistence is needed | Do not mount existing business volumes; do not judge a volume empty by its name |
| bind mount | Explicit real source path, UID/GID, read-only/write needs | Reject path escapes, credential directories, the whole host root and unknown symlink targets |
| port | Map only necessary ports to loopback, reserved independently per node | A pre-check cannot remove races; on bind failure switch this node's port, do not kill the occupying process |
| namespace | Database name, Redis prefix, object directory, message/stub state | Prefer independent services; for shared services, prove full-path naming isolation and cleanup scope |

`internal: true` only restricts external connectivity of the created network; it is not absolute proof of no egress. Extra networks, host mode, proxies, mounted sockets and application redirects can all form bypasses.
Check the final topology and observe the network against a locally controlled reject target; do not access a real cloud to prove there is no internet. No network at runtime does not mean image pull or build has no network.

## Capacity and lifecycle

From the host's available budget, deduct existing load and margin, then compute each node's CPU/peak memory/volume and log disk/PID/port needs; the number of runnable nodes is limited by the tightest dimension.
An estimate is not a measured limit; calibrate after observing the first node's peak. Record the Compose version and the limits actually in effect; a YAML field existing does not mean the kernel enforces the limit. OOM, disk exhaustion and PID limits are environment failures, not business assertion failures.

Before starting, record: candidate file digests, planned resource -> actual resource ID mapping and labels, start time and creator. Sample resources at fixed points in long tests and give logs bounded capacity; do not let evidence preservation become unbounded logging.
On exceeding the budget, first stop this task from starting new nodes, handle existing nodes per project rules, keep the failure state, then reduce the node count or raise a capacity gap.

## Bounded cleanup

First finish this node's in-flight requests and tests, take back write permission and save results; check actual IDs/labels, creation time, mounts and sharing against the manifest. Clean up only containers, networks and temporary volumes currently and explicitly owned.
Do not use `down --remove-orphans` or `down -v` as an unconditional finale; reused project names can also cause collateral damage. Persistent volumes need a separate list of rebuild evidence and deletion scope; if that cannot be proven, keep them as pending items.

On cleanup failure, report remaining IDs and reasons; never escalate to a global prune. When the environment was interrupted, recover the manifest and in-flight work before continuing; do not delete unknown resources.
Keep the minimal logs and image identity needed for the failure; remove rebuildable temporary inputs per the project archive policy; do not accumulate run records inside the skill package.
