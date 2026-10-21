# Evidence point patterns

All names, fields and values below are synthetic examples or project inputs.
Choose only the relevant pattern and complete every field from [Step format](step-format.md) in the [round template](../assets/evidence-step.md).
These are alternatives, not a five-step round; hand over only 1–3 steps after confirming environment, platform, identity and permissions.
All variable values belong in the round's first block; combine the selected pattern's settings there.
Use existing installed tools and privately configured sessions only; missing access -> the stated alternative, without new authentication or installation.
Confirm command semantics and bounded safe source fields before use, including any implicit hooks or wrappers.
Normal/abnormal examples here are illustrative observations, never text to put in command blocks.

## HTTP response or browser Network

Location: the user's confirmed browser page and existing session, or their machine with an already configured HTTP client.
Action/read-only rationale: inspect an existing response to an approved read endpoint; verify that the endpoint has no side effects.

1. Open Developer Tools -> Network -> Fetch/XHR on the confirmed page; select the existing request named `{{request_name}}` at `{{request_time}}`.
2. Open Headers -> General; record status, method and safe request identity without copying request headers or query secrets.
3. Open Response/Preview -> `{{status_field}}`, `{{error_category_field}}`, `{{correlation_field}}`; copy only those fields.
4. If a cURL reproduction is needed, use Copy -> Copy as cURL locally as a draft only.
   Remove Cookie/Authorization headers, embedded credentials, secret query parameters, payloads and unneeded headers before sharing anything.
   Do not run a copied write request or paste a HAR; do not repeat an action that changes state to obtain a response.

A bounded unauthenticated read or an already locally configured client can instead use this form.
The URL must select an already verified small, safe response; do not fetch a broad response then filter away secrets.

```sh
export READ_URL='{{approved_read_url_without_secrets}}' TIMEOUT='{{seconds}}' BYTE_LIMIT='{{max_bytes}}'
```

```sh
curl --disable --silent --show-error --fail --max-time "$TIMEOUT" --max-filesize "$BYTE_LIMIT" --url "$READ_URL"
```

This form sends no Cookie/Authorization; if identity is required, use the existing browser session or an existing user configuration reviewed locally for read-only semantics.
Never ask the user for the configuration contents, and never add credential literals to the command.
Normal example: `state=ready, error_category=none`; abnormal example: `state=rejected, error_category=dependency_unavailable`.
Paste only status, safe correlation and the selected fields with execution time/time zone/environment.
Redact identity/personal data and any secret fields before paste; inspect the final excerpt locally.
Budget: one existing response or one GET, a specified timeout and byte cap, and explicit selected-field length caps.
Check that the installed client enforces the cap for the response type; otherwise use a bounded field interface or the browser excerpt.
Unavailable -> use a bounded correlated log window, or ask the endpoint owner for these same fields.

## Container logs

Location: the user's confirmed host/Docker endpoint or cluster context and namespace.
Action/read-only rationale: read a bounded existing log slice, without follow, exec, restart, context switching or configuration changes.
Use this only if the selected log source has a known safe schema; an uncontrollable body -> seek a structured safe-field interface or owner-supplied excerpt.
The redaction pipeline in Step format is an extra local precaution on already bounded text, not permission for a secret dump.
The commands below invoke an already installed Bash, so the outer shell can be Bash or zsh without changing its options.
If Bash is unavailable, choose the browser or owner-provided excerpt instead of installing it.

Docker variant:

```sh
export CONTAINER='{{container}}' SINCE='{{window_start_with_timezone}}' UNTIL='{{window_end_with_timezone}}' TAIL_LINES='{{source_lines}}' MATCH='{{safe_correlation}}' MATCH_LINES='{{matched_lines}}' BYTE_LIMIT='{{max_bytes}}'
```

