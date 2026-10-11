# Security review result

- Candidate: `{{scope}}`, `{{content_identifier}}`, `{{identical_before_and_after}}`.
- Original requirements and constraints: `{{security_contract}}`, `{{identity_and_data_classification}}`, `{{permitted_environments}}`.
- Evidence type: `{{evidence_types}}` (source analysis / synthetic run / authorised observation); tools and versions: `{{tools_and_versions}}`; unverified: `{{unverified_items}}`.
- Conclusion: `{{conclusion}}` (no substantive findings / issues to fix / key evidence insufficient); limited to this review's coverage.

## Boundaries and outputs

| Input and controlling principal | Authentication/authorisation and authoritative layer | Operation or output | Verified basis / unverified premises |
| --- | --- | --- | --- |
| `{{entry_point}}` | `{{contract_and_source_location}}` | `{{operation_or_output}}` | `{{verified_basis_or_unverified_premise}}` |

## Findings

For each item give: stable ID, exact file/line or interface, controllable input and preconditions, missing constraint, actual impact,
evidence strength, risk level and basis, minimal fix suggestion, and a synthetic verification that could refute the risk.
For a suspected secret record only location and category, never the value. General style suggestions are not security blockers.

## Verification and handover

List each check performed and its actual result; anything not done cannot be filled in as pass.
Record which evidence a candidate change invalidates, residual risk, facts still to be supplied, fix ownership and re-verification scope.
This report does not authorise changing code, altering live policy, reading credentials or releasing.
