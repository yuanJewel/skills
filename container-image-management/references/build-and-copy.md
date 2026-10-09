# Build and copy

This page is the basis for choosing commands; examples are not executed.
First verify version/feature help, the approved target, tool capabilities, authentication boundary, TLS trust, writer and budget; do not auto-install tools or change host configuration just to make it work.

## Sync an existing image

Prefer copying the pinned content graph; pulling only the local platform and then doing a plain tag/push drops the other platforms.
Copying only the index JSON may leave missing child manifests or layers.
Use a tool that supports recursive transfer and handles target repository references, media types and attachments.

The official Buildx cross-registry example supports `imagetools create`; the concrete version still has to be verified.
The [pinned implementation](https://github.com/docker/buildx/blob/2b1e4d8995b3cf35e3ee9d86e913e4a687f8b2bd/util/imagetools/create.go) contains CopyChain; this does not mean every older version or attachment type is compatible.
CLI documentation and the actual copy path sit at different layers: do not infer from "create manifest" alone that layers are never transferred, and do not sign off field tool success just because the source code exists.

The verified source child manifests matching the project platform set can be combined directly into one release tag.
The example below uses two platforms; the command shape is as follows. The executor fills in variables within task scope; never concatenate unverified shell strings:

```sh
docker buildx imagetools create --dry-run \
  --tag "$target_ref" "$source_ref@$digest_a" "$source_ref@$digest_b"
# Only after approving the dry-run result, attachment policy, target identity and write permission does the same command without --dry-run perform the write.
```

`--dry-run` does not publish but may still need network reads.
When a complete source index already exists and its platform/attachment set exactly meets the requirement, copy it by index digest; do not blindly split and recombine.
When filtering child manifests into a new index, the new index digest may differ from the source; do not misread that as child images being altered.

Verify, against the source attachment list, which artifactTypes, index-embedded attachments and external referrers the copier actually supports.
Recursively copying layers does not copy all attachments; the upstream implementation may filter types.
Every attachment that must be retained needs a target identity and an accepted subject association; when unsupported or discovery is incomplete, do not sign off attachment delivery.
If the target relies on a tag-based attachment scheme, first verify it is compatible with the project tag policy (e.g. single release tag).
Do not treat the scheme's tags as an approved exception on your own, and do not delete them to hide the conflict.

A project that forbids per-architecture staging tags cannot create `-amd64/-arm64` tags "to delete after use", nor point the release tag at a single architecture temporarily.
If the chosen tool can only work through staging tags, the current path is BLOCKED; offer digest-addressed upload/local OCI output as alternatives, and do not silently relax the policy.
Untagged layers, child manifests and attachments are normal content objects, not forbidden staging tags.

## Build multi-platform images yourself

First pin source/dependencies, Dockerfile, context and ignore rules, all external images and builder platform capabilities.
For cross-compilation distinguish BUILDPLATFORM from TARGETPLATFORM; CGO, native dependencies and install scripts cannot be assumed compatible just by setting GOARCH.

```sh
# Command shape for an approved execution phase only; this page grants no push permission.
docker buildx build --platform "$platforms" \
  --file "$dockerfile" --tag "$target_ref" --push "$context_dir"
```

Verify that every approved platform succeeded and the actual output index/manifests match that set; failure of any approved platform blocks signing off a complete release.
On failure read the target state; do not promise that build/upload is an atomic transaction across all objects.
When the project requires isolated testing before release, verify with local OCI output first, then publish within the approved scope; do not create forbidden remote staging tags for testing.

BuildKit may produce attestation attachments. One release tag may point to an index containing attestations; do not disable provenance/SBOM to make the UI row count look tidy.
If the format the project requires conflicts with tool output, list the concrete differences.
Do not equate single-platform `--load` success with a complete multi-platform image having been saved.

## Release tag changes

Before initiating, record the target's old digest (record its absence too) and the intent.
Same name with the same content may move on to verification; different content requires overwrite authorisation for this run.
Do not bypass immutable-tag, permission or quota rejections by deleting tags, disabling immutability or switching projects.
Write to the same target exclusively; a re-read can only detect drift that already happened and gives no server-side CAS guarantee.
If exclusivity cannot be established, stop updating that tag.

After a success response, proceed to target integrity verification; a timeout enters UNKNOWN and is verified per the recovery reference, without an immediate re-push.
Scan, replication and signing jobs may be asynchronous: obtain their final state and the corresponding digest, and do not let push completion replace all later gates.
