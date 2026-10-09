# Local environment manifest

Filled in by the environment executor; write "unverified" for unknowns; do not pass template defaults off as observations.

- Task/node/sole writer: {{identity}}
- Permitted operations, root directory and local engine evidence: {{scope_endpoint}}
- Compose/engine/host architecture, explicit configuration files and digests: {{versions_files}}
- Image tag/digest/local ID, platform, whether acquisition is separately authorised: {{images}}
- Synthetic seed/fixed clock/random seed, configuration interfaces and reset conditions: {{fixtures}}
- Budget and first-node measurements: {{cpu_memory_disk_pids_ports}}

| Resource | Planned name/real path | Actual ID/ownership evidence | Shared with other nodes? | Keep or delete condition |
| --- | --- | --- | --- | --- |
| {{container/network/volume/bind/port/namespace}} | {{planned}} | {{observed}} | {{sharing}} | {{retention}} |

| Dependency | Start entry point | Readiness behaviour, timeout/deadline | Failure/recovery and observable result |
| --- | --- | --- | --- |
| {{service}} | {{argv_and_inputs}} | {{probe}} | {{recovery}} |

- Two-node isolation, resource overrun and abnormal interruption: {{evidence_or_not_run}}
- In-flight work at the end, evidence location, exact cleanup objects/entry point and remaining resources: {{closeout}}
- External capabilities not simulated or not verified: {{limitations}}
