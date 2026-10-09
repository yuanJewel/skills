# Examples, diagrams and delivery formats

Read this page when the document contains commands, code, diagrams or exported files.
The method decides what to check; concrete rendering tools use the dedicated capabilities listed in the host capability list or project inputs.

## Code and commands

Examples use synthetic customers, accounts, versions, domains and data; placeholder syntax must be understandable and not mistakable for real credentials.
State the applicable version, prerequisites, what the working directory means, the input and the successful output.
When a command has side effects such as writing, deleting or publishing, say so directly; verify whether it is an example or an action approved to run this time.
Do not operate real services just to check wording.

Harmless examples may be run in an authorised isolated synthetic environment, keeping command, result and version.
If not run, mark "syntax/source checked, not executed"; correct syntax highlighting does not replace a behaviour pass.
Do not remove key error handling to shorten an example, or let recovery commands destroy reader data by default.
For complex samples, prefer linking the single maintained version to prevent drift after copying.

## Diagrams and tables

Diagram nodes, arrows, hierarchy and labels correspond to facts in the body; flows have start/end, conditions and failure paths, and cross-role temporal relations may use sequence diagrams.
It must be distinguishable whether a diagram is illustrative or the implemented architecture.
Table column names, units and defaults are consistent with the body; empty / not applicable / unknown are each explained.

After export, check full pages and key diagrams: legend within bounds, arrows not clipped, fonts readable, page breaks not splitting meaning, headings not orphaned.
Do not shrink fonts indefinitely to squeeze onto one page; prefer shortening labels, adjusting layout or splitting the diagram.
If the output requires a drawn diagram, Mermaid source is not the final diagram.

## Links and Markdown

Check display text and actual target, distinguishing local files, anchors and remote links.
Being able to read the target does not mean the reader has access; when a remote is unreachable, record the check time, method and limits.
When migrating links, verify the current official target first; do not guess URLs.

Keep standard heading levels, blank lines between paragraphs, list/table boundaries, code fences and escaping.
Check long lines, Chinese punctuation, code fonts, table wrapping and page width; avoid "removing blank lines" that breaks Markdown.
Format validation only proves parsing and a subset of references; it cannot prove facts are correct, graphics do not overflow or web access permissions.

## Target formats and recovery

- Markdown/web: verify source structure, known local references, graphics required for actual display and readability; website publishing needs separate authorisation.
- DOCX/PDF: generate and render via dedicated skills, whose availability is listed in the host capability list or project inputs; if absent, keep the source and record "visual unverified".
  When rendered, check content and layout page by page; verify hyperlinks, fonts, table of contents and other parts this change touches.
- Slides: organise by presentation context, one main idea per slide; check actual rendering with the appropriate tool; do not stuff an article directly onto slides.

When export succeeds but visuals fail, return to the editable source, fix, regenerate and re-check the affected content; when the tool is absent, keep the source and mark it unrendered.
How confirmed deliverables are kept or saved separately is decided by `archive-maintenance` and the project contract; this package sets no naming or archiving scheme of its own.
Do not overwrite a confirmed deliverable to experiment with layout.
