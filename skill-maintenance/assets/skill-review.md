# Skill review record template

Written by the reviewer into task evidence, not back into the package; an author self-check is truthfully marked "author self-check".

- Object: {{package, pinned candidate version/file digest, source of criteria}}
- Role/scope: {{independent review or author self-check, allowed read/write scope, time period}}
- Verdict: {{deliverable/needs revision/check incomplete; applicable scope}}

| Check layer | Input/environment/tools | Actual action and artefact | Expected/observed | Verdict/evidence location |
| --- | --- | --- | --- | --- |
| Static format and references | {{explicit paths and parser}} | {{command actually run}} | {{actual result}} | {{result}} |
| Script normal/boundary/failure | {{synthetic input}} | {{actual execution}} | {{stable, exit codes, no side effects}} | {{result}} |
| Content walkthrough | {{scenario and method}} | {{read-only analysis}} | {{branches, failure recovery}} | {{not a host test}} |
| Actual trigger/behaviour | {{host version, configuration, candidate}} | {{trace and output}} | {{normal and adjacent negative cases}} | {{write unverified if not run}} |
| Composition/cross-project/upgrade | {{dependencies and consumers}} | {{actual verification}} | {{permissions, parameters, version, recovery}} | {{verified scope}} |

| Finding | Trigger condition and impact | Evidence | Minimal suggestion | Blocking/non-blocking/unverified |
| --- | --- | --- | --- | --- |
| {{number}} | {{concrete behaviour}} | {{location}} | {{suggestion; not fixed on the author's behalf}} | {{category}} |

- Source licensing and distributability: {{pinned sources, required notices, whether kept in the package}}
- Unverified and why: {{missing tools/authorisation/environment; which conclusion cannot be given as a result}}
- Comparison validity: {{baseline, whether evaluators took part in authoring, sample size, bias, actually available usage}}
- Re-verification scope after revision: {{scenarios needing a new candidate and rerun; basis for reusing old evidence}}
