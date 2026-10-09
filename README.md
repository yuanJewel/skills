# Shared Skill Library

English | [简体中文](README.zh.md)

38 Skill packages for AI coding assistants, covering the engineering flow from
requirement to plan, implementation, review, testing, diagnosis and release,
plus focused methods for Go, gRPC, HTTP, MySQL, Redis, Vue, Playwright, pytest,
Docker, Jenkins, GitLab, LDAP, cloud APIs and container images. Each package is
a discoverable, executable and verifiable method, not a tutorial or a command
list.

It works with any host that reads `SKILL.md` frontmatter, for example
Claude Code (project `.claude/skills/`) and Codex (project `.agents/skills/`).
Both hosts use the same single source copy.

## Quick start

```bash
git clone https://github.com/yuanJewel/skills.git
```

In the consuming project, link or copy individual packages as needed; do not
link the repository root:

```bash
ln -s /path/to/skills/plan-design  <project>/.claude/skills/plan-design
ln -s /path/to/skills/plan-design  <project>/.agents/skills/plan-design
```

When copying a single package into another project, copy the package-root
`LICENSE-*.txt` and `NOTICE.md` (if present) along with it. Whether a host
actually discovers and triggers a package can only be observed in that host;
a format check cannot sign off on it.

## Package structure

```text
<name>/
  SKILL.md              entry: triggers and exclusions, inputs, decision branches, steps, failure recovery, output, sources
  references/           topic pages read only when conditions get complex
  assets/               delivery templates and synthetic examples
  scripts/              a few deterministic read-only helper scripts
  LICENSE-<source>.txt  full licence text of an adapted source, byte-identical to the pinned upstream version
  NOTICE.md             adaptation and modification record for Apache-2.0 sources (relevant packages only)
```

The `SKILL.md` frontmatter holds `name` (same as the directory name),
`description` (what it does, when to use it, adjacent exclusions) and
`metadata.version`. The body carries the method and its judgements; reference
pages are read on demand, so the whole package never has to be loaded into
context at once.

## Design principles

- **Project facts are inputs, not constants.** Packages contain no project
  paths, role head counts, model IDs, quota numbers or real credentials; time
  zone, permission model, directory layout and the like are supplied by the
  consuming project.
- **A method grants no permissions.** Invoking a package does not authorise
  Git, production, external-service or cross-project writes; commands quoted
  from source documents are not authorisation to run them.
- **Conclusions are bound to evidence.** Output separates fact, inference and
  unverified; exit code 0, a passing format check or a "done" summary never
  substitutes for business assertions and actual results.
- **Synthetic data only.** Examples, fixtures, directories and event payloads
  are all synthetic values and contain no real accounts or addresses.
- **Clean up after use.** Containers, images, processes, ports, temporary files
  and test data created during development, testing or diagnosis are reclaimed
  at wrap-up to keep the machine tidy; only objects registered as owned by the
  current run are reclaimed, never a global clean-up. The rules live in
  `task-implementation`.
- **Single source of truth.** Plan bodies, status templates, retention methods
  and the Skill authoring method are each maintained in exactly one package;
  other packages reference them by name.

## Package list

### Roles and context

| Package | Version | Purpose |
| --- | --- | --- |
| [role-bootstrap](role-bootstrap/SKILL.md) | 0.1.0 | Locate the role contract, task scope and continuation conditions when the user asks to start a role, switch responsibilities or take over a named earlier session; supports a workspace with a single default role. Ordinary Q&A, quotations or role descriptions found in web pages do not trigger an identity change. |
| [project-context](project-context/SKILL.md) | 0.1.0 | When entering a project, switching modules, restoring context, or hitting missing material and conflicting rules, locate the minimum necessary material, verify source and currency, and return traceable facts and gaps. Ordinary concept questions do not scan the project; checkpoint persistence and handover belong to another package. |
| [context-handoff](context-handoff/SKILL.md) | 0.1.0 | At phase delivery, context recovery or takeover of a named earlier session, save checkpoints, verify results and execution liveness, continue approved work, and refresh the human-facing workbench. Ordinary Q&A creates no status file; this does not replace plan writing or history archiving. |

### Planning, execution and resources

