# Integration isolation and time contracts

## Choose the real implementation or a stub

Stubs verify the call contract and fault responses.
SQL locks, unique constraints, isolation levels and database encodings must be verified by synthetic local integration tests against the matching engine and version.
Passing on SQLite does not prove MySQL constraint behaviour; an HTTP stub does not prove compatibility with the real provider.
The report states coverage layer by layer; not every unit test run needs to start the whole environment.

Inputs: allowed environment identifier, synthetic data, endpoint type, service version, namespace and port allocation, lifecycle responsibility.
Without these, finish pure unit/static test design first; never automatically use a default DSN, old credentials or production data.
Follow the project's configuration method; do not invent new env override rules.

Every concurrent run uses a private directory, namespace, database/schema/unique-key prefix, or a container with provable isolation.
Cleanup targets only resources you created and whose identity can be confirmed; truncating the whole database or restarting a shared container is not ordinary cleanup.
Migrations, global configuration or fixed singleton resources that cannot be isolated run serially and are marked exclusive.
Random prefixes must be long enough to avoid collisions and be saved in logs; do not set test concurrency equal to the number of execution units.

## Enabling and skipping integration tests

Follow existing build tags, flags or command conventions.
Without the enabling condition, skip explicitly and list test name/reason/impact in the summary; `go test -short` succeeding does not mean integration is verified.
If this acceptance explicitly depends on integration and the environment is unavailable, the result is blocked, not downgraded to "not applicable".

Check the business meaning of service readiness, not just a listening port; retry only recoverable startup states and with a limit.
At test start, verify the version and clean synthetic data; do not assume the image tag is the actual version.
On cleanup failure, keep the resource identity and responsibility to avoid silent leftovers.

## Clock, time zone and month boundaries

From project inputs obtain: whether a value is an instant or a local calendar time, storage type/time zone, transport format, display rules and partition/archive boundaries.
`time.Local` or the developer machine's time zone is not the contract.
Inject `Now func() time.Time` or the existing clock interface; tests that depend on real timers use controlled barriers; freezing Now alone does not mean timers are controlled.

Build a matrix for the same instant: UTC input, explicit positive/negative offset input, the project time-zone encoding, a host in a non-project time zone, and just before/after a month boundary.
If an example project chooses a fixed +09:00, `2025-01-31T14:59:59Z` and `2025-01-31T23:59:59+09:00` are the same instant, and the next second enters February for that project; the expectation comes from the contract, not from the normalisation function under test.
For regions with daylight saving time, additionally verify non-existent/repeated local times; a fixed offset cannot replace a regional time zone.

Check steps: construct the instant independently -> convert for storage/transport per the contract -> parse back and compare instants -> verify month partition and query lower/upper bounds -> ensure no double offset.
A wall-clock DATETIME carries no time zone and cannot be parsed back as UTC directly; it needs explicit project semantics.
Half-open intervals are recommended for boundaries, but if the existing contract differs, verify against the existing contract.

Go-side tests cannot sign off on browser display and user time input; that end-to-end behaviour is delivered as frontend test evidence.
Historical time-zone defects serve only as a regression source; whether a defect still exists needs actual evidence, not conclusions from old risk records.

Normal: a private database is loaded with synthetic rows and two concurrent instances operate on their own keys; time tests inject the contract zone and rerun in a process with a different time zone.
Counter-example: generating want from the developer machine's default time zone while the implementation uses the same default; test and code make the same mistake together.
