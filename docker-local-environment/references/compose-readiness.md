# Configuration, startup and readiness

## Distinguish configuration interfaces

Verify per component which configuration the current version supports: a business service may only read a mounted YAML file, a third-party image may support env, files or init scripts, and Compose interpolation is yet another layer.
Do not infer from one image that "all official images accept only env", and do not replace an application's declared file interface with env.
Secret management is not reworked uniformly in this example; local inputs are all synthetic, never copied and masked from real configuration.

Verify build inputs and runtime configuration separately. An empty-credential configuration kept in the project may be a Docker COPY, compile or same-source test input; do not rename/delete the in-repo input because a test uses another mounted file.
Check the Dockerfile's actual dependencies; a missing input is a build failure, not something to bypass by changing the business contract.

Synthetic values keep format, length, empty/default semantics and recognisable identifiers; logs keep only permitted fields.
Init scripts usually run only against an empty data directory; restarting a database with an old volume after changing the script does not reseed it. A reset requires a dedicated node, ownership and a seed version; never wipe unrelated volumes.

## From configuration validation to service readiness

1. Pin all `-f` files and synthetic environment inputs; check that the rendered result has no implicit host inheritance, non-loopback ports, real targets, extra networks of undeclared purpose or unfamiliar volumes.
2. Verify image tag/local image ID, digest, platform and required programs. Release tags are mutable; record the actual identity for reproduction. The example requires LOCAL_TEST_IMAGE set explicitly and does not guess the latest version.
3. Dependencies reach their own readiness before consumers start; `depends_on` expresses only start ordering and cannot replace application reconnects, later failure handling or end-to-end readiness. When host tooling does not support conditions, use a bounded external probe and state the difference.
4. Probes have a total deadline, per-attempt timeout, interval and a cap on failure content; verify the contract for business version/seed completion/read-write capability. `running`, an open TCP port and any HTTP 200 each prove only their own layer.
5. Verify only on the actual path: when calls should go through the gateway, do not bypass it to reach data services directly. Verify synthetic dependency authentication failure, seed not complete and reconnect after recovery; with a dependency missing, do not count a 200 degraded page as whole-system ready.

Do not loop restarts on startup failure and mask the first cause. Keep the first error, the selected configuration and image identity; distinguish required dependencies, dependencies allowed to degrade and the test control plane.
After a restart, confirm the old instance has exited and the new instance's identity; do not consume a success response on the old port.

## Using the synthetic Compose file

The [example](../assets/compose-local.yaml) only starts a non-root Python HTTP service serving a synthetic ready file; it has no database/user directory/project code.
Before invoking, confirm the local Python 3 image, Compose version and available ports; bind the variables used by the two nodes to their respective start commands, never rely on one shared `.env` overwritten concurrently.
Run `config --quiet` first, then start per the environment manifest; the example does not authorise pulling images.

The example has two networks:
- `isolated` is an internal network; dependency services (databases, caches, etc.) attach only to it.
- `publish` is a plain bridge; only services needing host access attach to both `isolated` and `publish`; ports still bind only to `127.0.0.1`.
- When attached only to the internal network, published ports in `ports` are not mapped to the host.
- When `docker port` is empty or the host probe fails, do not sign off "port available" or "port conflict check passed".
- Attaching to `publish` gives the service a route out through the host. When the task requires the service to have no egress either, do not publish ports; use a probe container on the `isolated` network or `docker compose exec` for readiness/smoke checks.

The service is healthy only when the internal healthcheck reads the expected JSON; the host loopback port must be verified separately; neither proves compatibility with other protocols.
The template uses no persistent volume; files live in tmpfs and state is lost on destruction; when a failure needs reproducing, export permitted synthetic evidence first.
When an unsupported resource field appears, record the capability gap; do not silently drop limits and continue multi-node load tests.
