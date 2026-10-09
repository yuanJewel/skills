# Host dispatch adapters

Read this page when mapping a generic task brief onto actual tools. Do not write one platform's call names, maximum slots or model IDs as cross-platform facts.

## Capability check

Record host/client and relevant versions, available dispatch and query interfaces, the dispatch method the user authorised, executor and reasoning options, whether the actual run configuration can be queried, and what stop and completion mean. Configuration comes from the current tool declaration and the project's execution-channel configuration; documentation examples and historical error text are only clues pending verification.

- Grade-word mapping supported and actual model/reasoning returned: record as verified after checking request against response.
- Accepts a model only, no reasoning parameter: omit the unsupported field and record the capability limit. When, say, a lightweight model has no native effort setting, do not submit a fake parameter or claim high took effect.
- Host inherits the parent configuration automatically: record the inheritance method and verifiable information; without an actual run report do not write "execution channel verified effective".
- Required resource/mode unsupported: choose a compatible option within current authorisation or report the gap; never switch to an unauthorised execution channel on your own.

## Calls and exceptions

Save the logical task and reservation before the dispatch call; associate the real handle immediately after the call returns one. A short task name must not pose as a platform handle. Before retrying, query the original request: if it already started, continue it; only if clearly not started make a new attempt; if the query is inconclusive keep the occupancy. A sent stop request proves only that it was sent; write permission transfers only after the termination fact is obtained.

Read-only reviewers receive a fixed candidate location and content identity, write their own findings and do not modify the object under review. Rework is done by the current writer, who refreshes the content identity, after which affected items are re-reviewed.

## Reading and message size

On receiving artefacts, read the fixed header, locations and content identifier first, then the necessary evidence by section. A project may limit lines and bytes together; long lines are also read by field. Truncated output is not the whole file — fetch missing segments separately; after a file refresh, recalibrate section locators. On request-body/context errors, record client, gateway, model version, time and error evidence, then locate the failing layer; do not derive a universal limit from a single status code.

After successful acceptance send a brief notification; detailed evidence stays in files. A visible message does not equal real host discovery, authorisation or passed resource verification.