| Package | Version | Purpose |
| --- | --- | --- |
| [plan-design](plan-design/SKILL.md) | 0.1.0 | Turn a clear requirement into an implementable, hand-over-ready multi-step plan with files, interfaces, dependencies, acceptance and budget; when a complete design exists, verify it and fill gaps. Ordinary Q&A or low-risk small changes do not force a full plan, and this grants no requirement-change or execution permission. |
| [plan-review](plan-review/SKILL.md) | 0.1.0 | Review a designated design or pre-approval plan against the original requirements, checking scope, architecture, quality, testing and performance, and report evidence-backed blockers and unknowns. Does not implement the plan and does not write a second plan on the author's behalf. |
| [subtask-dispatch](subtask-dispatch/SKILL.md) | 0.1.0 | When the host allows dispatch and the task can close independently, split subtasks, reserve resources, dispatch and verify results, and handle unknown in-flight work and recovery. Does not dispatch automatically because there are several files or for the sake of concurrency. |
| [task-implementation](task-implementation/SKILL.md) | 0.1.0 | Execute an approved task; implement within the single write scope, compare expected against actual verification, record deviations and recover from checkpoints. Does not auto-escalate design or review requests into implementation. |
| [estimation](estimation/SKILL.md) | 0.1.0 | Estimate effort, elapsed time and resource usage for a plan or release phase, calibrate expectations against dependencies and parallel capacity, and verify actual usage at delivery or takeover. A short Q&A does not get a budget sheet; an estimate does not replace plan approval, dispatch or automatic timeout termination. |

### Review and quality

| Package | Version | Purpose |
| --- | --- | --- |
| [change-review](change-review/SKILL.md) | 0.1.0 | Review whether a specified candidate change meets requirements, correctness and project standards, binding the content identity of new files, modifications, deletions and generation sources. Use for delivery re-review or an explicit change review; does not replace implementation, release approval or a full-repository security audit. |
| [security-review](security-review/SKILL.md) | 0.1.0 | Security-review a designated code change for identity, permissions, external input, command or file operations, sensitive outputs and dependencies, and report evidence-backed risks and verification gaps. Does not probe production and does not auto-fix or upgrade dependencies. |
| [ai-trace-audit](ai-trace-audit/SKILL.md) | 0.1.0 | Review a specified change for collaboration traces that only serve an AI session, false comments and ineffective template content, giving evidence and reasonable exceptions per the project content boundary. Does not detect authorship and does not automatically delete or rewrite code. |
| [coding-conventions](coding-conventions/SKILL.md) | 0.1.0 | Choose and apply project code conventions within a decided implementation, refactor or review scope, separating formatting, conventions, semantic defects and design trade-offs. Does not automatically switch formatters or tech stacks, or refactor the whole repository. |

### Diagnosis, verification and release

| Package | Version | Purpose |
| --- | --- | --- |
| [systematic-diagnosis](systematic-diagnosis/SKILL.md) | 0.1.0 | Investigate defects, build failures, cross-component errors or performance regressions, locating the cause through symptom reproduction, boundary evidence and falsifiable experiments. An approved small fix with an already clear root cause is applied directly; new feature design and completion claims are not replaced by this skill. |
| [test-strategy](test-strategy/SKILL.md) | 0.1.0 | Choose test scope, assertions, fixtures and execution isolation from the behaviour and risk of the current change, and state the reasons for what is covered and what is not tested. Use to create or adjust a verification approach; language-specific test implementation, completion judgement and release ordering are handled by their dedicated methods. |
| [verification-gate](verification-gate/SKILL.md) | 0.1.0 | Before claiming something is done, fixed or passing, verify that the claim matches the candidate, the acceptance, the execution state and the evidence scope. Reuse evidence that is still valid and add only the necessary checks; does not invent a separate test strategy or automatically rerun the full suite. |
| [release-readiness](release-readiness/SKILL.md) | 0.1.0 | When the user is preparing to go live, move from a pinned candidate, reviews and local full-suite evidence into human acceptance, handle acceptance changes and give a pre-release recommendation. In ordinary phases it only assesses the current state and does not start a full suite automatically; this skill does not release, cut over traffic or replace the user's final decision. |
| [readonly-ops-diagnostics](readonly-ops-diagnostics/SKILL.md) | 0.1.0 | Collect read-only evidence, align timelines and test hypotheses for a clearly scoped local container, dependency or request-chain failure. Use for diagnosing latency, errors or local failure rehearsals; does not perform production investigation, automatic remediation or unauthorised fault injection. |

### Material and maintenance