```sh
bash -o pipefail -c '
docker logs --since "$SINCE" --until "$UNTIL" --tail "$TAIL_LINES" "$CONTAINER" 2>&1 | grep -F -m "$MATCH_LINES" -- "$MATCH" | head -c "$BYTE_LIMIT"
probe_codes=("${PIPESTATUS[@]}")
probe_exit=$(( probe_codes[0] != 0 || probe_codes[1] != 0 || probe_codes[2] != 0 ))
printf "\nproducer_exit=%s filter_exit=%s cap_exit=%s command_exit=%s\n" "${probe_codes[0]}" "${probe_codes[1]}" "${probe_codes[2]}" "$probe_exit" >&2
exit "$probe_exit"
'
```

Cluster variant: first ask the user to confirm the current context against their environment record; do not infer it from a workload name.
Pass the confirmed context explicitly; do not issue `use-context`.

```sh
export CONTEXT='{{confirmed_current_context}}' NAMESPACE='{{namespace}}' WORKLOAD='{{deployment_name}}' CONTAINER='{{container}}' SINCE='{{duration}}' TAIL_LINES='{{source_lines}}' MATCH='{{safe_correlation}}' MATCH_LINES='{{matched_lines}}' BYTE_LIMIT='{{max_bytes}}' TIMEOUT='{{request_timeout}}'
```

```sh
bash -o pipefail -c '
kubectl --context "$CONTEXT" --namespace "$NAMESPACE" --request-timeout "$TIMEOUT" logs "deploy/$WORKLOAD" --container "$CONTAINER" --since="$SINCE" --tail="$TAIL_LINES" --timestamps=true | grep -F -m "$MATCH_LINES" -- "$MATCH" | head -c "$BYTE_LIMIT"
probe_codes=("${PIPESTATUS[@]}")
probe_exit=$(( probe_codes[0] != 0 || probe_codes[1] != 0 || probe_codes[2] != 0 ))
printf "\nproducer_exit=%s filter_exit=%s cap_exit=%s command_exit=%s\n" "${probe_codes[0]}" "${probe_codes[1]}" "${probe_codes[2]}" "$probe_exit" >&2
exit "$probe_exit"
'
```

Each block is one Bash invocation that immediately captures every pipeline stage's status and prints it without requiring a second user command.
It exits 0 only when all stages succeed, otherwise 1; the printed stage codes preserve the actual producer, filter and byte-cap results.
Producer failure differs from grep exit 1 (no match); intentional truncation can also cause an upstream broken-pipe status, so report it as partial evidence, not a root cause.
If status capture is unavailable, return that limitation as `unverified`; a final `head` exit 0 does not show a successful log read.
Normal example: correlated `accepted` then `completed`; abnormal example: correlated `dependency_timeout` without a completion in the selected window.
Paste time, level, error category, safe correlation and the printed stage and command exit codes.
Redact message bodies, tokens, personal data and private identifiers locally.
Budget: explicit since/until where supported, source tail lines, matched lines, total bytes and per-field lengths; one query without streaming.
Reserve 96 bytes of the step's total output budget for the fixed status line, in addition to the BYTE_LIMIT cap on the evidence body.
The cluster CLI timeout bounds the request; use a trusted existing outer timeout for a Docker client that may hang, or choose another point.
No matches means only "not observed in this slice"; tail/byte truncation and sampling may hide an event.
Unavailable -> browser response or build console excerpt; if cluster access is absent, ask the workload owner for minimal fields rather than borrowing an account.

## Database row

Location: the user's database client with an existing read-only service/account for the confirmed database.
Do not use a write account for convenience, print connection strings or request credentials.
Action/read-only rationale: one SELECT of explicit safe columns for a primary key with LIMIT; no locks, exports, stored functions or procedures.
Check that the named table is an ordinary table, not a view with unreviewed functions or policies.
The following PostgreSQL example assumes synthetic columns `id`, `state`, `error_category` whose lengths are already known to be bounded.
Adapt identifiers to reviewed project columns before handover; if field lengths are unknown, stop and ask the schema owner for a bounded alternative.

```sh
export DB_SERVICE='{{existing_readonly_service_name}}' RECORD_ID='{{record_primary_key}}' PGOPTIONS='-c default_transaction_read_only=on -c statement_timeout=5000' PGCONNECT_TIMEOUT='5'
```

