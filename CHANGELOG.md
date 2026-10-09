# Changelog

All notable changes to this library are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Library releases are tagged `vX.Y.Z`; package versions (`metadata.version` in each `SKILL.md`) are independent, and each entry names the packages it touches and their new versions. Entries carry the short commit id once committed.

## [Unreleased]

## [0.1.0] - 2026-10-09

### Added
- Initial public release of the shared skill library: 38 skill packages, each at package version 0.1.0, usable from Claude Code and Codex. (7dd914a)
  - Workflow: `role-bootstrap`, `project-context`, `plan-design`, `plan-review`, `task-implementation`, `subtask-dispatch`, `context-handoff`, `verification-gate`, `change-review`, `release-readiness`, `estimation`.
  - Quality and governance: `skill-maintenance`, `coding-conventions`, `documentation-authoring`, `security-review`, `ai-trace-audit`, `archive-maintenance`, `systematic-diagnosis`, `readonly-ops-diagnostics`.
  - Testing: `test-strategy`, `go-testing`, `pytest-patterns`, `vue-testing`, `playwright-e2e`, `external-dependency-simulation`.
  - Backend and data: `go-patterns`, `http-api-design`, `grpc-proto-contract`, `redis-patterns`, `mysql-migration-safety`, `ldap-rbac`, `cloud-api-integration`.
  - Frontend: `vue3-development`.
  - Delivery and infrastructure: `deployment-patterns`, `docker-local-environment`, `container-image-management`, `jenkins-pipeline-jjb`, `gitlab-webhook-local-git`.
- All package content (SKILL.md, references, assets, scripts, notices) written in English; third-party licenses shipped per package with a library-wide summary in `THIRD_PARTY_NOTICES.md`.
- `skill-maintenance/scripts/skill-lint.py` static checker for package structure, frontmatter, links and Markdown rendering.
