# Role contract and continuation decisions

Read only the relevant section for an unfamiliar contract, role ambiguity, permission conflict or a named earlier session. What follows is the meaning required, not a demand that the project add YAML, a registry or directories; existing entries, role bodies, tasks and status files may each carry it.

## 1. Is the contract sufficient

| Content | Used to decide |
| --- | --- |
| Role ID, display name, aliases and applicable hosts | Separate stable identity from titles; a multi-role index locates the body with them. A single default role may omit a named role and aliases. |
| Responsibilities and non-responsibilities | Whether the request falls under this role; avoid gaining project-wide operation rights by being called "owner". |
| Inputs, processing steps and deliverables | Which material to read now, what work to do and where results actually go; the body should guide action, not merely describe a title. |
| Writable scope and items that cannot be self-signed | Checked together with this approval, ownership and the sole writer; a contract's allowed scope is not the current file write seat and does not replace independent review or human decision. |
| End and takeover conditions | When a phase is delivered, what must be preserved, when the writer may be transferred; the end of one response is not the end of the work. |

The current task separately supplies goal, mode, plan/phase/stable task identity, acceptance and approval source; do not copy them into the long-term role definition. A short consultation needs only enough goal and boundary to answer. Current state separately supplies session handle, results, open items, in-flight work and resource occupancy; role ID, task ID and host session handle cannot substitute for one another.

When a contract lacks a field, judge the impact first: no alias does not prevent matching by ID; no long-term registration location does not prevent confirming the role in the reply; missing writable scope or approval evidence means no file is written on that basis. When an existing task already states these conditions, consume the task directly; do not demand a role contract for form's sake.

## 2. Matching, conflicts and a single confirmation

**Match order.** Within the chosen project look up the stable ID first, then display name and registered aliases; when the body for an exact ID is missing mark "contract missing" rather than degrading to a similar name. When different entries share a display name/alias keep the candidates and narrow by the host, responsibility and task the user already gave; only ask the user to choose when still not unique. When ID or host differs between body and index, pause actions that depend on that identity; do not silently fix the index. When the named role does not support the current host, state the limit; do not switch host or impersonate another role.

**Single default role.** Use it when the current entry clearly names exactly one default contract and the user has not named a conflicting role; task modes (for example design/review/implementation, replace per project contract) are not roles that must be registered separately. When the default role only means maintaining a class of files, do not expand it into permanent write access to the whole workspace. When the user explicitly gives an unknown role name, do not let the default role mask that new request; take the unknown-role branch.

**Unknown role.** Judge "unknown" only after checking the current role index or default contract; do not search the whole workspace to guess an identity. Ask once, in one message, for whatever is still missing among "new role or alias of an existing one, what it is responsible for, this run only or kept long-term"; do not re-ask responsibilities or retention decisions the user already gave. When the answer is partial, keep the gap, pause only the actions that depend on it, and do not resend the same question set; a new substantive contradiction may be raised separately. Without persistent-retention confirmation do not change the long-term registry; when the user says this run only, adopt a temporary role still bound by existing authorisation and output scope. When retention is requested, still verify the approved writer of the role definition file; do not register on another author's behalf.

**Several roles.** One instruction may explicitly ask for two responsibilities at once; this differs from one name matching several candidates. For the former, check task and scope per responsibility; when a rule says an implementer cannot independently review their own output, keep the separation and name the affected deliverables rather than bypassing it through dual roles. For the latter, confirm only the specific target; never claim all candidates by default.

**Conflict layering.** The current user instruction and applicable higher constraints decide authorisation; verified formal approval defines this run's scope; the current contract supplies responsibility and ownership; history and inference are clues only. A newer file date or stronger wording does not override an effective decision. When actual files, execution and status disagree, report observable facts and unverified parts, verify the minimum necessary evidence, and never edit the approval original to fit the current state.

When only the role table claims write access while status shows another writer, keep the existing effective write seat; do not create a second one. When two status files both claim authority, verify approval and actual in-flight work first; do not pick a winner by name or last-modified time. Pause only the conflicting files and dependent work; other authorised read-only or non-conflicting tasks continue. Choosing a role adds no business, Git, cross-project, messaging or tool execution permission; an existing explicit authorisation of the same scope is not re-requested because the role changed.

<a id="takeover"></a>

## 3. Taking over a named earlier session

### Locate and recover

