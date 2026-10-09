# Harbor and content integrity

Read when planning an upload and when accepting it afterwards.
First verify whether the target is a normal project or a proxy-cache project; proxy-cache projects offer no normal push entry.
Harbor version, project quota, immutability policy, media-type support and an authorised executor are prerequisites; do not auto-create projects, change global policy or widen robot account permissions.

## Layered verification

| Layer | Required observation | Signals that cannot replace it |
| --- | --- | --- |
| Tag | The exact target tag currently resolves to this run's index/manifest digest; record the time | A local image of the same name, the target string printed by the command |
| Platform graph | Target raw index; each required platform maps uniquely; OS/arch/variant of child manifest and config agree | Platform text in Harbor lists, descriptor platform fields alone |
| Content present | Responses fetching every child manifest/config and all layers from the target repository; verify digest/size; trace the download origin | Source repository readable, HEAD 200, pulling only the default architecture |
| Actual retrieval | An isolated empty content store pulls full content from the target by each child digest; the downloader verifies hashes; record per-platform results | Cached image showing Already exists, local inspect |
| Attachment relations | Per the source list, verify each target attachment's digest, subject, artifactType and content; reverse-look up associations from the target via the agreed discovery mechanism; verify pagination/filtering | No attachments in the index, downloading only image layers, copy command supporting a few attachment types |
| Runnable | A native/approved emulated environment matching the platform runs the minimum functionality the task requires; note emulation limits | Pull success, uname text under QEMU, a run on another platform |
| Additional project gates | Scan/signature/attestation verification for the specified digest and actual Harbor UI observation | Index exists, scan queued, signature attachment file exists |

During content verification, trusted object-storage redirects used by the target deployment may belong to the target service.
First verify allowed download hosts and the scope of authentication forwarding; never forward authentication headers to arbitrary redirect hosts.
Never fall back to the source repository to mask missing target layers.
An external/foreign layer that has only a URL does not make the target self-contained; do not auto-fetch unknown addresses, and list them separately per the project's allowed policy.

When implementation conditions are insufficient, it is acceptable to stop at "target manifest checks passed, full pull unverified".
Do not turn emptying the cache into a global Docker prune; use the isolated content store/tool workspace approved for this run, and record its creation and cleanup.
Layer verification may reuse downloads of the same digest, but platform mapping and results are still listed item by item.

## Harbor observation

The API can query an artifact and its tags by digest; handle pagination, with_tag and similar parameters per the actual version's contract.
When a list lacks an object, first verify pagination/filtering/permissions; do not conclude it was deleted.
An index's child artifacts and attachments may be shown separately, and views vary by version.
If the project requires a single release version tag, that requirement can be verified; no version of the UI is guaranteed to show only one row.
When a specific UI appearance is required, observe it and state the view; do not delete required child objects to fit a screenshot.

Give pass/fail/unverified separately for full retrieval, attachment retention, run, vulnerability scan and signature trust.
Attachment bytes present but the subject relation missing means retention verification is still incomplete; unsupported or non-exhaustive attachment discovery must not report "no attachments".
When attachments are a project requirement, missing ones block complete delivery.
For tasks requiring only image content, state the verification scope explicitly; do not claim a complete supply-chain attestation was retained.
Old scan reports need the scanner/database time verified against the current digest; signatures need identity/trust policy verification, and a recomposed index may lose coverage by the original index signature.

The method does not presume the consuming project must add a particular scanner or signing infrastructure.

Final delivery: source/target index, selected child digests, platform and attachment lists, verification time, actual download/run scope and remaining conditions.
If a tag change happens outside the writer, report the current drift; do not use an earlier PASS to sign off the current tag.
