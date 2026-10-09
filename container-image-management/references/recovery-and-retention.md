# Recovery and retention

The operation record keeps at least the pinned source identity, old target identity, expected new content graph, steps, results, in-flight work and stop conditions; it stores no credentials.
A failed sync or build does not automatically delete the target, nor directly deploy the old version.

## Failure branches

| Situation | Next action |
| --- | --- |
| Push timeout/process interrupted | Stop further writes; confirm the original process's final state, then read the target tag and expected content graph read-only. If it cannot be verified, keep UNKNOWN |
| Target already equals expected and content is complete | Record that the response was lost but the operation completed; do not push again |
| Tag not updated, some content already uploaded | Mark partially complete; resume within bounds by pinned digest only if the original operation has stopped and the original authorisation/writer is still valid |
| Target shows another digest | Treat as a conflict and stop overwriting; check for other writers; do not retry to win it back |
| Tag correct but child manifests/layers missing | Release failed; keep known references and do not delete the index first; after repairing content within the approved scope, fully re-verify affected graphs |
| 401/403, immutability rejection, quota, TLS failure | Report a prerequisite gap; do not loop logins, change certificate verification, global rules or account permissions |
| 429 or recoverable network failure | Respect Retry-After and the task time/attempt budget; before each retry verify whether the previous attempt produced a write |

Rolling back a tag is also a write and needs matching scope and an exclusive writer; verify the old content graph is still complete and meets current policy.
Do not assume deleting the new artifact restores the old tag.

## Three cleanup actions

1. **Detag** removes only the specified tag from the specified artifact.
   The Harbor API shape is DELETE on `/api/v2.0/projects/{project}/repositories/{repo}/artifacts/{reference}/tags/{tag}`.
   Even with a tag as reference, the delete-artifact endpoint is not detag; prefer binding to a verified artifact digest, and verify tag ownership before and after.
   Parameter encoding follows the server API contract; nested repos must not be concatenated from unencoded strings.
2. **Delete artifact** acts on `/artifacts/{reference}` and affects the manifest, its tags and possibly associated objects.
   First list parent indexes, other tags, attachments, deployment references, restore points and retention policy.
   Untagged does not mean unreferenced; do not delete children an index needs because the list "looks redundant".
3. **GC/retention jobs** have wider impact and may be asynchronous. Do not run them without an explicit task requirement.
   When required, first verify the version's dry-run/candidate support, active uploads, protected set, recovery strategy and final job evidence; do not use GC as a shortcut to delete one tag.

"Create no per-architecture staging tags" differs from "clean historical architecture tags": the latter needs an exact list explicitly allowed for this run.
One upload authorisation does not extend to cleaning the whole target Harbor project.
When the project only requires detag, reject tool paths that delete artifacts.

Before each deletion re-verify object identity and references; when the response is unknown, query first, and do not assume repeating DELETE is safe.
At the end, verify retained tags, indexes, child manifests and layers are still retrievable.
Routine cleanup handles only local temporary directories/caches owned by this run.
Formal evidence and licenses are archived per the project retention method; do not keep copies of all layers indefinitely.
