# Dependency simulation contract

Filled in by the person responsible for implementation/testing, recording the actual public version and allowed boundaries.

- Task, caller version, protocol version and source of independent expectations: {{identity}}
- Chosen stub and rationale, real client/SDK boundary: {{choice}}
- Synthetic data, seed/clock, scenario naming and state reset: {{fixtures}}
- Local endpoint, verification that forwarding/default identity/proxy are disabled: {{network_evidence}}

| Operation/failure | Request matching | Response and side effect/state | Independent expectation | Actual result/evidence | Unsimulated difference |
| --- | --- | --- | --- | --- | --- |
| {{operation}} | {{contract}} | {{transition}} | {{oracle}} | {{result_or_not_run}} | {{gap}} |

- Two-node isolation, unknown-request rejection, duplicates and recovery: {{observations}}
- Fixture/adapter candidate identity, execution entry point and remaining in-flight work after finishing: {{repro}}
- Coverage by static/reasoning/local protocol/real external evidence separately: {{levels}}
- Failure preservation and cleanup scope: {{retention}}