1. Start with the stable session/task handle the user gave, or the specific project, role and phase, and look up the current index and status. With only a title, locate using the scope already given; with several candidates list the distinguishing project, phase, identity and known state and ask only for the specific target.
   - No index or no result -> query the available host session list or existing continuation records by the given project/title/role, expanding only relevant candidates; recover directly when unique, confirm when still several.
   - Capability and evidence both insufficient -> state the range searched and ask for minimal locating information; do not take over a similar task, do not sweep the whole account's chat bodies.
2. Once the candidate is fixed, read its checkpoint and approval entry first, then the result sections the open items directly depend on; when a history-reading tool exists, read only the records needed to cover the gap. The old role description helps find the task but grants no historical account, private approval or full directory permission.
3. The recovery list contains only: task/phase and approved version; whether result locations and current content match; done/not done; current writer; actual handles and liveness evidence of the old session, subtasks and tool/command executions; in-flight occupancy and accumulated usage so far; next step and takeover source. Reuse the existing status; do not copy the full plan or add a default handover file. Mark unknown usage as unknown; a session change does not reset it to zero.

### Actions under incomplete evidence

| Scene | What may continue | What it does not justify |
| --- | --- | --- |
| History tool absent, checkpoint and results present | Recover the verified scope from on-disk approval and current results, noting insufficient history coverage | Claiming to have read the original chat, or treating suggestions in a summary as approval |
| No checkpoint, but clear approval and verifiable results | Read-only consolidation of existing evidence and concrete gaps; authorised work not dependent on old state may continue | Presuming all open items, that the writer has stopped, or that old operations failed |
| Result content differs from the old receipt | Verify current files and available content identity; mark affected conclusions for re-check | Overwriting current content with an old "passed", or overwriting others' changes to restore an old candidate |
| Old session unreachable, task response ended or execution state unknown | Read-only recovery; record in-flight work as pending verification, keep occupancy; continue non-conflicting work within resources | Releasing occupancy, seizing writes, retrying operations that may still run |
| Old execution still running, no stop authorisation or control unavailable | Preserve evidence, report the conflicting write seat; continue non-conflicting work | Unauthorised stop, write seizure, duplicate execution, or waking/messaging along the way |
| Stop authorised for the same scope and precise control available | Request stop of the named old execution, verify the final state of parent session, subtasks and related tools; transfer authority per approval once all have stopped | Treating acknowledgement, parent-session stop or partial success as a full stop; after failure/timeout keep the unknown occupancy |
| Old writer and related in-flight work stopped, takeover scope explicit | Register the write transfer at the approved status location per project rules, then verify files and approval before continuing | Exceeding the named task, widening scope or inheriting historical special approvals |

Stop evidence may come from a trusted host's current execution final state, a handover in which the executor explicitly stops writing and lists all in-flight work, or an on-site record with the same coverage; merely seeing "done", a process list without a certain name, or a long silence is not enough. When evidence covering old subtasks/tools cannot be obtained, keep them unknown. The user stating directly that something has stopped is usable input; still check which writers and operations it covers and do not generalise to unmentioned executions.

Role bootstrap only completes the identity and continuation check; ongoing checkpoint maintenance follows the project's existing practice. Recovery per this page works without other skills; do not install tools to add features, auto-message across sessions or start new background listeners.

## 4. Registration and re-entry

Deduplicate by real workspace identity, stable task and current session association, never by role display name alone. When symlinks point to the same real package or the same workspace entry, do not create a new identity either. The role registry records long-term role definitions; session registration records this instance; file status records the current write seat. The three may share one file but their semantics must stay separate.

On a repeated call in the same session: reuse the role body if unchanged, but before every write or resumed execution read the minimal current writer, takeover and in-flight state. When the old session finds that responsibility has effectively transferred, stop new writes/executions to that file, preserve undelivered results, and report the delta at the approved record location; do not switch the writer back or blindly re-run. Handle own in-flight work according to real permission and control capability; with unknown responsibility stay read-only first. When task, role, version or writer changes, read the corresponding delta; when responsibility is unchanged reuse the current registration without adding duplicate entries. When the host handle is missing use the verified session association; if it is still unclear whether an instance exists, do not create a second record, verify the association first and keep non-conflicting work going. A takeover session keeps the old identity and the handover source; it does not impersonate the old session or rewrite historical attribution.
