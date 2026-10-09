# Protocol contract review

How to fill in: trim this template to the changes at hand; an existing review artefact may add the equivalent fields. Unfilled items are not evidence of a pass; for items not involved write not applicable with the basis. All results come from actual observation, never back-filled from expectations. This template is an adaptation of the four-dimension method plus an own-authored record structure; license scope is in the package NOTICE.

## Verdict and scope

- Verdict: {{compatible within scope / depends on release order or value range / breaking / insufficient context}}
- Degree of verification: {{static inference, actual run coverage and unverified boundaries}}
- Task/approved scope/writer: {{goal, mode, changeable declarations and generated targets}}
- Old schema/descriptor: {{identifier, release basis, imports/options}}
- New schema/descriptor: {{identifier, diff location}}
- Encodings and options: {{binary / ProtoJSON / TextFormat / gateway; unknown field and enum name/number policy}}
- Persisted messages: {{format, location category, retention/replay window, allowed masked or synthetic samples}}
- Mixed versions and rollback: {{old/new versions, duration, rollback target, irreversible data steps}}
- Missing inputs: {{what is missing, which verdicts are blocked, what can still be completed}}

## Consumers and tool versions

| Consumer/service/data job | Independently released outside the repo | Language and version | Generator/plugin/parameters | protobuf/gRPC runtime | Evidence or unknown |
| --- | --- | --- | --- | --- | --- |
| {{object}} | {{yes/no/unknown}} | {{version}} | {{version}} | {{version}} | {{source}} |

## Four-dimension change matrix

One row per changed symbol; compatibility in one dimension does not cover another.

| File/fully qualified symbol | Old -> new (number/name/type/presence/path etc.) | binary | JSON/text | source/generated API | behavior | Verdict/prerequisite/evidence |
| --- | --- | --- | --- | --- | --- | --- |
| {{symbol}} | {{change}} | {{verdict}} | {{verdict}} | {{verdict}} | {{verdict}} | {{evidence}} |

## Key findings

| Severity and location | Failing version/path/input | Concrete impact | Minimal fix or migration condition | Evidence and verification plan |
| --- | --- | --- | --- | --- |
| {{graded by actual impact}} | {{reproducible condition}} | {{lost value/rejection/compilation/duplicate side effect etc.}} | {{change and boundary}} | {{fact or pending verification}} |

## Mixed-version and storage verification

| Path | Sample and old/new versions | Expectation (value/presence/unknown value/final state) | Actual/evidence/reason unverified |
| --- | --- | --- | --- |
| Old write -> new read | {{input}} | {{assertion}} | {{result}} |
| New write -> old read | {{input}} | {{assertion}} | {{result}} |
| New write -> old peer modifies -> new read | {{unknown field/oneof/enum}} | {{assertion}} | {{result}} |
| Old write -> new peer modifies -> old read | {{deleted field/unknown payload/old semantics}} | {{assertion}} | {{result}} |
| Old persisted message -> read/replay after upgrade | {{historical encoding/validation}} | {{assertion}} | {{result}} |
| New data already written -> roll back to old peer | {{new value/dual write}} | {{assertion}} | {{result}} |
| Old client -> new service | {{RPC/version}} | {{assertion}} | {{result}} |
| New client -> old service | {{RPC/version}} | {{assertion}} | {{result}} |

## Runtime topics (fill only affected items)

- Deadline/cancel: {{total budget/per-hop limit, propagation evidence, task and downstream cleanup after cancel, final state on both sides}}
- Interceptors and identity: {{unary/stream chain order, authentication and authorisation, trusted source and forwarding scope of the original caller}}
- Metadata: {{key/producer and validator/repeated values/limits/masking in logs and errors/cleanup between requests}}
- Status/details: {{old and new codes, business codes, structured types, old-peer degradation and proxy preservation}}
- Retries: {{actual layers and counts/overall deadline, idempotency or reconciliation method}}
- Response lost after commit: {{injection point; number of business effects and results for repeated requests/same key different payload/concurrency/restart}}
- Streaming: {{backpressure/bounded queues, half-close and final status, cancellation releasing waits, long-stream identity, optional resume protocol}}
- Resources: {{message size, element count/nesting complexity, fan-out/in-flight limits, validation before expensive or side-effecting work, evidence for at-bound/over-bound/cancel reclamation}}

## Generation scope and check ledger

- Input/import closure: {{exact files or fixed list}}
- Generation entry/tools/parameters: {{actual versions; scope of verified command side effects}}
- Allowed output: {{directories, expected added/changed/deleted}}
- Actual diff: {{all files; out-of-scope diffs and their handling}}
- Final consumer dependencies: {{release identifier, whether temporary dependencies were removed, re-verification result or unverified}}

| Check | Fixed input/baseline/rules | Actual command and version | Exit code/evidence | Scope not proven |
| --- | --- | --- | --- | --- |
| protoc/descriptor | {{input}} | {{command or tool missing}} | {{real result}} | Not compatibility |
| lint | {{rules}} | {{command or not run}} | {{real result}} | Not breaking |
| breaking | {{old baseline/rule set}} | {{command or not run}} | {{real result}} | Not client/behaviour |
| Generation/compilation/runtime pairing | {{language matrix}} | {{execution method}} | {{real result}} | Untested languages/versions |
| Client/fault/storage fixtures | {{scenario}} | {{execution method}} | {{real result}} | Real TLS/proxy/deployment etc. |

## Release, rollback and handover

| Phase | Prerequisite evidence/write limits | Action and owner | Stop on failure/recovery |
| --- | --- | --- | --- |
| Compatible readers ready | {{readers covered}} | {{action}} | {{recovery}} |
| New writes and necessary dual writes | {{value range, conflict precedence}} | {{action}} | {{recovery}} |
| Persisted data migration | {{backup/backfill validation}} | {{action}} | {{irreversible handling}} |
| Close rollback/retire old peers | {{evidence that old consumers and replay have exited}} | {{action}} | {{stop condition}} |

Unfinished/unverified: {{object, reason, next step and owner}}. In-flight operations and continuation inputs: {{actual state}}. Record author self-check and independent review separately; this review verdict does not replace release authorisation.
