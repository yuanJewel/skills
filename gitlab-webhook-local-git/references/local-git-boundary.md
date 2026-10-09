# Isolated local Git admission

This skill verifies the Git protocol only in an explicitly permitted synthetic space. Business repositories and repositories at real domains must never be written; real remotes are not reached around this run's boundary under a "read-only" label either. When no Git action is required, do not touch the workspace's Git.

## The manifest must be verifiable

Record this run's task/run identity, the normalised isolation root, creator, service instance/container/process identity, listen address and port, allowed repository paths and refs, allowed operations, data source (purely synthetic), lifecycle and cleanup responsibility. A path string or "a localhost service" alone is not enough: the endpoint may forward to a real system, and the directory may be a symlink to a business repository.

Confirm item by item:

1. The canonical paths of the root and repositories lie within the approved isolation root; check all ancestors/symlinks and actual ownership. Reject aliases pointing to business repositories, host shared mounts or old caches. When a repository already exists with unknown origin, verify its identity read-only; do not reset or overwrite it.
2. Parse the URL's scheme/host/port/path/userinfo first, and match the endpoint exactly against the manifest; reject URLs with embedded credentials, unapproved ports, domain aliases and path traversal/encoding ambiguity. IPv4/IPv6 loopback still needs instance proof; do not rely on the string containing localhost.
3. Check SSH URLs, scp-style `user@host:path`, file paths and HTTP in the same way; reject formats that cannot be reliably normalised. SSH config Host/ProxyCommand/jump hosts and Git URL rewriting can change the actual target; use an isolated, verified configuration, and do not read host credentials or silently inherit global configuration.
4. Disable automatic redirect following; if the local service genuinely needs a redirect, pre-approve each hop's endpoint and prevent credentials from being sent across domains. Git submodules/LFS/remote helpers, config includes, hooks, filters and external diff can trigger additional access; synthetic verification explicitly disables them or permits them one by one, not just checking origin.
5. Do not build shell strings from command arguments; validate refs/paths first and separate them from options. Execute only the specific clone/fetch/push actions the manifest allows; do not ignore that fetch writes local objects/refs just because it is called "read".
6. Record the identity of your own repositories/services and their changes before and after. Cleanup deletes only resources self-created this run with no other references; stop and check unknown in-flight work first, and never run global prune/reset.

## Separate Git and event verification

A local Gitea or other service can prove specific Git transport behaviour, but not GitLab webhook headers, permissions, recursive events or redelivery semantics. GitLab payloads are synthesised from the public contract of the matching version and tested through the receiver; never register a real hook or set up an external tunnel to let real events into tests.

Normal: the manifest specifies a temporary root and the local service/repository created this run; synthetic commits are pushed and fetched on approved refs and the results recorded. Counter example: replacing a real repository URL with localhost while the server proxy still points to the real remote; without proof of an isolated instance, refuse. When address items are missing, keep the candidate command and the missing proof; do not execute first and review afterwards.
