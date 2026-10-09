---
name: container-image-management
description: Plan, execute or review container image builds, cross-registry sync, Harbor uploads, multi-platform manifest list verification and image retention cleanup. Use for artefact identity and distribution tasks; does not cover business deployment traffic switching, local Compose failures or the identically named Harbor benchmarking tool.
metadata:
  version: "0.1.0"
---

# Container image management

Deliver images that are traceable by immutable identity, have genuine platforms and complete content, and whose cleanup breaks no references.
First read the image policy and allowed actions designated by the consuming project.
Registry domains, project names, platform sets, tag conventions and executors all come from project input; do not derive permissions from examples.

## Inputs and modes

Determine whether the task is a plan, read-only review, sync, build-and-publish or cleanup; plan/review alone performs no push or deletion.
Take the source reference, target repository/tag, platform set and variant, allowed intermediate artefacts, image/tool/Harbor versions, existing target digest, writer, observation and retry budget, and verification requirements.
Missing permissions still allow a plan; a missing source platform cannot be fabricated by editing JSON or using a local image.
Authentication is handled by the approved execution environment; do not request or read real passwords, tokens or Docker credential files.
Available credentials do not equal operation authorisation.

## Read per step

1. **Source and platforms**: read [Source and platforms](references/source-and-platforms.md) and pin the source content graph; distinguish upstream image sync, build from source and tag-only changes.
2. **Prepare execution**: read [Build and copy](references/build-and-copy.md).
   Follow the project-supplied limits on release tag count and staging tags (e.g. single release tag, no per-architecture staging tags); one target tag has exactly one writer.
   Use a concrete command only after verifying it on the target tool version.
3. **Target verification**: read [Harbor and integrity](references/harbor-verification.md); verify the release tag, index, child manifests, config and all layers. Merely showing platform names is not a full pass.
4. **Failure or cleanup**: read [Recovery and retention](references/recovery-and-retention.md).
   Verify unknown results first; deleting a tag, deleting an artifact and running GC are three distinct actions and are not interchangeable.
5. **CI integration**: read [Pipeline and policy](references/pipeline-and-policy.md) only when a Dockerfile, pipeline or release consumption is involved.
   Image pullable, scan passed, runnable and business go-live are different conclusions.
6. Use the [operation and evidence template](assets/image-operation.md) to deliver what was observed, what was not observed and the next executor. When an existing record can be reused, add fields to it; do not build a parallel ledger.

## Completion conditions and resources

A sync task proves the approved platform mapping matches the source digests and the target is completely retrievable.
A rebuild task proves pinned source/build inputs and platform artefacts; it cannot be required to match the upstream digest.
Give separate content, runtime, scan/signature and UI-observation conclusions as the project requires; tests not run stay unverified.
After cleanup, re-verify the retained tags and content graphs; do not rely on the deletion return code alone.

Read-only preparation across different repositories may run in parallel; release tag updates, rollbacks and cleanup run serially under the sole writer.
Budget bandwidth, disk, builder CPU and download-verification bytes separately; pulling multiple platforms does not mean they run natively on the local machine.
Do not automatically add remote builders, install QEMU, change TLS policy or change Harbor global settings.

**Wrap-up cleanup**: intermediate images built or pulled locally, temporary local tags, temporary buildx builders and exported files are cleaned up at task end.
Deletion of remote tags/artifacts still requires separate authorisation per the recovery and retention reference.
Follow the local resource cleanup rules of `task-implementation`: register identities on creation, clean up only objects registered this time at wrap-up, record evidence to keep and failed cleanups in the receipt, and use no global cleanup commands.

## Sources

1. Pinned source: [EC09 docker-patterns](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/skills/docker-patterns/SKILL.md); Docker/Harbor/OCI technical facts are verified against [Technical sources](references/technical-sources.md).
2. Adopted the scenario-check and counter-example organisation; image state, cross-registry integrity and recovery methods are own-authored for this package.
   Dropped any deployment, installation or cleanup authorisation from the source.
3. License: shipped with the package as [LICENSE-EC.txt](LICENSE-EC.txt) (EC, MIT), [LICENSE-DX.txt](LICENSE-DX.txt) (Docker Buildx, Apache-2.0), [LICENSE-HB.txt](LICENSE-HB.txt) (Harbor, Apache-2.0); modification notes in [NOTICE.md](NOTICE.md); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license files along when copying this package alone.
