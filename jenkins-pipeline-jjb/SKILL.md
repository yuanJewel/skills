---
name: jenkins-pipeline-jjb
description: Write or review JJB YAML, Pipelines, plugin compatibility and the Jenkins job state loop, verifying rendering, CPS, queue, cancellation and callbacks layer by layer; run test jobs only in an approved isolated local environment and never auto-publish to or modify a real Jenkins. Deployment strategy and traffic switching belong to deployment-patterns, GitLab webhook receiving to gitlab-webhook-local-git, image build and push to container-image-management, local Compose environments to docker-local-environment.
metadata:
  version: "0.1.0"
---

# JJB and Pipeline

Inputs:

- Approved scope.
- Actual versions of JJB, Jenkins, Java and plugins.
- Job type and parameter schema.
- Job templates, macros and source list.
- Output directory.
- Agent labels and isolation.
- Local endpoint admission.
- Callback, cancellation and artefact contracts.

Missing branches:

- A version missing -> review configuration sources first; do not claim runtime compatibility.
- Environment admission missing -> offline work only.

## Expand by the layer where the failure sits

1. Draw `YAML -> defaults/project/job template/macro -> job XML -> Pipeline script -> stage/external action -> callback`. Annotate each edge with input, expansion time and artefact identity.
2. For YAML, parameter or XML differences read [JJB rendering](references/jjb-rendering.md); render offline first, then compare semantics. Pushing configuration directly is not a syntax check.
3. For Pipelines, steps and runtime read [Plugins and execution](references/pipeline-and-plugins.md); record evidence separately for linter, Groovy compilation, stub tests and real Jenkins.
4. For multi-layer strings and parameter entry points read [Quoting and secrets](references/quoting-and-secrets.md); template escaping is not safe input validation.
5. For triggering, queue, cancellation and callbacks read [Job lifecycle](references/job-lifecycle.md); keep an operation identity before initiating, and query before retrying when the result is unknown.
6. Use the [synthetic JJB example](assets/synthetic-job.yaml) to show offline template expansion; it is disabled by default and accesses no network/repository.
   For execution, enable it only in an explicitly approved test copy. When the project uses SCM, keep using SCM; do not switch back to an inline script because of the example.
7. Use the [evidence template](assets/pipeline-evidence.md) to deliver the source/plugin matrix, XML diff, actual tests and unverified items. When the current contract is already complete, fill gaps in it; do not create a parallel authoritative document.

Normal: a missing macro causes an offline failure; add the macro and parameters first, then verify the XML script, then verify on an authorised synthetic agent node.
Counter-example: marking running as soon as the queue POST returns, or archiving because a post callback said success; instead obtain the build identity and verify the final building/result.

On failure keep the source, XML, parameter snapshot and operation/queue/build identity.
An unknown initiation result must not be blindly re-sent; persist cancel intent first; late callbacks must not revive the task.
If the real trigger source (e.g. GitLab) and real traffic switching are covered by the consuming project's manual go-live verification, local rehearsal does not sign off for them.

Resource suggestion: `low/low` for mechanical rendering/diff checks; `normal/medium` for Pipeline design; `normal/high` for CPS, cancellation races, credential egress and plugin conflicts.
Grade words map to actual execution configuration through the project resource mapping.
Parallelism is set by node/workspace/external resource isolation; do not assume each stage gets its own executor.

**Wrap-up cleanup**: test jobs, build records, workspaces, agent containers and rendered output created in the isolated local environment are cleaned up after verification.
Follow the local resource cleanup rules of `task-implementation`: register identities on creation, clean up only objects registered this time at wrap-up, record evidence to keep and failed cleanups in the receipt, and use no global cleanup commands.

## Sources

1. Pinned sources: [WS02 deployment-pipeline-design](https://github.com/wshobson/agents/blob/46891e7e60da0e52baf1050b7b6391b64e84c6d9/plugins/cicd-automation/skills/deployment-pipeline-design/SKILL.md), [EC10 deployment-patterns](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/skills/deployment-patterns/SKILL.md).
2. Adopted inputs/outputs, stage dependencies and the health/failure framework; the JJB/CPS/state-machine specifics are own-authored for this package and checked against the linked official material; the upstream is not claimed to provide a complete JJB package.
   Dropped fixed gates, deployment commands, credentials, default platforms and timeouts. Re-verify against actual versions when updating.
3. License: shipped with the package as [LICENSE-WS.txt](LICENSE-WS.txt) (WS, MIT), [LICENSE-EC.txt](LICENSE-EC.txt) (EC, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license files along when copying this package alone.
