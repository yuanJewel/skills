# Schema evolution and generation scope

Use when fields, enums, encodings, the generated API or persisted messages change. This page is adapted from and extends the PB01/GH02 methods; sources and license are in the package [NOTICE](../NOTICE.md). First verify the actual syntax/edition, language and version; the judgments below cannot be extrapolated directly across versions, encodings and consumers.

## 1. Establish comparable old and new inputs

Record the old/new schema or descriptor identifiers, imports and custom options, release scope, encoding options and consumer versions. If the descriptor lacks source comments, it cannot prove that documented semantics are unchanged. With only the new file you can check structure, but mark every "old -> new" verdict as insufficient context.

List changes by fully qualified name: field number/name/json_name/type/cardinality/presence/oneof/default; enum number/name/alias/zero value/reserved; RPC request/response/streaming mode/path; language package, namespace, file location and generation parameters. For numbers with unclear release history, do not infer from "currently unreferenced" that they were never used. Adjustments to drafts with evidence of never having been released and no persisted data are handled within that limited scope, without applying a released compatibility window.

Consumers include old binaries, regenerated applications, independent SDKs, transcoding layers, reflection/registry users and jobs that read or write persisted data. Zero search results in the repository do not prove nobody outside uses it.

## 2. Give the four-dimension verdict item by item

| Change | binary | JSON/text | source/generated API | behavior |
| --- | --- | --- | --- | --- |
| Add an ordinary field with a new number | Usually parseable; verify unknown field preservation | Old parsers may reject the new key | Verify generated API and hand-written adapters | Defaults, validation and business-required may break old requests |
| Delete a released field and reserve its number/name | Old data becomes unknown fields; verify the preservation path | reserved does not make old JSON automatically accepted | Removed accessors can break compilation | Old values being ignored may change behaviour |
| Same number, field name changed only | Binary does not depend on field names | Verify old name, new name, json_name and historical payloads | Accessors/reflection change | Masks or rules that depend on field paths need verification |
| Widen int32 to int64 | Old peers may truncate out-of-range values | Verify numeric range, quoted representation and precision | Static types and conversions change | Restrict the written value range until all old readers and rollback are closed |
| Add an enum value | Verify open/closed and runtime | Unknown names may be rejected | Verify exhaustive switches and default branches | Unknown must not map to success/allowed/zero value |
| Add a oneof member | Parseable does not mean the selection is preserved | Verify unknown keys and mutually exclusive representation | case/accessor and exhaustive branches change | Old peers do not know the member; read-modify-write results need real tests |
| Rename/move package/change streaming mode of an RPC | Method identity or interaction shape changes | Transcoding routes affected in step | stub/service interfaces change | Authentication, retries and proxy routing all need migration |

Fill each cell with a verdict and evidence; do not copy "usually" as passed. Mark a dimension that is genuinely unused as not applicable, with evidence of scope.

Type and cardinality changes go through data migration review first, even when the wire type is the same. Go deep only into the conversions involved this time:

- string<->bytes: subject to UTF-8 constraints.
- sint<->plain integer: sint ZigZag encoding is not the same as plain integer encoding.
- singular<->repeated: values may be lost or messages merged; packed numerics in particular cannot be reasoned by analogy.
- map<->entry: duplicate keys or ordering may be lost.

## 3. Numbers, names and deletion

Do not renumber released fields and do not reuse deleted field numbers. On deletion, reserve the number and the name with separate `reserved` declarations; deleted enum values likewise reserve number and name. A declaration that still exists cannot be reserved at the same time. New fields use a legal number that is neither occupied nor reserved; do not backfill historical gaps for compactness.

Reserving a name prevents future schema reuse; it does not keep the original accessor and does not make ProtoJSON recognise a deleted key. TextFormat's special handling of reserved names varies by implementation. Adding reserved alone does not prove historical payloads are readable; verify with the actual parser and old payloads. [Official reserved semantics](https://protobuf.dev/programming-guides/proto3/#fieldreserved)

To replace a field, prefer a new number and new name: first read both, and agree precedence and conflict handling when both are present; then dual-write per rollback needs; verify historical migration and old-peer retirement; finally stop writing/reading the old field and reserve its number and name. Not every compatible addition needs a new RPC or new major version; only when a released contract is genuinely broken, choose a parallel version or migration plan suited to the project.

## 4. Presence, oneof, unknown data

