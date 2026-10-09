# Candidate review receipt

- Task, reviewer and author relationship: {{independent review/author self-review; source of responsibility}}
- Candidate root and scope basis: {{approved object, scope list; explicit scope only}}
- Start/end identity: {{before / after manifest location and candidate_sha256}}
- Stability: {{same/changed/could not stabilise; an empty scope must not pass}}
- Specification and standards inputs: {{version, provenance; missing items and impact}}
- Included/excluded: {{added, modified, deleted, generation inputs/outputs, uncommitted/WIP; per-item exclusion reason}}

| Axis | Requirement or rule | Implementation location | Evidence and kind | Conclusion/gap |
| --- | --- | --- | --- | --- |
| Specification | {{requirement}} | {{file_and_line}} | {{actual run/static reasoning/unverified}} | {{result}} |
| Standards and correctness | {{rule or invariant}} | {{file_and_line}} | {{evidence}} | {{result}} |

## Confirmable issues

- {{id/severity/confidence}}: {{title}}
- Location: {{candidate file, line, old/new side}}
- Trigger, expected, actual and impact: {{minimal input sufficient to reproduce, without secrets}}
- Evidence: {{actual command, exit code and output location; or static causal chain}}
- Minimal fix: {{suggestion; do not expand scope automatically}}

## Suggestions and unverified

{{Keep smells/preferences separate from defects; mark missing specification, old baseline, consumers, generation reproduction or real environment individually.}}

## Conclusion

{{Separate conclusion per axis; when the candidate changed, list invalidated items and re-review scope; finding no issue does not prove absence of defects. Next step and the minimal material a successor needs.}}
