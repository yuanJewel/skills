# Concurrency, fuzzing and performance

## Parallelism and race detection

Use `t.Parallel` only when cases are independent and the environment allows it: check shared maps, ports, file paths, database names, the global clock, environment variables, caches and dependency quotas.
Case-local variables do not mean external state is isolated; tests that change the process environment must not run in parallel with cases that depend on it.
Handle range-variable capture per the minimum language version.

Use channels/barriers to bring the task under test to a real blocking point, then cancel or release; use a bounded timeout as the failure ceiling, not sleep to assume the task has started.
Assert that the owner receives completion and resources are released; cancel returning does not prove the goroutine has stopped.
Send background errors back to the test goroutine; do not call Fatal from a worker goroutine.

Replace the package and durations in the commands per authorised resources, and prefer the project's existing commands:

```sh
go test -count=1 -shuffle=on -timeout=30s ./target/package
go test -race -count=1 -timeout=60s ./target/package
```

Example durations are not universal thresholds; first confirm the current toolchain supports these flags.
Write the -shuffle seed into the report and rerun that seed on failure; list race failures separately and do not ignore them because a plain go test passed.
If race builds do not support the target or runtime dependencies are missing, mark it blocked; do not silently drop the race flag and claim the race check passed.

## Fuzzing

Applies to parsers, encodings, state transitions and similar code with clear invariants.
First define a detectable property: valid inputs round-trip while preserving normalised semantics, comparisons satisfy required algebraic relations, malicious input causes no panic, out-of-bounds access or runaway resources.
Merely calling the function under test without assertions is not enough; computing want with the same faulty implementation is not enough either.

Seeds include normal, empty, boundary, badly encoded and historical minimal failing inputs; purely synthetic, never captured from production.
The fuzz target must be deterministic, free of external side effects and bounded per iteration.
Invalid input may return an error, but "return on err" must not mask independently valid seeds that should succeed.

```sh
go test -run='^$' -fuzz='^FuzzDecode$' -fuzztime=20s ./target/package
```

Choose one package and one target, and set resource/time limits; fuzzing needs actual toolchain support, not inference from dependency versions.
Save the failing corpus entry, minimal input, seed, candidate and command, and turn them into a stable regression.
Running fixed seeds is not fuzz exploration; finding no crash does not mean all inputs are safe.

## Benchmarks

Use only with a performance goal or a located hot spot.
Record CPU/OS/Go version, input distribution, size, parallelism and memory statistics; whether warm-up/setup is timed depends on the action being measured.
For mutable inputs such as sorting, rebuild from a fixed baseline each iteration rather than repeatedly measuring already-sorted data; state whether copy cost belongs to the target.

The classic `for i := 0; i < b.N; i++` is widely compatible; verify the minimum version before using newer APIs.
Keep an observable result to stop the compiler from eliminating pure computation; do not treat `x := F(); _ = x` as an adequate optimisation barrier.
Measure several times under the same conditions; give no performance conclusion when the difference is below noise.
A passing benchmark does not verify business correctness; pair it with normal behaviour tests.

## Failure recovery

For a flaky test, first pin the random seed, scheduling barriers and isolation, and keep the original failure.
Adding retries until green hides races; do not automatically delete failing cases.
When a tool times out or is interrupted, verify the process final state, occupied resources and leftovers, clean up your own synthetic resources, then resume; external shared resources are handled within their authorised boundary.