| Package | Version | Purpose |
| --- | --- | --- |
| [archive-maintenance](archive-maintenance/SKILL.md) | 0.1.0 | When active documents, rules, decisions or evidence need archiving, a shorter current entry, or history recovery, classify the retention contract, verify references and prove recoverability. Use for material lifecycle governance; does not perform business data migration and does not auto-clean files because they grew large or old. |
| [skill-maintenance](skill-maintenance/SKILL.md) | 0.1.0 | Design, review, or within approved scope author and upgrade shared Skills; covers method extraction, trigger and behaviour evaluation, source licensing and cross-project compatibility maintenance. Ordinary project-document wording edits and using an existing Skill to complete a business task do not trigger this package. |
| [documentation-authoring](documentation-authoring/SKILL.md) | 0.1.0 | Write or revise human-facing technical, usage and explanatory documentation, organising structure by reader purpose, verifying key facts and checking examples, links and delivery format. Does not author project governance rules or mix session workflow into business documentation. |

### Server side

| Package | Version | Purpose |
| --- | --- | --- |
| [go-patterns](go-patterns/SKILL.md) | 0.1.0 | Handle interfaces, errors, package boundaries, concurrency and resource lifecycle in Go implementation or review, choosing by the actual toolchain and existing patterns. Pure documentation or mechanical formatting changes need no expansion. |
| [go-testing](go-testing/SKILL.md) | 0.1.0 | Write, review or diagnose Go tests, choosing table-driven tests, stubs, httptest, concurrency, fuzzing and isolated integration verification by public behaviour. Existing healthy tests are not rewritten because the skill is used, and coverage does not replace fault-detection power. |
| [grpc-proto-contract](grpc-proto-contract/SKILL.md) | 0.1.0 | Design, change or review Protocol Buffers and gRPC contracts, assessing schema evolution, generated code and mixed-version runtime behaviour. Use for proto changes, client upgrades and compatibility failures; do not expand into a whole-protocol overhaul just because ordinary business code calls gRPC. |
| [http-api-design](http-api-design/SKILL.md) | 0.1.0 | Design or review new and evolving HTTP endpoints, making inputs and outputs, permissions, errors, idempotency, pagination and compatibility windows explicit. Internal fixes under an established contract verify only the affected boundaries; do not rebuild product requirements out of REST preference. |
| [mysql-migration-safety](mysql-migration-safety/SKILL.md) | 0.1.0 | Design or review MySQL table, index, constraint, backfill and startup migrations; verify the actual version, application compatibility, locks, re-entrancy and failure recovery. Ordinary read-only queries do not start the migration procedure, and production SQL is never executed automatically. |
| [redis-patterns](redis-patterns/SKILL.md) | 0.1.0 | Design, implement or review Redis data models, TTL, cache consistency, locks, idempotency and client failure handling. Use for caching, sessions, counters, rate limiting and connection problems; pure SQL optimisation or configuration format edits without behaviour change do not trigger it automatically. |

### Front end and testing

| Package | Version | Purpose |
| --- | --- | --- |
| [vue3-development](vue3-development/SKILL.md) | 0.1.0 | Implement or review the state flow, async side effects and interaction states of Vue 3 components, stores and composables. Use for a defined front-end behaviour change; do not refactor the whole front end because a Vue keyword appears, and do not force migration of existing Options API code. |
| [vue-testing](vue-testing/SKILL.md) | 0.1.0 | Write, review or diagnose behaviour tests for Vue components, Pinia stores and composables, choosing real or stub boundaries and controlling async. Use for a concrete testing need; real layout, native browser events and end-to-end chains need browser-layer evidence. |
| [playwright-e2e](playwright-e2e/SKILL.md) | 0.1.0 | Use Playwright to verify critical user journeys, browser-specific behaviour or a local front-end/back-end chain, handling reliable waits, mock boundaries, parallel isolation and failure evidence. Do not grow a single-function test into E2E, and do not treat mocked APIs as verification of the real backend. |
| [pytest-patterns](pytest-patterns/SKILL.md) | 0.1.0 | Write, review and diagnose Python pytest cases, handling fixture lifecycle, parametrization, mocks, async and parallel isolation. Use for a defined testing task; do not convert every Python script to pytest, and do not install plugins automatically. |

### Environment, integration and delivery