**Presence**: distinguish absent, explicit zero and non-zero. Messages have their own presence; repeated/map usually cannot distinguish absent from empty. An implicit scalar round trip may lose "explicitly set to zero"; after changing to optional, verify not only values but also has/clear, merge, serialisation, defaults and partial updates. When an existing FieldMask/update protocol can express clearing, keep it; do not mechanically force optional. A proto2 default change gives the same absent bytes a different interpretation; required, or new business-required/strict validation, rejects old writers and needs a separate behaviour migration judgment. [Official presence](https://protobuf.dev/programming-guides/field_presence/)

**Oneof**: means "at most one", not "exactly one"; mandatory selection is decided by defined business validation. When a new member is sent to an old peer, case=NOT_SET on the old peer may be an unknown member; do not infer the user selected nothing. An old peer setting a known member is not guaranteed to clear the member it does not know; after re-serialisation both may be present, and back on the new peer the result depends on parse order. Test both paths "new member -> old peer does not modify" and "new member -> old peer modifies a known member"; do not claim a given member is always lost or always kept. Moving into an existing oneof, splitting/merging oneofs and deleting then re-adding can all lose the selection. Moving a single explicit-presence field into a new oneof may be binary compatible, but its generated/behaviour dimensions still need verification. [Official oneof](https://protobuf.dev/programming-guides/proto3/#backward)

**Unknown fields/enums**: verify the read representation by syntax/edition, open/closed enum, generated language and version; do not assume they are all integers or all throw. Use an undefined enum number to test parsing, exhaustive branches, logging, re-serialisation and business authorisation. Do not reject unknown enums by default to "fix" compatibility; decide accept, preserve, reject and error code by boundary needs. A new validation library and `defined_only` are both behaviour changes. Keep the existing meaning of zero values; new enums should prefer an unambiguous zero value, and a released 0 must not be redefined. Enum renames or alias order changes need separate verification of JSON parsing/output by name; do not call it safe just because the number is unchanged. [Official enum behaviour](https://protobuf.dev/programming-guides/enum/)

Unknown fields can disappear in field-by-field copying, JSON round trips, message reconstruction or explicit discarding. Verify with the actual read-modify-write chain, comparing semantics, presence and unknown payload, without requiring identical binary byte order; serialisation is not a general canonical format. If digests/dedup depend on a stable representation, define that protocol separately; do not use a hash of arbitrary serialisation as a cross-language semantic identity. [Unknown fields](https://protobuf.dev/programming-guides/proto3/#unknowns), [Non-canonical serialisation](https://protobuf.dev/programming-guides/serialization-not-canonical/)

## 5. Name-based encodings and stored messages

List separately which schema version ProtoJSON/TextFormat/the gateway uses, whether unknown fields are ignored, whether enums are by name or number, the field name choice and default value output. Ignoring unknown keys only tolerates input; it does not preserve them. New fields, new enum names, changed json_name and deleted old fields all need real bidirectional parsing. Check special mappings involved this time, such as 64-bit integer precision, bytes, time and Any; do not treat an ordinary JSON library as ProtoJSON. [Official JSON evolution](https://protobuf.dev/programming-guides/json/#json-wire-safety)

For stored data, at least establish the formats, maximum retention and consumers in databases/queues/events/caches/replay archives. Use representative masked or synthetic old payloads covering deleted fields, zero values, unknown values, boundary numbers and old validation rules; do not read unauthorised real data for sampling.

| Path | Assertion to verify |
| --- | --- |
| Old write -> new read | Released old values remain interpretable; defaults and validation do not reject legitimate historical records |
| New write -> old read | Written value range stays within constraints; unknown values have defined behaviour and do not grant authorisation by mistake |
| New write -> old read -> modify -> new read | New fields, oneof selection and unknown values do not silently change business meaning |
| Old write -> new peer modifies -> old read | Deleted fields become unknown payload and are preserved as needed; reconstructing a message must not silently drop old semantics |
| Old stored data -> read/replay after upgrade | Historical versions, persisted formats, batch jobs and validation remain supported |
| New values already persisted -> roll back to old peer | Old peer can read, or there are explicit isolation/recovery measures; rollback is not just swapping binaries |

The migration plan writes down the prerequisite evidence for: compatible readers going live, the new-write switch, dual-write conflicts, backfill validation, old-peer retirement and cleanup. When data has already been irreversibly discarded, do not promise recovery by rolling back code alone; state the conditions for backup restore, stopping writes or manual handling.

## 6. Generator and consumer delivery

Before generating, list input files and the import closure, schema identifier, protoc/plugin/runtime versions, options, output directory and expected added/modified/deleted files. Prefer the existing fixed entry point and offline dependencies; if it implies upgrades, network access or out-of-scope writes, narrow the execution first. Do not use full-regeneration noise to mask unauthorised changes, and do not clean up user files directly.

After generating, compare the diff of all files; for unexpected files, first locate parameter/version drift. Verify the generated API, compilation and runtime loading per language; do not equate successful generation with a supported runtime pairing. New generated code with an old runtime is not covered by the general guarantee; verify stricter or looser language rules against their official support ranges separately, and record protobuf and gRPC plugin/runtime versions separately rather than letting one version number stand for all. [Official cross-version guarantee](https://protobuf.dev/support/cross-version-runtime-guarantee/)

protoc proves compilation, lint proves the configured rules, breaking proves that rule set against a fixed old baseline; keep each real exit code. Without a breaking tool you can compare descriptors/sources, but do not call it a pass of that tool. Run old/new generated clients against each supported service version; if only one language exists, state that cross-language is unverified. The contract and consumers may be verified together with allowed temporary dependencies; formal delivery pins the actual release dependencies per the project contract and re-verifies, and temporary-path results must not pose as final results.
