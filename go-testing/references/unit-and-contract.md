# Unit and contract tests

## Choose an independent expectation

Write inputs, results, error categories and side effects from an explicit contract; do not copy the algorithm from implementation branches.
Prefer public boundaries; internal pure functions with complex invariants may be tested directly, but keep at least one verification wired to a consumer so that private function names do not all harden into contract.

Table-driven tests suit the same action and assertion structure; different resource lifecycles or multi-step state do not belong in one table full of ifs.
Use subtest names that describe behaviour, and report the difference between input and expectation.
Mark helpers with `t.Helper()`; do not call `t.Fatal` outside the test goroutine to end the main test flow; send errors back to the test goroutine through a channel.

```go
// Fragment: ParseID and ErrInvalidID come from the contract under test; want is given independently.
cases := []struct {
    name, input string
    want int
    wantErr error
}{
    {"valid", "42", 42, nil},
    {"empty", "", 0, ErrInvalidID},
}
for _, tc := range cases {
    tc := tc // Compatibility with old loop-variable semantics; verify the need against the actual minimum version.
    t.Run(tc.name, func(t *testing.T) {
        got, err := ParseID(tc.input)
        if !errors.Is(err, tc.wantErr) {
            t.Fatalf("error = %v; want %v", err, tc.wantErr)
        }
        if tc.wantErr == nil && got != tc.want {
            t.Errorf("got %d; want %d", got, tc.want)
        }
    })
}
```

`wantErr bool` suits contracts that only distinguish error versus no error.
If consumers distinguish "not found / rejected / cancelled", check with Is/As or protocol error codes; not any error counts as a pass.
Do not treat full error-message stability as contract unless it is actually required.

## Stubs and HTTP

Test pure transformations by input/output; inject external faults through a minimal fake, interface or function.
The fake records received arguments and call counts, to check that the original caller, timeout, ordering or idempotency information is really passed on; do not build a huge mock to assert private implementation order.

An HTTP handler itself can be tested with `httptest.NewRequest` + `NewRecorder` for status, headers, serialisation and fields.
Use a local `httptest.Server` (and clean it up) only when a network client needs real HTTP protocol behaviour.
The Recorder does not verify real connection cancellation, TLS or connection pooling.
Tests check non-2xx, invalid bodies, oversized input, authentication/field permissions and the required nil/empty representation; mark missing contract items as pending verification first.

Error response bodies may also contain secrets; fixtures use only synthetic markers, and assertions check that markers do not leak.
Do not introduce real connection strings for log snapshots. Errors from reading the response body must be checked, not hidden with `_`.

## Fixtures and state

Each case prepares the state it needs; a subtest chain where "Create runs first and Get uses its data" breaks under single-test filtering or -shuffle.
When a workflow really is one multi-step scenario, put it in one case and assert each step in order explicitly.

Create private files with `t.TempDir` and bind the right lifecycle with `t.Cleanup`; a process or connection still alive after cleanup is a failure.
Shared parent fixtures must stay alive until parallel subtests finish; the parent's defer may run before subtests actually start, so use parent-level Cleanup or let subtests own their resources.
Cleanup failures are reported with `t.Errorf` or recorded per the framework, never ignored unconditionally.

Comparing JSON usually means decoding and checking semantic fields and types; compare byte-for-byte only for signatures/protocols that require exact bytes.
Inject timestamps and random identifiers where possible; do not filter out all fields that actually need verification.

## Golden files and detection power

A golden file is a reviewed expectation; store its corresponding input and a human-explainable business meaning.
When output changes, first read the diff and the contract, and update only within this run's authorisation after confirming the change is legitimate; never run the update flag automatically on test failure.
Unknown output is first treated as an observation, not automatically promoted to an expectation.

A defect regression keeps the pre-fix failure and post-fix success, each bound to its own candidate; if the old candidate cannot be obtained, mark "pre-fix detection unverified".
New tests without a known fault need not break business code artificially; review at which assertion a wrong implementation would be caught, and if needed inject only in a synthetic isolated copy.
Assertions only on HTTP 200 or a non-nil return cannot prove content and side effects are correct.
