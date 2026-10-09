# Pipeline evidence

- Approved scope/source identity: {{job templates, macros, scripts, artefact/parameter snapshot}}
- Local admission: {{server/test job prefix/agent node/workspace/cleanup responsibility}}
- Tool matrix: {{JJB/Jenkins/Java/plugin versions and actual evidence}}

| Source -> artefact | Expected | Actual check | Result/evidence | Unverified |
| --- | --- | --- | --- | --- |
| YAML -> XML | {{job count, parameters, script/SCM}} | {{command/exit code}} | {{hash and diff}} | {{scope}} |
| Pipeline -> steps | {{stage dependencies/CPS}} | {{linter/unit/local run kept separate}} | {{result}} | {{plugins/agent nodes}} |

- String boundaries: {{each interpretation layer, synthetic special characters and fake-secret leak checks}}
- Identity chain: {{operation -> job -> queue -> build; query evidence when the result was unknown}}
- State tests: {{queued/running/cancelled/final state; duplicate/out-of-order/restart/missing callback}}
- Isolation: {{resource scope of each approved agent node and evidence of no cross-contamination}}
- Cleanup/in-flight: {{own resources only; executions not yet stopped}}
- Conclusion: {{real local execution, offline rendering, static reasoning kept separate; manual items such as real triggering/traffic switching}}