| Package | Version | Purpose |
| --- | --- | --- |
| [docker-local-environment](docker-local-environment/SKILL.md) | 0.1.0 | Set up, diagnose or clean up local Docker/Compose environments for development and testing, managing dependency readiness, resources and parallel isolation. Production operations, remote Docker endpoints and release decisions are out of scope for this package. |
| [external-dependency-simulation](external-dependency-simulation/SKILL.md) | 0.1.0 | Design and verify local synthetic stubs for external HTTP, SDK or messaging calls, covering contract, state, failure and recovery. For isolated development and testing; does not prove end-to-end compatibility with real cloud or external services. |
| [jenkins-pipeline-jjb](jenkins-pipeline-jjb/SKILL.md) | 0.1.0 | Write or review JJB YAML, Pipelines, plugin compatibility and the Jenkins job state loop, verifying rendering, CPS, queue, cancellation and callbacks layer by layer; run test jobs only in an approved isolated local environment and never auto-publish to or modify a real Jenkins. Deployment strategy and traffic switching belong to deployment-patterns, GitLab webhook receiving to gitlab-webhook-local-git, image build and push to container-image-management, local Compose environments to docker-local-environment. |
| [deployment-patterns](deployment-patterns/SKILL.md) | 0.1.0 | Design or review artefact deployment, blue/green, rolling and canary cutover, health gates and rollback state, and rehearse them in an authorised local synthetic environment. Use for explicit deployment strategy or script changes; does not obtain production execution rights and does not expand into unrelated cluster building. |
| [gitlab-webhook-local-git](gitlab-webhook-local-git/SKILL.md) | 0.1.0 | Design, review and synthetically verify GitLab webhook authentication, event selection, retries and out-of-order delivery, plus approved isolated local Git protocol tests. Does not register real hooks, open external tunnels, operate on repositories at real domains, or write to business repositories. |
| [ldap-rbac](ldap-rbac/SKILL.md) | 0.1.0 | Design, review and synthetically verify LDAP login, directory sync, group-to-role mapping, API authorisation and revocation. Use for bind/search, identity uniqueness and stale-session invalidation problems. It obtains no credentials, queries no real directory and does not change existing permission categories on its own. |
| [cloud-api-integration](cloud-api-integration/SKILL.md) | 0.1.0 | Design or test cloud provider HTTP/SDK client boundaries, pagination, rate-limit retries, async operation state and resource normalisation. Use for wrapping an established API set and local synthetic verification; does not perform real cloud discovery, tests or operations, and does not automatically replace existing direct calls with an SDK. |
| [container-image-management](container-image-management/SKILL.md) | 0.1.0 | Plan, execute or review container image builds, cross-registry sync, Harbor uploads, multi-platform manifest list verification and image retention cleanup. Use for artefact identity and distribution tasks; does not cover business deployment traffic switching, local Compose failures or the identically named Harbor benchmarking tool. |

## Bundled scripts

Three read-only scripts ship with their packages; they are not standalone
Skills, and their input/output contracts are documented in each package's
reference pages. Exit codes are uniform: `0` pass, `1` non-conformance found,
`2` input or runtime-condition error; finer-grained states go in the JSON
`status` field.

| Script | Purpose |
| --- | --- |
| [change-review/scripts/candidate-manifest.py](change-review/scripts/candidate-manifest.py) | Pin a review candidate: path, type, content hash, deletion state; rejects escapes from the root, symlinks and path traversal, gives no stable verdict if content changes while being read, and reports the specific reason on failure |
| [skill-maintenance/scripts/skill-lint.py](skill-maintenance/scripts/skill-lint.py) | Static check of a Skill package: frontmatter, directory name, encoding, reference reachability, placeholders; requires an explicitly specified trusted Node and marked parser, and exits 2 without one |
| [archive-maintenance/scripts/archive-verify.py](archive-maintenance/scripts/archive-verify.py) | Pre- and post-archive verification: missing items, size/hash, symlink boundaries, target conflicts, text references, recovery spot checks; read-only, never copies or deletes |

When checking any package in this library, add `--allow-reference-root <library root>`,
because packages link to files at the library root:

```bash
python3 skill-maintenance/scripts/skill-lint.py plan-design --allow-reference-root . --node "$(command -v node)" --marked-module /path/to/node_modules/marked/lib/marked.esm.js
```

## Maintenance

The three maintenance modes (design, review, implementation) and the authoring
method are described in [skill-maintenance](skill-maintenance/SKILL.md).
Upgrading the shared source copy affects every project that references it, and
already-loaded sessions do not refresh automatically; before an upgrade, pin
the affected consumers, the recovery point and the verification scope. Version
history is recorded in [CHANGELOG.md](CHANGELOG.md).

## Licence

Original content in this library is released under the [MIT](LICENSE) licence.
Packages adapted from third-party Skills each retain the full upstream licence
text and a record of modifications; sources, pinned versions, licences and the
packages that use them are summarised in
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Official technical
documentation is used only for fact-checking and its text is not
redistributed. This library does not represent an endorsement by any upstream
project or vendor.
