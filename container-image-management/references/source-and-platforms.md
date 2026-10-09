# Source and platforms

Read during preparation. First list the complete platform set the project requires, distinguishing OS, architecture, variant and runtime ABI.
`arm64` is not `arm/v7`; `amd64` and `arm64` images cannot be swapped by editing descriptor fields.
Different consuming projects may require different platforms; do not hard-code one project's two-platform requirement.

## Pin the content graph

1. Record the human-supplied tag and resolution time, and resolve the source to an index or single-manifest digest.
   Read by digest from then on; a later change of the source tag does not change this run's input.
2. Read the raw index and every selected child manifest/config to form `platform -> child digest -> config and layer digests`.
   Verify media type, size, digest and the config's OS/architecture.
   Recurse into nested indexes within bounds; cycles, unrecognised objects or incomplete reads stop at a gap.
3. An index may contain attached artefacts such as SBOM, provenance or signatures; `unknown/unknown` is not automatically a third runnable platform and must not be deleted directly.
   Classify by mediaType, artifactType, subject/annotations and actual content; list unrecognised ones separately as unverified.
   Filtering to two platforms may drop attachments or invalidate the source index signature; handle per the approved attachment retention policy.
4. No attachment entries in the index does not prove there are no attachments.
   Per the project attachment policy, also look up external referrers whose subject is the source index or a selected child digest.
   Use the OCI referrers API, Harbor attachment queries or the established tag-based attachment convention that the actual version supports; record mechanism, subject, artifactType, digest and content dependencies.
   Verify all pages, filters and responses; do not treat unsupported, permission-denied or filtered-empty sets as exhaustive.
   An OCI 1.1 404 requires a trusted client to fall back to the referrers tag schema per the spec; if the fallback is unverified or reading is not authorised, record discovery as incomplete.
   Expand attachments required by policy and their dependencies within bounds; when the budget limit is reached, keep it incomplete.
5. When a sync preserves the selected child manifest bytes, target child digests should equal the source.
   Rebuilding, format conversion or recompression changes identity; that is a different operation and must not be passed off as the original image.
   After an index is recomposed, a signature pointing at the old index still proves only the old subject; do not alter the subject to pretend the signature is still valid.

## Branches

| Observation | Decision |
| --- | --- |
| Upstream lacks an approved platform | Block a release that must satisfy that platform set; list alternative versions or a rebuild plan; do not silently reduce scope |
| Multiple candidates for the same platform / variant unclear | Compare actual CPU/ABI with project input; do not take the first array element |
| Source is single-architecture and the local machine can pull it | Proves only that architecture is retrievable, not multi-platform |
| Tag drifted but the pinned digest still exists | Continue with the approved digest; if the source should be updated, list the difference separately |
| Image attestations unknown or tool unsupported | State the retained gap explicitly; do not disable attestations or skip signature verification by default |

When the user asks for a local pull, pull per platform and source digest and record what actually ran; a read-only inspect cannot sign off for it.
Run verification needs matching hardware or an approved emulator; record pull and run separately.
When source licensing/trusted identity is unclear, do not promise the user the artefact can be redistributed.
