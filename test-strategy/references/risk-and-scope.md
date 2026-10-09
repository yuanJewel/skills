# Risk and minimal effective scope

## From change propagation to affected behaviour

First confirm the actual candidate content and the contract difference before and after.
Find consumers along callers, shared functions, data formats, permission boundaries and state transitions; state three classes: definitely affected, possibly affected, and unaffected with a basis.
Adjacent directories do not imply a dependency, and different repositories may still share a contract.

Select tests by consequence, trigger condition and how hard the failure is for existing checks to detect; do not add risk levels up as scores.

| Risk hint | Minimal starting point | Signals to expand | Example of reasonably not testing |
| --- | --- | --- | --- |
| L0 copy, comments, static material with no execution semantics | Content/link/rendering or format check | A command, configuration, generated input or behaviour description changed | A plain typo does not run the database or a whole-site E2E |
| L1 single-component deterministic computation/branch | Independent input/output and targeted regression | Shared functions, serialisation or state persistence affected | A private pure-function fix does not automatically rebuild every service |
| L2 multi-state, data/interface combinations | Integration/contract, including failure and recovery | Transaction boundaries, mixed versions, concurrent reads/writes | A field mapping the existing contract already catches does not repeat many UI steps |
| L3 permissions, compatibility, critical paths | Rejection/out-of-scope access, mixed versions, concurrency/cancellation and the necessary E2E | The real entry point differs from underlying behaviour; state is irreversible | Local simulation cannot prove real external traffic cutover; leave an explicit later boundary |

Choose the lowest layer that "can catch it", not the lowest that "can run".
A unit test that mocks out the whole authorisation function cannot prove permissions are correct; a browser seeing only that a button appears cannot replace the server rejecting an illegal operation.
Different layers prove different claims; small slices can be combined.

## Turning acceptance into discriminating cases

Each key behaviour has at least one explicit expectation and a corresponding failure mode;
then add necessary negative cases by risk: empty/single/boundary, invalid input, rejection, partial success, re-entry/duplication, cancellation/timeout, recovery and compatibility.
Not every behaviour mechanically expands every category; note the reason for non-applicability.

Pagination example: the set is fixed as [A,B,C] with page size 2; page one is [A,B] with a non-empty next cursor, page two is [C] with a termination signal;
the aggregate must be exactly [A,B,C] with no duplicates/omissions.
Returning page one twice, terminating early on a full page and looping on a final empty page must all be caught.
When the contract allows concurrent change, define the snapshot/cursor semantics first; do not constrain a dynamic interface with a static full-set assertion on your own.

A defect fix uses a minimal reproduction to pin the failure cause.
When the old candidate cannot be executed safely, give an alternative comparison and the gap, and do not fabricate having seen red;
if it can be reproduced in a synthetic isolated copy, state that this is not the old real environment.
Tests for a new feature may be written from the approved contract; deleting existing correct functionality just to get a red is not required.

## Test trade-offs and validity after change

Classify untested content as: unrelated to this change with dependency evidence; covered by a smaller layer; currently not executable yet still required; explicitly excluded from this phase.
The first two are reasons not to test, the last two are limitations; they cannot all be marked N/A together.

After the candidate changes, verify the affected files/dependencies, generated artefacts, fixtures, runtime, environment and acceptance claims.
Existing evidence that can be shown to be unrelated continues to be cited; when impact cannot be bounded, widen to the possibly affected parts and state why.
For a change to acceptance expectations, verify the approval basis first; do not change the standard on your own after a test goes red.

The complete release full suite is carried by the pinned candidate of the go-live preparation phase;
the "all cases relevant this time" chosen day to day is called relevant regression and is not conflated with the release full suite.
An interrupted existing full suite is also recovered by execution batch and impact; cases never reached do not count as passed.
