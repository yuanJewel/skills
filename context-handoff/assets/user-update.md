<!-- This file is the only template for the human-facing current workbench, for the project's chosen user page or the current reply.
When generating, delete this note, the examples and every heading that does not apply; keep only what the user needs to see now.
Do not hand the user an abbreviated internal status table; results first, then the real required action.
Update the project's existing user page when there is one; tasks needing no persistent user page deliver in the reply, adding no file for the template's sake.
The full decision basis must not be cut for brevity, and the user must not be asked to assemble a conclusion across several files. -->

# {{work name}}

{{State first the results obtained, actual coverage and gaps affecting the user's goal, using names the user understands.}}

<!-- Choose one action sentence by situation; never ask "approve?/continue?" out of nowhere:
No pending decision/acceptance/manual action -> "No action needed from you now; I will continue {{authorised next step}}."
All current work complete -> "{{Result}} is complete; no action needed from you now."
A real action exists -> "You now need to {{one clear decision or action}}, because {{what is affected without it}}." -->
{{action sentence}}

<!-- Keep the next section only when a current decision is pending; several truly independent items may be listed side by side; never re-request approval for already authorised actions. -->

## Your decision needed: {{item described in the user's language}}

{{Recommended option and reasons; list real alternatives and trade-offs; explain why existing authorisation is insufficient to make this decision for the user.}}

| Decision basis | Current specifics |
| --- | --- |
| What is done this time | {{clear scope, target result and necessary boundaries; how far existing authorisation covers}} |
| Why now | {{verified facts, what changed and the impact on the user's goal; unverified assumptions listed separately}} |
| Which files/artefacts change | {{concrete reviewable files/UI/deliverables and the changes; related affected items too, not just a file count}} |
| Verification and failure handling | {{key acceptance, verification done, evidence still missing, where recovery goes after failure}} |
| Time and resources | {{the user's waiting range, the parts of accumulated effort/resources or cost that affect the decision, prerequisites; unknowns stated explicitly}} |
| What your choice changes | {{outcomes of different choices, impact of deferral and the real actions the user must take}} |

{{The exact choice to make or single step to perform; evidence links allow deeper checking, but key decision information is shown in full on this page.}}

<!-- Keep the corresponding section only when user acceptance or a manual action is really needed now; accepted items no longer keep a pending column. -->

## {{Result awaiting acceptance / Action you need to complete}}

{{Directly viewable result entry, the actual pass criteria, verified coverage and limits; or the exact manual action, object and observable result after completion.}}
{{Request only actions agreed in the original task or actually necessary; do not escalate author self-checks into mandatory user acceptance.}}

<!-- Keep only when another session must continue now; takeover does not require the user to carry hashes, version lists or internal status tables.
The copyable sentence locates; the successor reads approvals, results, write permission and in-flight work itself; the sentence neither means the old execution stopped nor grants extra actions. -->

## Continue this work

Paste into the target session:

> Continue {{project/work name}}, {{plan or stable task ID, phase}}. Recover current approvals, results, write permission and in-flight work from {{single status entry}} and continue the authorised next step.

<!-- Pre-publish check:
1. Can the user understand the result and whether action is needed on the first screen? If no action, is that stated explicitly?
2. Is each real decision complete in scope, reasons, concrete file impact and budget, rather than hidden behind several links?
3. Do internal task numbers, hashes, resource ledgers, source checks or tool operation steps really affect the user's decision? If not, leave them in status/evidence.
4. Are confirmed items first written to the formal decision location, then removed from the current page? Without new facts, keep no confirmation history, empty headings or "none" tables.
5. Does the continuation sentence appear only when needed, using stable identity to avoid same-name mix-ups? -->

<!-- Examples (do not copy into the user page):
No pending decision: The export format is fixed; all three samples open normally. Old-format compatibility is still being verified. No action needed from you now; I will continue the compatibility check.
Real decision: Two export options have been compared. You now need to choose whether to keep the old format, because disabling it affects colleagues still on the old client.
The latter must fully fill concrete files/artefacts, compatibility scope, time/resources and consequences; never just "see link for options, please approve".
Misuse: "Changed several files today, verified several hashes, nothing pending but please confirm to continue" — that is an internal ledger and manufactures a new approval. -->
