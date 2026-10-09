# DDL, locks and constraints

## Version and algorithm

In an explicitly approved synthetic local database, obtain the server's actual version, engine, target table definition, character set/collation, row format, indexes/foreign keys/generated columns/partitions, sql_mode and relevant session isolation settings; do not read real connection strings.
When verification inputs are insufficient, complete only the pending-verification matrix and run no guessed SQL.

Check the target version's official operation matrix: whether INSTANT is possible, whether INPLACE is possible, whether only COPY is available, whether the table is rebuilt, what concurrency is permitted and under what conditions.
INPLACE may rebuild the table; INSTANT must not be read as taking no locks at all. The following are MySQL 8.4 facts; verify other versions separately:

- Fallback chain: when ALGORITHM is omitted (or DEFAULT), MySQL picks the most efficient algorithm the operation supports in the order INSTANT -> INPLACE -> COPY, and may fall to a heavier path without warning.
- Guardrail: an explicit `ALGORITHM=INSTANT` or `ALGORITHM=INPLACE` on an unsupported operation fails with an error instead of downgrading. Express "no fallback allowed" requirements with verified, supported explicit clauses.
- COPY cost: creates a temporary new table, copies row by row and rebuilds the whole table; concurrent DML is blocked during execution while queries can still read; the final table swap needs a brief exclusive lock during which both reads and writes wait.
- Rebuild space and time: COPY's temporary table copy is created in the original table's directory and needs roughly table data plus indexes in extra space; an INPLACE rebuild also writes sort temporary files to tmpdir (or `innodb_tmpdir`), which can reach table data plus indexes too. Duration grows with table size.
- Conditions where INSTANT does not apply must be checked in the official matrix. For example, each INSTANT ADD/DROP COLUMN adds one row version; at the limit (64 in 8.4) it is rejected and the table must be rebuilt to reset the count. Tables with `ROW_FORMAT=COMPRESSED`, with a FULLTEXT index, in the data dictionary tablespace, and temporary tables cannot add/drop columns INSTANT.

Examples are for a local synthetic schema only and must be re-verified per table:

```sql
ALTER TABLE sample_item ADD COLUMN display_label VARCHAR(120) NULL,
  ALGORITHM=INSTANT;
ALTER TABLE sample_item ADD INDEX ix_label (display_label),
  ALGORITHM=INPLACE, LOCK=NONE;
```

Do not merge these two statements and assume INSTANT is still supported; in MySQL 8.4 INSTANT permits only the default LOCK, so do not append LOCK=NONE.
When a statement is unsupported, keep the error and redesign the window/approach; do not automatically drop the restriction and retry.
Do not port PostgreSQL syntax such as CONCURRENTLY to MySQL; with a different engine, do not apply InnoDB conclusions directly.

## Metadata lock and stopping

Online or LOCK=NONE does not promise zero waiting. A long transaction, even one that only reads the table, can hold a metadata lock that makes DDL wait; the waiting exclusive metadata lock can in turn block subsequent requests.
Before migrating, arrange short transactions and an observation window, and use a bounded lock-wait policy.

The two wait parameters are not interchangeable (MySQL 8.4; verify other versions separately):

- `lock_wait_timeout`: upper bound on waiting for a metadata lock, applying to DDL/DML and other statements on tables; default 31536000 seconds (about one year), timed separately for each lock acquisition. Usually set a short value in the session before DDL.
- `innodb_lock_wait_timeout`: upper bound on InnoDB row lock waits, default 50 seconds; it does not apply to table locks and cannot bound DDL metadata lock waits.

Local counter-example design: session A starts a transaction reading the target table without committing -> B issues DDL -> C attempts a new query -> observe waiting and impact -> release A -> verify the final state of B/C.
Cancel/clean up only your own synthetic sessions; do not automatically kill real business transactions.

After a migration client times out, first verify whether server-side execution continues and the actual table schema, then decide to cancel/retry. Interrupting an online DDL may involve lengthy cleanup; do not immediately declare resources released.
Record the error, executor identity, observation scope and basis for termination; do not treat "the script produced no output" as finished.