```sh
psql --no-psqlrc --dbname="service=$DB_SERVICE" --set=ON_ERROR_STOP=1 --set=record_id="$RECORD_ID" --tuples-only --no-align <<'SQL'
SELECT id, state, error_category FROM task_runs WHERE id = :'record_id' LIMIT 1;
SQL
```

The quoted psql variable is a SQL literal, not executable SQL from a pasted value; validate the key's expected type first.
Keep the read-only service in existing local configuration; do not display it.
Normal example: one row `42|ready|none`; abnormal example: `42|blocked|dependency_timeout`; zero rows leaves identity/retention hypotheses open.
Paste only the selected safe columns and time/time zone/environment; redact personal keys and any sensitive category text.
Budget: one primary-key query, one row, bounded column lengths and a stated total byte cap; connection/statement timeout 5 seconds in this example.
Verify those column lengths fit the byte cap before executing; LIMIT alone does not bound a large text column.
Unavailable -> request the same safe fields from the API or database owner, or use correlated logs; do not switch to a write identity.

## Build console

Location: the user's existing build-system browser session and exact build page, with job/build identity and time confirmed.
Action/read-only rationale: view the existing console, without rebuild, retry, replay, approval or parameter changes.
For example, a Jenkins build exposes a Console Output page and a `{{build_url}}/consoleText` raw-text address.
That address is a locator, not permission to download a whole console or attach authentication headers to a shared command.

1. Open the confirmed job -> build `{{build_number}}` -> Console Output (or the system's equivalent panel).
2. Use the viewer's bounded section/search around `{{stage_name}}` and `{{safe_correlation}}` within `{{time_window}}`.
3. Select only timestamp, stage, result and error category; keep the build identity, without pasting credentials or the full console.

Normal example: stage `package` finished with result `success`; abnormal example: stage `package` ended with category `missing_input`.
Paste those fields with execution time/time zone/environment; redact shell arguments, secret bindings, personal data and private URLs.
Budget: one build, one stage/time slice, specified line/byte/field limits and a viewer timeout; no "download all logs".
If the viewer cannot bound the read safely, request an owner-provided minimal excerpt instead of fetching consoleText wholesale.
Unavailable -> build status API with safe bounded fields or the build owner; a missing console does not prove a build never ran.

## Cloud resource status

Location: the user's existing cloud CLI session/profile and confirmed account scope, region and resource identity, kept private locally.
Action/read-only rationale: a reviewed show/list operation with explicit scope and safe selected fields; check wrappers and authentication hooks first.
Do not use subcommands that refresh authentication, modify state, fetch credentials or expose secret configuration.
If an expired session would require refresh, stop this step and use another observation point.

Azure example, only when the installed command is a read-only resource lookup under the existing session:

```sh
export RESOURCE_ID='{{confirmed_resource_id}}' QUERY='{state:properties.provisioningState}' BYTE_LIMIT='{{max_bytes}}'
```

```sh
az resource show --ids "$RESOURCE_ID" --query "$QUERY" --output json --only-show-errors | head -c "$BYTE_LIMIT"
```

Choose the analogous installed AWS or Google Cloud read command only after confirming its semantics, selected fields and bounded account/resource scope.
Do not run discovery lists across an entire account to find the target.
Query/output selection limits returned display fields, but may not limit what the service sends to the client; verify that underlying data is also permitted.
Normal example: `state=Succeeded`; abnormal example: `state=Failed`; neither by itself establishes the application-level cause or recovery.
Paste only selected state and observation time/time zone/environment; redact resource/account identifiers and any returned secret or personal data.
Budget: one resource, one request, stated client timeout, bytes and field lengths; use only a trusted existing timeout mechanism with no authentication refresh.
If the CLI cannot enforce the required request/time/data limits, use a bounded portal status panel or an owner-provided safe field instead.
Unavailable -> existing portal status panel or the resource owner; do not change the active identity or grant a new role.
