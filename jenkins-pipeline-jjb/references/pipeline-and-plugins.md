# Pipeline and plugin layer

Build a capability table: Jenkins core/Java -> Pipeline plugins and versions -> steps/options used -> agent node tools -> shared library/SCM source.
Versions come from evidence in the approved environment, not inferred from past successes or JJB dependencies.
The Declarative validator checks declarative pipeline structure; it cannot replace verification of each plugin at runtime, script sandbox approval or agent node capability.

Each stage defines input artefacts/parameters, success preconditions, output identity, allowed side effects, timeout/retry and failure propagation.
Only immutable artefacts produced by a successful build are handed on; do not fetch "latest" from a moving branch again in the deploy stage.
Enable retry only when the operation is re-entrant/idempotent; do not use a whole-Pipeline retry that re-creates external resources.

## CPS and resumption

The official [CPS Method Mismatches](https://www.jenkins.io/doc/book/pipeline/cps-method-mismatches/) states that non-CPS methods cannot call CPS-transformed code; `@NonCPS` is not an escape hatch that makes Pipeline steps legal.
Pure computation may be isolated into non-CPS methods when needed, returning simple serialisable values.
Constructors, closures passed into non-CPS libraries and GString closure boundaries are analysed per concrete call; do not harden "a whole class must be annotated" into a general rule.

Across pause points, avoid holding non-serialisable connections, streams, Matchers or complex runtime objects; acquire, use and release them where needed.
Plain Groovy unit tests or annotation stubs do not execute Jenkins CPS and cannot prove resumption after restart.
When the sandbox rejects a signature, prefer a supported equivalent step; do not auto-add Script Approval or disable the sandbox.

## Layered verification

| Layer | Can prove | Cannot prove |
| --- | --- | --- |
| YAML/JJB -> XML | This configuration parses and generates; output diff | Agent nodes/plugins can run it |
| Groovy compile/static | Syntax/partial types of the compiled files | vars/SCM not included, CPS resumption |
| Local stub unit tests | Pure logic and specific call contracts | Jenkins sandbox, scheduling and real plugins |
| Declarative linter | Declarative structure accepted by the target validator | All custom steps/runtime safety |
| Approved local Jenkins | This run's behaviour on that version/agent node/plugins | Real release or another environment |

Local runs create only test jobs with the approved prefix/identity; first verify disabled/auto-trigger configuration so cron/SCM events do not start them unexpectedly.
With synthetic parameters, verify agent label/tool/workspace isolation separately on each approved agent node (count per project input); no matching node is a queue reason, not evidence of a run failure.

What a timeout covers depends on agent allocation and stage/top-level placement and needs interpretation of the actual configuration; record queue time and run time.
Cancellation verification covers both queued and running, checking child processes and the final state of resources.
Cleanup targets only resources created this run; do not call global delete-old or bulk workspace cleanup.

Missing plugin/version mismatch: keep the failing layer and the calling step, fix the matrix and plan first; do not auto-install plugins or upgrade Java.
A missing test environment stays unverified; syntax passing cannot pose as a complete successful build.
