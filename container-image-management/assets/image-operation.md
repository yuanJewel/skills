# Image operation and evidence

Filled in by: the current executor; an existing equivalent receipt can be extended directly.
Without evidence write unverified, never "passed by default"; never record passwords, tokens or authentication headers.

- Task/mode/allowed actions: {{plan, review, sync, build, cleanup; approved scope}}
- Project policy and pinned inputs: {{version/location; platform set, release tag and intermediate-object limits}}
- Source identity: {{input tag, resolution time, source index digest; for builds also list source code and input digests}}
- Target identity: {{target repository:tag, previous digest or absent, expected graph, sole writer}}
- Tools and target capabilities: {{Docker/Buildx/Harbor versions, project type, required features and verified results}}
- Resources/duration: {{disk, expected download/upload bytes, builder, effective work and wait budget}}

| Platform/variant | Source child digest | Target child digest | Config/layers fully retrieved | Native/emulated run | Reason unverified |
| --- | --- | --- | --- | --- | --- |
| {{platform}} | {{digest or n/a for builds}} | {{digest}} | {{time/evidence}} | {{environment/result}} | {{gap}} |

- Index and attachments: {{final digest; embedded/external discovery mechanism and completeness; per-attachment source/target digest, subject, artifactType; pagination/filter/unsupported scope; selection/retention/signature impact}}
- Current state: {{PREPARED/RUNNING/VERIFIED/PARTIAL/FAILED/UNKNOWN; last observation}}
- Initiation and recovery: {{operation identity, start/end, stopped/in-flight, retry count, next safe action}}
- Layered evidence: {{separate conclusions for tag, graph, full pull, run, scan/signature, UI}}
- Cleanup: {{detag only or artifact/GC; exact allowed objects, retained references, before/after verification}}
- Delivery: {{completed, limits, actual duration versus budget; image verification does not stand in for business go-live}}
