# Independent assertions and fixtures

## Expectations cannot come from the same implementation

First write down which production error would make the test fail.
Derive the expectation from requirements, the protocol, a small hand-verifiable example, a conservation property or another independent algorithm;
do not call the function under test to generate expected, and do not merely assert that a mock's return value equals the preset value.

Use mocks at external boundaries to drive the real code under test through success, error, timeout, partial result and cancellation.
Call arguments may be checked to verify a key contract, but the consumer's output and side effects must be checked too.
For example, after the dependency rejects, no "success record" may be written; assert_called alone does not prove that.
The validity of the mock's own protocol is self-checked separately; a stub self-check must not be written up as product verification.

Assertions match real semantics: HTTP status, business code, response fields and persisted state each correspond to a claim; exact value, set, order and tolerance are chosen per the contract.
Avoid checking only non-empty, no exception or unchanged snapshot.
Time and random results use a fixed clock/seed or an explainable range; do not let the host's default timezone or incidental timing decide the expectation.

## Defect regression and first-run failure

Run the target test first under the safely executable old conditions or in an isolated copy and confirm it goes red because of the target symptom;
an import failure, an unbuilt fixture or a wrong path is not a valid red.
After the fix keep the relevant preconditions unchanged, confirm green, then check adjacent behaviour by impact surface.
When the test is green from the start, first check whether it was not triggered, the assertion is too weak or the behaviour already existed;
do not automatically change it to a stricter expectation with no basis.

Non-defect tests prove their value with independent boundaries and properties, for example the total equals the sum of the items, no new writes after cancellation, a rejected request leaks no fields;
do not manufacture an error for every test or delete the implementation and start over.

## Fixture ownership and isolation

Each shard names its data namespace, database/cache keys, file directory, ports, clock and external stub instances.
Build minimal known data and verify the preconditions; do not rely on "the previous test should have set it up".
A shared read-only baseline may be reused but tests must not modify it; mutable fixtures are copied into the shard.

Cleanup handles only temporary objects this shard actually created and owns; do not wipe a shared database or delete others' data by a fuzzy prefix.
On failure, still keep enough diagnostic evidence; sensitive or business data must not be damaged by fixture cleanup.
When isolated resources cannot be obtained, schedule a mutual-exclusion window; do not quietly borrow another shard's environment.

| Failure example | How to tell and recover |
| --- | --- |
| Two shards both use a fixed user ID and one deletes the other's data | Verify concurrent execution identity and ownership; re-establish independent namespaces and rerun the contaminated shard |
| The clock depends on the current date and fails intermittently at month boundaries | Fix the clock and cover the contract-specified boundaries; keep the historical failure, do not just rerun until green |
| The stub's return value directly becomes expected and bypasses the business logic | Identify the entry point under test and switch to independent expectations driving the real consumer logic; the original test cannot be used for that claim |
| A case reports skip because a service is unavailable | A missing required prerequisite is BLOCKED; N/A only when the contract genuinely does not apply |
| Data changes cause duplicated pagination | First separate fixture drift from the interface's snapshot contract, then decide between product failure and invalid test precondition |

Local simulation proves the caller's behaviour under the constructed conditions; it does not prove the real vendor, a real Git trigger, production permissions or network reachability.
When those claims are needed, list a separate verification boundary; a stub being "more realistic" cannot be written up as the real thing verified.
