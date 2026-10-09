---
name: documentation-authoring
description: Write or revise human-facing technical, usage and explanatory documentation, organising structure by reader purpose, verifying key facts and checking examples, links and delivery format. Does not author project governance rules or mix session workflow into business documentation.
metadata:
  version: "0.1.0"
---

# Reader-oriented documentation

First establish what the reader should learn, accomplish, look up or understand after reading, then choose structure and evidence.
Use an existing explicit outline, terminology, format and destination directly; do not turn every writing task into another outline approval.

## Inputs and boundaries

From the task and existing documents extract the reader, goal, type, scope, fact sources, terminology/style guide, target format, allowed destination and current writer; organise them with the [document brief](assets/document-brief.md) when needed.
Missing information blocks only the content that depends on it: write the verified parts first, batch clarifications for ambiguities that affect facts or structure, and never fill gaps with invented capabilities.

This is documentation for people, not a carrier for runtime instructions.
Project governance content such as AI collaboration rules goes to the location designated by the project configuration; a business README keeps its product introduction and usage role and does not mix in session IDs, model scheduling or AI work logs.
Legitimate AI product features, copyright and licenses may stay and must not be deleted by keyword.
Authoring a Skill itself uses `skill-maintenance`; the user workbench and continuation status use the contract of `context-handoff`.

## Writing loop

1. **Pick one primary purpose.** A tutorial takes a newcomer to a reachable result; a how-to guide solves a specific problem; reference serves accurate lookup; explanation covers mechanism and trade-offs.
   Organise per [Structure and evidence](references/structure-and-evidence.md); other purposes are supplied via adjacent links, not mixed into a chronological log. Artefact: primary type and section skeleton.
2. **Locate impact and verify facts.** Read the current text and applicable version; locate the sections, anchors, diagrams, tables and examples this change affects.
   Build a [fact check table](assets/fact-check.md) that points key assertions at source code, protocols, user decisions or accepted evidence.
   Old description conflicts with source code -> first clarify version/fact layers; do not silently pick one version. Artefact: fact check table.
3. **Arrange structure before prose.** Arrange headings and information order first, then write the body; adopt a structure the user has given or confirmed directly.
   Stop condition: wait for that decision only when the user explicitly asks for approval, or when structural ambiguity would affect the result.
   State known facts definitely; separate unverified facts from future direction clearly; do not invent percentages, production validation or isolation guarantees.
4. **Support the reader's task.** Support it with concrete operations, prerequisites, expected results and error recovery. Examples use synthetic values only.
   Verify a command's side effects, version and real entry point first, then validate per [Examples and formats](references/examples-and-formats.md); do not run side-effecting examples just to write documentation.
5. **Verify consistency and links.** Verify that the same fact is consistent across body, diagrams, tables, headings, code and conclusions; check link targets, anchors and reader paths.
   For existing documents adjust only what is necessary and keep linkable entry points. When an anchor must change, update related references or record the compatibility handling.
6. **Generate and verify the format.** Generate the specified format and verify the editable source and any necessary preview.
   Layout and rendering of complex DOCX, PDF and slides go to dedicated tools/skills, whose availability is listed in the host capability list or project inputs; this package does not copy their full workflows.
   No rendering capability -> deliver a text draft and record "visual unverified"; a successful build does not mean no overflow.
7. **Deliver.** Artefacts: body text, sources of key facts, unverified items and actual format/readability check results.
   Retention of confirmed deliverables and historical versions follows `archive-maintenance` or existing project rules.
   Publishing or uploading follows this run's authorisation; finishing a document does not automatically mean approval to publish.

## Failure and recovery

When sources are insufficient, keep the assertion list, write the verified parts and mark where content is pending; do not use "expected to" to disguise a capability that was claimed as implemented.
When a link is broken, first determine whether the target was renamed, access is insufficient or the version migrated; do not guess a replacement URL without basis.
When the format is broken or a legend overflows, fix the source and regenerate affected pages, and verify visuals again before delivery.
Recovery starts from the last editable source, version and fact table, not from rewriting the whole document from a compressed summary.

## Resources and examples

Mechanical fact/link spot checks may use low/low; body structure starts at normal/medium; complex contract explanations use normal/high; grade words map to actual execution configuration through the project resource mapping.
Split read-only verification or independent drafts only when the host allows and sections are independent; the formal file is still integrated by one writer.
Short edits need no added agents or full-document restructuring for the sake of the package workflow.

Normal example: a tutorial gives a synthetic project, clear prerequisites, steps and a final visible result, and on failure explains how to return to a resumable state.
Misuse example: a parameter reference opens with a page of product vision but no types, defaults or limits; turn it into a searchable specification.
Conflict example: an old document says a field is required while the current contract makes it optional; after verifying the applicable version, update body and examples together rather than just one place.

## Sources

1. Pinned source: [GH01 documentation-writer](https://github.com/github/awesome-copilot/blob/7cce7cfb4b61196c36d7e8eb8475ae84b356b126/skills/documentation-writer/SKILL.md).
2. Adopted the four Diátaxis reader purposes and structure-before-prose; fact tracing, version conflicts, synthetic examples, format checks and preserving entry points are own-authored for this package.
   Dropped re-asking for already known inputs every time, separate outline approval for every document, and a blanket ban on public fact-checking. Project facts and fixed layouts come from the project documentation conventions.
3. License: shipped with the package as [LICENSE-GH.txt](LICENSE-GH.txt) (GH, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license file along when copying this package alone.
