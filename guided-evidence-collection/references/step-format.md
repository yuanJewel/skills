# Format a user-run evidence step

The agent fills the [round template](../assets/evidence-step.md); the user supplies private configuration locally and returns only safe fields.
Resolve missing execution environment before producing commands.
Each round has hypotheses, outcome-to-hypothesis predictions and 1–3 ordered steps.

## Fixed step fields

Use these same fields in every step, including click-only steps:

| Field | What to supply |
| --- | --- |
| Step ID | A stable round/step identifier for the report's `user-run` evidence. |
| Execution location | Machine, cluster context/namespace or browser page, with target identity and existing access confirmed by the user. |
| Action and read-only rationale | Exact observation and why its actual semantics do not change state. |
| Command or click path | One command per block, or a numbered path naming panel, request and fields. |
| Expected normal output | One synthetic example, outside command blocks. |
| Expected abnormal output | One synthetic example and which hypothesis it supports, outside command blocks. |
| Fields to paste | Minimal fields plus execution time/time zone and environment; never an entire response by default. |
| Redact before pasting | Credentials, authentication headers, personal data and project-sensitive identifiers; inspect locally. |
| Output budget | Time window, lines/rows, total bytes, field lengths, request count and timeout/sampling limit. |
| Alternative if unavailable | A permitted observation point or owner to ask for minimal fields; no permission escalation. |

Missing results use the `unverified` label from `guided-evidence-collection`; a failed query is not evidence that no error exists.
If any limit is exceeded, stop or truncate and report the missing range; do not claim completeness.

## Commands and variables

- One fenced block contains one command, without a shell prompt, pasted output or an interactive editor.
- Gather all variable values in the first block of the round, for example one `export A='{{a}}' B='{{b}}'` command.
  Later blocks reference only those variables; do not scatter replacement values across steps.
- Fill placeholders before execution, check quoting for the actual shell and validate identifier/number inputs.
  Do not interpolate untrusted paste text into shell or SQL code.
- Secret values are never literal placeholders for the agent to fill; use existing user configuration or privately set, non-echoed variables.
  Avoid shell tracing, printing variables, verbose authentication output and commands that put secrets in process arguments.
- A pipeline can be one command, but inspect every stage and preserve the producer's failure status; no matches or empty output does not prove a healthy system.
  Choose an explicit byte/time cap as well as row or line caps; filtering alone does not bound the source read.

Prefer tools already available: curl, kubectl, docker, a database CLI or a cloud CLI's show/list.
Do not install a tool to make a step executable.
If using an optional tool such as jq, give an equivalent without it and offer only the applicable alternative in the round.
Only give both macOS/Linux shell and Windows PowerShell when needed by the user's actual platform.
For PowerShell, collect settings in one first-block command such as `Set-Item -Path Env:TARGET -Value '{{target}}'`; use `$env:TARGET` later.
For multiple settings, use one mapping piped to `ForEach-Object`/`Set-Item`, with values in that first block only.
Choose platform-native filtering and failure-status checks; do not assume a POSIX pipeline runs in PowerShell.

For UI-only evidence, number the click path down to panel name, request name and field names.
Do not ask the user to repeat a state-changing request merely to populate Network.

## Bounded redaction before paste

First prefer an interface selecting safe fields at source.
For already bounded text held locally by the user, this best-effort pipeline masks the entire contents of lines mentioning these fields, case-insensitively:
Authorization, Cookie, token, password, passwd, secret, api key (`api[-_]?key`), bearer or private key (`private[-_]?key`).
It uses portable extended regular expressions supported by BSD and GNU sed; no GNU-only case-insensitive flag is needed.
Set these variables with the rest of the round's variables in its first block:

```sh
export EVIDENCE_FILE='{{bounded_local_text_file}}' LINE_LIMIT='{{line_limit}}' BYTE_LIMIT='{{byte_limit}}'
```

```sh
LC_ALL=C sed -E '/[Aa][Uu][Tt][Hh][Oo][Rr][Ii][Zz][Aa][Tt][Ii][Oo][Nn]|[Cc][Oo][Oo][Kk][Ii][Ee]|[Tt][Oo][Kk][Ee][Nn]|[Pp][Aa][Ss][Ss][Ww][Oo][Rr][Dd]|[Pp][Aa][Ss][Ss][Ww][Dd]|[Ss][Ee][Cc][Rr][Ee][Tt]|[Aa][Pp][Ii][-_]?[Kk][Ee][Yy]|[Bb][Ee][Aa][Rr][Ee][Rr]|[Pp][Rr][Ii][Vv][Aa][Tt][Ee][-_]?[Kk][Ee][Yy]/s/.*/[REDACTED sensitive-field line]/' < "$EVIDENCE_FILE" | head -n "$LINE_LIMIT" | head -c "$BYTE_LIMIT"
```

This deliberately loses other fields on the same line; use another safe extraction point when that removes necessary evidence.
Redaction is best effort: it cannot recognise every secret, multiline encoding, personal field or project identifier.
The user must visually inspect the final text locally before pasting; if unsure, return only the location/type and the evidence gap.
The byte cap bounds the displayed result, not a huge input file; this pipeline is not permission to export broad logs first.