## Implicit commit and atomic DDL

In MySQL 8.4, DDL such as ALTER TABLE ends the current transaction; an outer BEGIN/ROLLBACK cannot roll back earlier DDL like ordinary DML.
Atomic DDL means coordinated consistency of a single DDL statement in supporting engines; it does not mean a group of migrations and seeds are undone together within a user transaction. Design recovery for DDL, backfill and version records separately along the real commit boundaries.

Counter-example: update rows, then ALTER, then deliberately fail and finally ROLLBACK; do not expect every action to be restored.
Local tests should compare the actual final state of rows and schema, not just the client's rollback success return. Verify exceptions such as temporary tables against the corresponding statement; do not infer "all DDL behaves the same".

## NULL, unique keys and soft delete

A MySQL nullable unique index allows multiple NULLs; with `UNIQUE(code, deleted_at)` and live rows having NULL, that index alone cannot prove a code has only one live record.
Do not treat an old project's locking-read approach as a general theorem; especially when the key to insert does not exist, locking behaviour depends on indexes, isolation level and more.

Minimal counter-example, verified only in an isolated synthetic database: create unique key `(code, deleted_at)` and insert two rows with the same code and deleted_at NULL in a row; both may succeed. This is a design gap to verify, not a test to be coerced into failing.
Then test two connections doing Create/Update concurrently, recreate after soft delete, transaction rollback, deadlocks and wait timeouts.

Solutions may compare a real unique constraint, an applicable generated column, a stable business key or a serialisation protocol, but must be reviewed against existing field semantics and the actual version; do not silently change business nullability rules.
Before adding UNIQUE/NOT NULL/foreign keys, run synthetic checks for duplicates, NULLs, orphan data and encoding conflicts; for dirty data, decide a cleanup policy separately; do not use IGNORE or silent truncation to make the DDL "succeed".

Re-verify invariants when the isolation level changes. One concurrent run without a duplicate collision does not prove deduplication; use a barrier to create the window where both transactions see the key as absent, verify the final row count and error classification, and do not equate every deadlock with a business duplicate.

## Official fact check

The following are MySQL 8.4 version fact sources only; for upgrades or other versions, check the corresponding sections. Documentation does not replace actual runs.

- [Online DDL Operations](https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-operations.html): index/column operation matrix and limits (including INSTANT add/drop column limits and the row version cap); the full matrix is not copied.
- [ALTER TABLE](https://dev.mysql.com/doc/refman/8.4/en/alter-table.html): algorithm and LOCK clauses, the INSTANT -> INPLACE -> COPY order when the algorithm is omitted, failure on explicit unsupported algorithms, COPY blocking concurrent DML.
- [Online DDL Space Requirements](https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-space-requirements.html): location and space of intermediate table files and sort temporary files during a rebuild.
- `lock_wait_timeout` in [Server System Variables](https://dev.mysql.com/doc/refman/8.4/en/server-system-variables.html) and `innodb_lock_wait_timeout` in [InnoDB System Variables](https://dev.mysql.com/doc/refman/8.4/en/innodb-parameters.html): scope and defaults of the two lock waits.
- [Metadata Locking](https://dev.mysql.com/doc/refman/8.4/en/metadata-locking.html) and [Online DDL Performance and Concurrency](https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-performance.html): impact of transactions holding locks and DDL waits.
- [Implicit Commit](https://dev.mysql.com/doc/refman/8.4/en/implicit-commit.html) and [Atomic DDL](https://dev.mysql.com/doc/refman/8.4/en/atomic-ddl.html): DDL commit boundaries; atomic is not transactional.
- [CREATE INDEX](https://dev.mysql.com/doc/refman/8.4/en/create-index.html): NULL behaviour of nullable UNIQUE.

The official manual is copyright Oracle and/or its affiliates; see [Legal Notices](https://dev.mysql.com/doc/refman/8.4/en/preface.html#legalnotice). This package contains only an independent method and short paraphrased facts; it does not distribute the manual or replace its license with the MIT license shipped here.
