# pytest test evidence

Target contract/candidate: {{behaviour and source, code/generated artefact identity}}.
Capability: {{Python/pytest/plugin versions, async mode/loop scope, whether xdist is present, actual command}}.
Selected set: {{nodeid/parameter IDs/markers, exclusions and reasons}}.
Fixtures and stubs: {{scope, owner, real/mock boundary, release path when preparation fails}}.

| Scenario | Independent expectation | worker/attempt/data | setup/call/teardown | Evidence |
| --- | --- | --- | --- | --- |
| {{normal/error/boundary}} | {{input -> result}} | {{identity}} | {{actual result of each phase}} | {{original/re-verification}} |

Counts: {{passed, failed, error, skip, xfail, xpass, not run; state explicitly when no tests were collected}}.
Cancellation/timeout/cleanup: {{task awaiting, resource release, failures and what is still in flight}}.
Limits and recovery: {{missing plugins/unverified real dependencies, valid results, follow-up responsibility}}.
