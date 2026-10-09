# Vue test plan and evidence

Behaviour/source: {{input -> action -> output; rejections and boundaries}}.
Candidate and capability: {{Vue/VTU/Vitest/Pinia/DOM/plugin versions, existing commands; write unknown when not provided}}.
Test boundary: {{component/store/composable, mount scope, observation surface and reason for the choice}}.
Stub contract: {{real/stubbed actions, service returns, plugins/providers, external parts that cannot be proven}}.

| Scenario | Independent expectation | Data/time control | Actual result and evidence |
| --- | --- | --- | --- |
| Normal/error/empty/permission | {{choose by goal}} | {{fixtures/timezone}} | {{first run/re-verification/unverified}} |
| Race/unmount/re-entry | {{late result and cleanup}} | {{deferred/timer/scope}} | {{result}} |

Resources and cleanup: {{this case's Pinia, wrapper, Teleport, listeners and owner; record cleanup failures separately}}.
Browser/API-layer gaps: {{what jsdom or stubs cannot prove, and the corresponding next layer}}.
Failure recovery/in-flight: {{first failure, candidate changes, still-valid results, leftovers and next step}}.
