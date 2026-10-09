<!-- This is the current-facts template, mapped onto the project's existing status structure; it does not require copying every column or creating a file.
Fill in actual values; unknown must not be shortened to zero, and "no in-flight work" needs an observation basis. Delete rows/sections that do not apply; keep unknowns that affect continuation.
Do not attach a per-round ledger; key old checkpoints, approval originals and evidence are stored and referenced per the project retention contract. -->

# {{work name}} current status

Status revision: {{project's existing revision identifier}}; updated: {{time with timezone}}
Plan/phase: {{stable plan and phase ID}}; body: {{entry and relevant sections}}
Approval: {{original entry, effective version/content identity, scope; suggestions/unapproved stated explicitly}}
Sole status writer: {{responsible identity and current host session association}}
Latest checkpoint: {{this identifier, save time, complete or concrete gaps}}

## Current results and next step

| Stable task | Current responsibility and file write scope | Proven results and result entry | Unfinished/unverified | Next step and prerequisites |
| --- | --- | --- | --- | --- |
| {{task ID/name}} | {{responsibility, current writer, exact files/scope}} | {{result; candidate content identity; check evidence and coverage}} | {{unfinished and unverified written separately}} | {{one directly executable step; which prerequisite it waits on}} |

## Accumulated usage and in-flight work

| Stable task | Host/session/execution association | Actual state and observation time | Write or side-effect scope | Grade word/execution channel and occupancy | Final-state/stop evidence or gap |
| --- | --- | --- | --- | --- | --- |
| {{task ID}} | {{parent/child relation; session and tool/command handles, not a substitute for the task ID}} | {{starting/running/recovering/stop pending verification/unknown/verified final}} | {{exact conflicting objects}} | {{requested/effective; resource pool, units; unknown marked}} | {{evidence entry, which executions it covers; unverified items}} |

Accumulated usage: {{working time, elapsed time and available tokens/cost recorded under the stable task; measured/estimated/unknown written separately, referencing existing ledgers without double counting}}
Estimate location: {{remaining expectation, headroom and calibration recorded per the `estimation` package's template, referenced only here; delete this line when none}}

<!-- With no in-flight work at all, "verified no in-flight work as of {{time}}, basis {{entry and coverage}}" may replace the table.
Business blocked, awaiting answer and submitted are not execution final states; a stop merely accepted or partially complete keeps its occupancy.
When the unit itself is unknown mark unknown; do not count as zero. Without price/usage information do not fabricate an exact amount. -->

## Checkpoint and takeover

Continuation source: {{old session/checkpoint and locating evidence; may be omitted on first execution}}
Recovery coverage: {{actual read range of original chat/on-disk material; verified facts, inference, unknown separated}}
Write transfer: {{old -> new responsibility, exact scope, authorisation entry, final-state evidence, transfer time; state "not transferred" when unmet}}
Candidate re-check: {{whether current result content identity matches the evidence; drift impact and pending checks}}
Allowed continuation scope: {{what may run now; concrete scope blocked by conflicts/missing approval/unknown executions}}
Takeover entry: {{minimal reachable path to body, approval, results and in-flight work; reference sections already linked above}}

<!-- The current status keeps no confirmation history; user decisions are saved to the formal decision location first, then this page and the user workbench are refreshed.
File hashes/version identifiers bind to result originals; do not embed this file's own hash in it.
When template fields are added, state their meaning and the degradation for old records lacking them; never parse an old missing field as "no in-flight work/authorised". -->
