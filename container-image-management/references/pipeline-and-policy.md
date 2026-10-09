# Pipeline and project policy

Read when CI image-source checks or delivery are involved.
Image management provides the pipeline with immutable artefact identity and verification results.
JJB/Pipeline expansion, queue/cancel/callback are handled by `jenkins-pipeline-jjb`; deployment strategy per `deployment-patterns` consumes the verified digest, and traffic is not switched automatically just because an image was pushed.

## Dockerfile external inputs

Pin the Dockerfile, context, target, build args and named build contexts that actually execute the build; do not just scan the file named Dockerfile at the repository root.
Parse all stages and external inputs: FROM, external COPY --from, RUN --mount from=, and the syntax frontend.
Also handle named contexts, ADD remote URL/Git inputs and extended syntax according to tool capability.
Do not treat `ADD --from`, which the build system does not support, as standard syntax: if project docs use it, verify the actual parser and record the difference.

First tell apart named stages, numeric stages, scratch and genuine external images, then resolve effective references according to ARG scope, defaults and this run's overrides.
When the project requires Harbor defaults, verify both defaults and actual overrides, so CI parameters do not switch the source back to the public internet.
If any dynamic source cannot be determined, report the gap; one Harbor FROM line does not make the whole graph compliant.

Packages, URLs and extra contexts downloaded by RUN during the build are other dependencies, handled per the project network and supply-chain policy.
"All images come from Harbor" does not imply the whole build is offline or reproducible.
Ordinary make tasks that build no image are not required to have a Dockerfile.

## Identity, release and cost

CI machine identity, credential injection/revocation and credential helpers are maintained by the project's approved execution infrastructure.
This skill does not read the host's real Docker configuration, does not request credentials, and does not write secrets into Dockerfile/ARG/ENV layers or build logs.
Images do not carry the project's AI working directory, private configuration or task records.

The pipeline stores build input digests, tool versions, both digest kinds (index/child manifest), platforms and verification receipts.
Callbacks or job status must match this run's image identity; re-pushing the same tag means old receipts cannot sign off the new content.

Configure scan/signature/attestation gates as the task requires; do not add supply-chain platforms on your own.
Retain the data plane: scanner version, vulnerability database time, signer and trust basis, SBOM coverage.
When verification is impossible, deliver the gap; do not disable a gate to pass.

Estimate time separately for source pull, build, upload, full target download, per-platform runs and waits on asynchronous gates.
Calibrate with actual bytes/architecture strategy/cache hits; do not convert the number of subtasks into upload speedup; same-tag releases stay serial.
After completion, verify actual duration, repeated downloads and unverified items, and feed them back into the next budget.
