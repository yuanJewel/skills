---
name: mysql-migration-safety
description: Design or review MySQL table, index, constraint, backfill and startup migrations; verify the actual version, application compatibility, locks, re-entrancy and failure recovery. Ordinary read-only queries do not start the migration procedure, and production SQL is never executed automatically.
metadata:
  version: "0.1.0"
---

# MySQL migration safety

Inputs:

- Actual MySQL version and storage engine; `go.mod`, an image name or an old report cannot prove the current database version.
- Old and new schema, including indexes and constraints.
- Reads and writes of the affected tables/columns by the old and new applications.
- Data size estimate and its source.
- Lock and downtime tolerance.
- Migration owner.
- Backup and restore capability.
- Permitted local synthetic environment.

## Pick the route by change type

1. **Classify the change**
   - Do: separate expansion (table/column), constraint or index, backfill, and contraction/drop. Additive does not mean risk-free; widening also requires verifying charset, row size, algorithm and consumers.
   - Stop condition: only an ordinary query -> do the matching query analysis only; do not enter the migration procedure.
   - Artefact: list of change types and risk points.
2. **Design phases**
   - Do: use [Migration phases and recovery](references/migration-phases.md) to write expand -> sync/backfill -> switch reads -> stop old writes -> contract.
   - Stop condition: small changes without old/new coexistence may be simplified; do not mechanically create every phase for each index.
   - Artefact: phase sequence and old/new read-write matrix.
3. **Verify DDL and locks**
   - Do: use [DDL and locks](references/ddl-and-locks.md) to verify the algorithm, metadata lock and implicit commit for the actual version, engine and operation. The MySQL 8.4 official facts in that file are only a version example.
   - Stop condition: target version not verified -> do not specify an algorithm; list a pending-verification matrix only.
   - Artefact: algorithm, lock and commit boundary for each DDL statement.
4. **Write the migration plan**
   - Do: with the [migration plan template](assets/migration-plan.md), give each step its entry criteria, DDL/data action, progress, abort threshold, failure state and recovery method. Reuse the existing migration tool and approval boundaries.
   - Stop condition: destructive change not approved -> stop at that step; do not bypass permissions via "run automatic migration on startup".
   - Artefact: completed migration plan.
5. **Local synthetic verification**
   - Do: in an authorised local environment, run synthetic schema/data through normal, interrupt-and-re-enter, mixed old/new application, NULL/duplicate, concurrency and time-boundary cases. Record only what was actually executed.
   - Stop condition: no environment -> deliver a runnable design with the database-behaviour column marked unverified; do not substitute SQLite or reasoning from documentation for MySQL results.
   - Artefact: actual run results or unverified items in the scenario table.
6. **Closing verification**
   - Do: after a successful migration, verify the actual schema and constraints, backfill completeness and application readiness.
   - Stop condition: failure -> keep the completed steps and the failure state; stop false readiness that depends on the schema. Do not clear the dirty flag or force the version number so the service appears ready.
   - Artefact: final-state evidence or failure-state record.

## Missing inputs and outputs

- Actual version missing -> design phases and verification scenarios first; do not specify a supported DDL algorithm.
- Old application read/write information missing -> do not guarantee a rolling upgrade; list consumers pending verification.
- No verifiable recovery plan -> do not promise "can roll back" for irreversible actions.

Describe reversible schema, irreversible data and forward fixes separately.

Normal: adding a nullable column, first ensure existing writes maintain the new value, then backfill in batches and verify old and new reads agree; after old consumers retire, contract separately.
Counter-example: renaming the table in PostgreSQL's `CREATE INDEX CONCURRENTLY` and using it as a MySQL script, or assuming an outer transaction can undo all DDL.

For interrupt recovery, first verify whether the migration lock/executor is still present, the actual schema and the committed batches, then decide on re-entry; a client disconnect does not mean the database operation failed. Do not delete unknown progress or rerun non-re-entrant steps.

Mechanical schema-diff tidying may use low/low; phase design uses normal/medium; locks, constraints, concurrency, irreversibility and time/archive integrity use normal/high. Grade words map to actual execution configuration through the project resource mapping.
Throughput and duration come from synthetic scale and actual resources; do not write estimates as real production measurements.

**Closing cleanup**: temporary databases, schemas, containers and backfill data used for rehearsal are cleaned up when the rehearsal ends; real databases are out of cleanup scope. Follow the local resource cleanup rules of `task-implementation`: register identities at creation, at closing clean up only the objects registered this time, write evidence to keep and cleanup failures into the receipt, and use no global cleanup commands.

## Sources

1. Pinned source: [EC07 database-migrations](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/skills/database-migrations/SKILL.md); MySQL fact check in [official 8.4 sections](references/ddl-and-locks.md#official-fact-check).
2. Adopted only the expand/contract, batching and recovery organisation; the MySQL-specific content is own-authored for this package, no official manual text is copied, and Oracle material is not relabelled MIT.
   Dropped production data copies, PG syntax, universal rollback and automatic version forcing. Re-verify the relevant algorithms/limits on version upgrades or schema changes.
3. License: shipped with the package as [LICENSE-EC.txt](LICENSE-EC.txt) (EC, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license file along when copying this package alone.
