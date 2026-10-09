# Stub selection and isolation boundaries

First ask what must be proven, then choose the tool; do not deploy the largest stack out of technology preference.

| Behaviour to verify | Minimal usable stub | Cannot be inferred from it |
| --- | --- | --- |
| Mapping, state decisions, pagination loops | In-memory fake of the project's existing interface, with injected clock and random source | Real HTTP encoding, connection pools or TLS |
| Method/path/headers/serialisation/SDK compatibility | Loopback protocol stub called through the real client/SDK | Vendor real-time policies or capacity |
| Data constraints, transactions, protocol server semantics | Version-pinned dedicated local service | Cloud-managed extensions, real DR/HA |
| Long tasks, retries, failure recovery | Stateful stub with controllable scheduling/virtual clock | Latency distribution under real wall-clock load |
| UI loading/failure presentation | Route mock at the browser boundary, keeping UI behaviour | Backend integration or network protocol passing |

Existing WireMock/Mockoon may be reused, but first verify the matching, state and fault capabilities supported by that version; do not install a tool automatically when none exists. Language fakes can be lighter, but must provide call history and feedback on invalid requests. When an interface-only fake cannot catch a misspelt JSON field, add a contract test that really serialises to a local stub, rather than copying the same fake data twice.

## Egress and identity

Bind to an explicit local address or this task's internal network; consider base URL, DNS, redirects, proxies, the SDK's default credential chain and metadata access. Inject an explicit synthetic identity and endpoint, and disable fallback/proxy/record-and-forward. Do not mount host credential directories, and do not let the SDK read real configuration "just to initialise". A local name is not a local target; verify the actual resolution and connection path.

Unknown requests return a distinguishable failure and record the minimal match difference; never pass through to the real service to fill in a response, and never default to success. Request logs must not contain raw authentication fields or unbounded bodies; even when all data is synthetic, keep the minimal-field convention so it can be reused with other data.

Network isolation and call history together provide evidence: check that the final environment has no external routes/extra networks/proxy bypass, and verify that misconfiguration fails against a controlled local refusing target. Merely searching the source for no HTTP URLs does not prove there is no egress; also do not try connecting to the real cloud to verify that external access is blocked.

Lifecycle is named per task/node/scenario; initialisation/ready/reset/teardown have explicit owners. Concurrent tests do not clear all state through one global admin API. Control endpoints are used only inside the isolated test network and are not mixed into public business interfaces.
