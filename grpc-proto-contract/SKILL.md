---
name: grpc-proto-contract
description: Design, change or review Protocol Buffers and gRPC contracts, assessing schema evolution, generated code and mixed-version runtime behaviour. Use for proto changes, client upgrades and compatibility failures; do not expand into a whole-protocol overhaul just because ordinary business code calls gRPC.
metadata:
  version: "0.1.0"
---

# Protobuf and gRPC contracts

Give a scoped, re-verifiable compatibility verdict and the minimal change. Distinguish design, review and approved implementation; a review does not automatically authorise generation, upgrades or releases.

## Confirm inputs

Locate the following from the task and the project contract, reusing existing material:

- Identity of the old/new schema or descriptor, release history, syntax/edition, imports and the symbols changed this time.
- The actual encodings: binary, ProtoJSON, TextFormat, transcoding gateways; whether persisted messages exist in databases, queues, caches or events.
- Inventory of services and consumers, including independently released clients outside the repository, languages, generators, protobuf/gRPC runtimes and JSON options.
- Mixed-version duration, upgrade order, rollback version and window; the declarations and generated targets allowed to change, and the sole writer.

Without the old schema, backward compatibility cannot be judged from the new file; without a consumer inventory, the verdict is limited to known consumers. List the gaps and the verdicts they block; you can still review the new design, organise the symbol diff and list scenarios pending verification. When the old version cannot be found, do not install tools and do not pick a baseline out of thin air.

## Choose the method by change

1. Compare fully qualified symbols: field number/name/type/cardinality/presence/oneof, enum values and reserved entries, RPC path/input/output/streaming mode, and options that affect the generated API. Match the existing style; do not renumber in the name of tidying up.
2. For each change, judge **binary, JSON/text, source/generated API, behavior** separately. Passing one does not cover the others; declaring an encoding not applicable needs evidence.
3. For field, enum, storage or generation changes read [schema-evolution.md](references/schema-evolution.md); for RPC, identity, error, timeout, retry or streaming changes read [grpc-runtime-contract.md](references/grpc-runtime-contract.md).
4. Cover old write -> new read, new write -> old read, a new message modified and re-serialised by an old peer, historical messages read after upgrade, and rollback after new writes have happened. For RPCs also verify old client -> new service and new client -> old service; run them with the actual languages and versions.
5. Write down the limits of conditional compatibility and the evidence that lifts them: who upgrades first, when new values are allowed, how persisted data migrates, how to roll back. Choose the smallest change that meets the need; do not add a new RPC, version, stream, Buf or protovalidate by default.

## Generation and evidence

First verify the project's existing check entry points, command side effects and offline inputs. Keep a single generation source; pin the input/import closure, plugin versions/parameters, output directory and expected files. Generate within the approved scope and verify the full diff; do not hand-edit generated code to mask a schema problem. Connections, credentials, timeouts and retry policies are maintained by consumers per project convention; do not stuff them into the declaration package without reason.

Record separately the input identity, command/version, exit code, evidence location and limits:

| Check | What it proves | What it does not replace |
| --- | --- | --- |
| protoc/descriptor compilation | Declarations, imports and the compiler used accept the input | Compatibility with the old baseline and runtime behaviour |
| lint | The currently enabled style/static rules | breaking and business semantics |
| breaking check | Differences covered by the configured rules against the specified old baseline | Actual language clients, persisted data and passing all four dimensions |
| Generator/runtime and client verification | Behaviour of the tested versions in the specific scenarios | Untested clients, real proxy/TLS/deployment environments |

Without Buf, use existing protoc, descriptor diffs and client fixtures; without those tools, provide a static review and a to-run checklist, explicitly marked unverified. When the baseline, tools or dependencies are missing, do not install, do not swap approved inputs and do not fake a pass; if a proposed command would exceed project permissions, stop that action. In-memory transport or bufconn does not prove real TLS, gateway or release compatibility. Results against temporary local dependencies do not replace re-verification against the final release dependencies.

## Delivery and review

Use [contract-review.md](assets/contract-review.md) for the review artefact; if an existing format is in place, add the equivalent information. Choose the verdict from "compatible within scope / depends on release order or value range / breaking / insufficient context", and state the actual degree of verification. Each finding gives location, old -> new change, affected dimensions, failure path, minimal fix and verification evidence. Style preferences must not pose as compatibility blockers.

Pick normal and counter examples by change:

- Adding an ignorable field.
- Missing old baseline or out-of-repository consumers.
- Historical messages containing a deleted field.
- Zero-value presence round trip.
- Read-modify-write of unknown enums and oneofs.
- New generated code with an old runtime.
- Side effect took effect but the response was lost.
- Stream half-close, slow reader, cancellation.

Author self-check does not replace independent acceptance.

Mechanical inventory may use low/low; cross-language, authentication/authorisation, concurrency and conflicting evidence use normal/high. Grade words map to actual execution configuration through the project resource mapping; no model is fixed.

On interruption save the input versions, generation scope, what has/has not run and in-flight state; continue only after confirming the original writer has stopped. When versions or semantics change, re-check the relevant official material and fixtures; do not treat a historical pass as today's pass.

## Sources

1. Pinned sources: PB01 [protobuf entry](https://github.com/bufbuild/claude-plugins/blob/c4766e5fff1b52283f38bd61122103efe58c60fd/plugins/protobuf/skills/protobuf/SKILL.md), [evolution best practices](https://github.com/bufbuild/claude-plugins/blob/c4766e5fff1b52283f38bd61122103efe58c60fd/plugins/protobuf/skills/protobuf/references/best_practices.md); GH02 [protobuf-grpc-api-review entry](https://github.com/github/awesome-copilot/blob/7cce7cfb4b61196c36d7e8eb8475ae84b356b126/skills/protobuf-grpc-api-review/SKILL.md), [compatibility](https://github.com/github/awesome-copilot/blob/7cce7cfb4b61196c36d7e8eb8475ae84b356b126/skills/protobuf-grpc-api-review/references/protobuf-compatibility.md), [runtime](https://github.com/github/awesome-copilot/blob/7cce7cfb4b61196c36d7e8eb8475ae84b356b126/skills/protobuf-grpc-api-review/references/grpc-contract-review.md).
2. Adopted the match-existing-style approach, evolution checks, the four dimensions and the mixed-version method, reorganised; generation scope, identity trust and failure evidence methods are own-authored for this package, and the topic pages cite official semantics.
   Dropped mandatory new tools/new validation on every field and "adding to a oneof is unconditionally safe".
3. License: shipped with the package as [LICENSE-PB.txt](LICENSE-PB.txt) (PB, Apache-2.0) and [LICENSE-GH.txt](LICENSE-GH.txt) (GH, MIT); modification notes in [NOTICE.md](NOTICE.md); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license files along when copying this package alone. Each part is governed by its own license; there is no single unified license statement.
