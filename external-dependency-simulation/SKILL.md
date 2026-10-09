---
name: external-dependency-simulation
description: Design and verify local synthetic stubs for external HTTP, SDK or messaging calls, covering contract, state, failure and recovery. For isolated development and testing; does not prove end-to-end compatibility with real cloud or external services.
metadata:
  version: "0.1.0"
---

# External dependency simulation

Make the stub realistic enough on the defined call surface while being able to state its differences. First obtain the public protocol version, the operations the caller actually uses, the authentication and error contracts, synthetic data rules, clock/random sources and the allowed execution environment. Without the protocol you can list differences and assumptions pending proof, but do not reverse-engineer the current implementation into the correct contract.

## Routing and steps

1. Use the [dependency matrix](assets/dependency-matrix.md) to list the real contract, stub capability, independent expectation, unsimulated items and evidence. Cover only this task's call surface; do not rebuild a complete cloud platform.
2. Read [Stub selection](references/double-selection.md) and use a narrow transport fake, protocol stub or isolated service as needed. Choose the smallest tool that reaches the failure layer under test; avoid always-containers or always-in-memory mocks.
3. Read [Contract and state](references/contract-and-state.md) to define strict request matching, response semantics, state changes, repeated requests and reset. Unknown requests must fail visibly and never go out.
4. Read [Failure injection](references/failure-injection.md) to cover success/empty set, rejection, malformed data, pagination, rate limiting, timeout, disconnect and recovery as the caller actually handles them. Mark separately whether a server-side side effect has happened; do not treat every failure as retryable.
5. Cross-check the stub with the caller's or SDK's contract tests. Expectations are obtained independently from the public contract/approved requirements; do not just make the stub return data the implementation under test likes. Execution logs record only synthetic allowed fields; pin the seed, virtual clock, node and scenario identity.
6. Deliver the configuration/fixtures, run and reset method, actual results, differences and unverified external boundaries. After interruption keep state and in-flight identities, confirm the old execution has stopped before resuming, and never silently reset globally.

The [HTTP declaration example](assets/http-stub.json) is a neutral contract fixture, not a format any specific tool can import directly. When implementing the adapter, verify the semantics of every field; do not claim the stub has run just because the JSON parses.

## Quality and boundaries

Normal requests should observe output and call count; negative cases should observe that nothing was called or an explicit rejection. Resetting two nodes independently must not delete each other's data; malformed JSON, missing required fields and unknown requests must actually trigger failure. Internal pure functions need not all be mocked; keep the necessary real serialisation/transport boundaries.

A passing simulation supports only the synthetic paths tested. List differences such as real load, vendor authentication policies, real webhook delivery and actual traffic switching separately; they cannot sign off on production verification. Never record samples from real business traffic; when replay is needed, record only local synthetic traffic and still verify its format/timing against the independent contract.

Resource guidance: organising known fixtures uses `low/low`, stub implementation uses `normal/medium`, protocol/concurrency/partial-success semantics use `normal/high`. Grade words map to actual execution configuration through the project resource mapping; concurrency is provided by the current project configuration. Prefer the minimal call surface and a bounded failure matrix; when over budget, close out with uncovered items listed rather than cutting costs by deleting failure cases.

**Wrap-up cleanup**: stub service processes or containers started this run, occupied ports and generated recording files are reclaimed after verification ends. Follow the local resource cleanup rule of `task-implementation`: register identity on creation, reclaim only objects registered this run at wrap-up, write evidence to keep and failed cleanup items into the receipt, and use no global cleanup commands.

## Sources

1. Pinned sources: [EC09 docker-patterns](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/skills/docker-patterns/SKILL.md), [EC11 api-connector-builder](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/skills/api-connector-builder/SKILL.md).
2. EC09 provides the isolated environment reference; EC11 provides the narrow call surface and transport layering. Stub selection, the state machine, independent contracts, unknown-request rejection and the difference table are own-authored for this package.
   Nothing is attributed to unread appendix pages. Dropped the real API examples and uniform coverage requirements.
3. License: shipped with the package as [LICENSE-EC.txt](LICENSE-EC.txt) (EC, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Copy the license file along when copying this package alone.
