# Changelog

All notable changes to this library are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Library releases are tagged `vX.Y.Z`; package versions (`metadata.version` in each `SKILL.md`) are independent, and each entry names the packages it touches and their new versions. Entries carry a linked short commit id once committed; each link targets the full commit id.

## [Unreleased]

### Added
- `skill-maintenance` 0.1.1: a new authoring checklist collects package structure, frontmatter, the eleven author conventions, British spelling and key terms, the sole-authority index and the pre-handover steps into one page, marking each check as lint or manual. ([f07453f](https://github.com/yuanJewel/skills/commit/f07453f098036cc8808c57cb783baa0de8a170f6))
- `skill-maintenance` 0.1.1: the design and authoring method now states how to evaluate an external Skill source — read full files at a pinned commit, check license compatibility and script scope, record the source, and never install automatically. ([f07453f](https://github.com/yuanJewel/skills/commit/f07453f098036cc8808c57cb783baa0de8a170f6))
- `ai-workspace-governance` 0.1.0: add a shared method for organizing AI working materials under a project-selected root, with a common core, project extensions, selective policy-change memory, a user workbench, retention configuration, copyable agent handover instructions, and verified plan archiving with recoverable close-out. ([2e28c80](https://github.com/yuanJewel/skills/commit/2e28c80e4823b977669c93d9bba6c14c07caee72))

### Changed
- `coding-conventions` 0.1.1, `security-review` 0.1.1, `ai-trace-audit` 0.1.1, `documentation-authoring` 0.1.1: their assets templates replace descriptive prose with explicit `{{field}}` placeholders, keeping the surrounding fill-in guidance. ([f07453f](https://github.com/yuanJewel/skills/commit/f07453f098036cc8808c57cb783baa0de8a170f6))

### Fixed
- `redis-patterns` 0.1.1: the Go cache-aside template and client reference now state the client precondition for context deadlines (go-redis/v9 `ContextTimeoutEnabled`, finite dial/pool/read/write timeouts), that the cache budget applies to Get and Set separately, and that cancellation does not promise immediate interruption of started I/O. ([690c538](https://github.com/yuanJewel/skills/commit/690c5380d2033320ee00710d70c7b38b6de4307a))
- `change-review` 0.1.1: `candidate-manifest.py` returns the fixed JSON `error`/`status` object on stderr with exit 2 for missing or invalid command-line arguments instead of plain-text usage. ([690c538](https://github.com/yuanJewel/skills/commit/690c5380d2033320ee00710d70c7b38b6de4307a))

### Docs
- Remove fixed package counts from the English and Chinese README introductions. ([2e28c80](https://github.com/yuanJewel/skills/commit/2e28c80e4823b977669c93d9bba6c14c07caee72))

## [0.1.0] - 2026-10-09

### Added
- Initial public release of the shared skill library: 38 skill packages, each at package version 0.1.0, usable from Claude Code and Codex. ([7dd914a](https://github.com/yuanJewel/skills/commit/7dd914ac1ea9260ceadec22cfade5285bbfc8d7a))
  - Workflow: `role-bootstrap`, `project-context`, `plan-design`, `plan-review`, `task-implementation`, `subtask-dispatch`, `context-handoff`, `verification-gate`, `change-review`, `release-readiness`, `estimation`.
  - Quality and governance: `skill-maintenance`, `coding-conventions`, `documentation-authoring`, `security-review`, `ai-trace-audit`, `archive-maintenance`, `systematic-diagnosis`, `readonly-ops-diagnostics`.
  - Testing: `test-strategy`, `go-testing`, `pytest-patterns`, `vue-testing`, `playwright-e2e`, `external-dependency-simulation`.
  - Backend and data: `go-patterns`, `http-api-design`, `grpc-proto-contract`, `redis-patterns`, `mysql-migration-safety`, `ldap-rbac`, `cloud-api-integration`.
  - Frontend: `vue3-development`.
  - Delivery and infrastructure: `deployment-patterns`, `docker-local-environment`, `container-image-management`, `jenkins-pipeline-jjb`, `gitlab-webhook-local-git`.
- All package content (SKILL.md, references, assets, scripts, notices) written in English; third-party licenses shipped per package with a library-wide summary in `THIRD_PARTY_NOTICES.md`.
- `skill-maintenance/scripts/skill-lint.py` static checker for package structure, frontmatter, links and Markdown rendering.
