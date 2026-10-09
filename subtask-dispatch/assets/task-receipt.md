# Subtask receipt
Status: {{done / aborted / pending (choose one; distinguish author completion from acceptance result)}}
Task: {{logical ID, artefact path, corresponding approval identity}}
Summary: {{result and key points still to handle; length per project contract}}
Scope: {{actually read/written this run and untouched boundaries}}
File classes: {{actual change counts by project classification; example: body / reference / template, replace per project contract}}
Execution: {{period, real execution handle, known model/reasoning or unverified}}
Sources: {{external material or originals actually used and section ranges; write "none" if none}}
Verification: {{checks done, evidence location; checks not done explicitly marked unverified}}
In-flight: {{whether all related executions terminated, stop evidence or unknown}}
Stop-writing: {{stopped and handed to whom / not yet stopped and why}}
Locators: {{section names and line numbers/anchors of key results, verification and unfinished items; content identifier in the external index}}

## Results and evidence

Per acceptance item write expected, actual, evidence and coverage limits. Attach the change list and impact; do not substitute exit codes for business assertions.

## Deviations and unfinished work

List gaps, impact, current writer, actions that may continue, recovery conditions; state explicitly when there are no gaps.

## Finalisation check

Locators correspond to the final file; the identifier is computed by an external index or another file; do not require the receipt to contain its own full hash. The main task reads the header first, then verifies evidence by section; after a file change, old identifiers and old reviews must be re-judged for applicability.

The fixed header field count may grow or shrink per project contract; reductions must keep identity, scope, result and evidence location. The completion message carries only the receipt path, status, a one-sentence conclusion and the number of pending decisions. Line, byte and summary limits come from project configuration; the receipt is not the user workbench and does not write the overall status.
