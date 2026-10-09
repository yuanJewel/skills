# Third-party sources and modification notice

This package is a reorganisation with independent supplements; it is not a verbatim redistribution of any upstream. This notice and both complete licenses must be distributed with the adapted parts; this file keeps the minimal attribution and scope, and the library-wide summary is in the root THIRD_PARTY_NOTICES.md. Upstream NOTICE files that were not found or not provided are not fabricated by this package; this file is this package's source/modification statement and does not pose as an upstream NOTICE.

## 1. PB01: Apache License 2.0

- Upstream: bufbuild/claude-plugins
- Pinned version: c4766e5fff1b52283f38bd61122103efe58c60fd
- Files: plugins/protobuf/skills/protobuf/SKILL.md; plugins/protobuf/skills/protobuf/references/best_practices.md
- Original: https://github.com/bufbuild/claude-plugins/blob/c4766e5fff1b52283f38bd61122103efe58c60fd/plugins/protobuf/skills/protobuf/SKILL.md
- Appendix: https://github.com/bufbuild/claude-plugins/blob/c4766e5fff1b52283f38bd61122103efe58c60fd/plugins/protobuf/skills/protobuf/references/best_practices.md
- Copyright 2026 Buf Technologies, Inc.
- Complete license in LICENSE-PB.txt (kept verbatim from the pinned version).
- Adapted parts: in SKILL.md, matching existing style, on-demand references and the evolution/verification route; in references/schema-evolution.md, the related methods for reserving field numbers/names, presence and evolution checks.
- Modifications: rewritten and reorganised with other sources; dropped mandatory Buf, protovalidate, installation/dependency updates and unscoped generation; changed the unconditional-safety claim for adding to a oneof into a mixed-version read-modify-write judgment; not all of its style preferences adopted.

## 2. GH02: MIT License

- Upstream: github/awesome-copilot
- Pinned version: 7cce7cfb4b61196c36d7e8eb8475ae84b356b126
- Files: skills/protobuf-grpc-api-review/SKILL.md; skills/protobuf-grpc-api-review/references/protobuf-compatibility.md; skills/protobuf-grpc-api-review/references/grpc-contract-review.md
- Original: https://github.com/github/awesome-copilot/blob/7cce7cfb4b61196c36d7e8eb8475ae84b356b126/skills/protobuf-grpc-api-review/SKILL.md
- Compatibility: https://github.com/github/awesome-copilot/blob/7cce7cfb4b61196c36d7e8eb8475ae84b356b126/skills/protobuf-grpc-api-review/references/protobuf-compatibility.md
- Runtime: https://github.com/github/awesome-copilot/blob/7cce7cfb4b61196c36d7e8eb8475ae84b356b126/skills/protobuf-grpc-api-review/references/grpc-contract-review.md
- Copyright GitHub, Inc.
- Complete license in LICENSE-GH.txt (kept verbatim from the pinned version).
- Adapted parts: in SKILL.md, compatibility scope/four-dimension judgment/mixed versions/evidence boundaries; in both references, the frameworks for evolution, runtime behaviour and failure checks; in assets/contract-review.md, the four-dimension and mixed-version record skeleton.
- Modifications: reorganised, adding missing-input branches, project scope limits, generator/final dependency verification, metadata trust boundaries, and lost-response and stream-close assertions. Refined oneof unknown members, reserved names, cancellation and retry conditions per official semantics.

## 3. Independent supplements and official semantics

Generation scope and evidence layering, the produce/validate/forward/clean-up handling of identity fields, the review steps for idempotency and unknown results, and the template's record fields are independently designed for this package or extensions of the methods above. They distil the single declaration source, consumer policies and final dependency re-verification from existing working methods, without carrying project identities or paths.
The official protobuf.dev and grpc.io pages are used only to verify technical semantics; no manual passages are copied wholesale. Specific links sit next to the relevant topic judgments, and the official web page licenses are not conflated with the licenses of the two code repositories above.
This package declares no single unified license, does not relabel the Apache part as MIT, and does not misattribute the MIT part to Buf. The independent supplements do not revoke the copyright, license and modification notice obligations of the adapted parts.

## Modification record

- 2026-10-09: 0.1.0 initial public version, content as above.
