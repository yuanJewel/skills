# Client and authentication boundary

## Existing pattern first

Separate the domain interface from provider details: domain reads input -> provider parameters/signing -> injected transport -> protocol response -> domain result/error. The constructor explicitly receives endpoint/transport, a synthetic credential provider, a clock, and retry/page budgets; the client must not scan environment variables, config files or metadata on its own for real credentials.

Direct HTTP: request building, signing and transport can be replaced independently; the synthetic transport records requests and returns fixed responses. Existing SDK: use its public endpoint/resolver, credential provider and HTTP client injection; confirm the actual behaviour of default retries/redirects/credential refresh. When the default chain cannot be disabled, do not construct and execute; deliver only the gap and an adapter design. Tests do not require installing a new SDK.

## Request scope and addresses

The call inventory is exact down to provider, API version, method/action, region, target resource, pagination and error codes. Open only this run's scope. The synthetic transport rejects unregistered requests and all external addresses by default; "read-only cloud API" is not authorisation for real cloud access.

nextLink/operation URLs in responses are data: validate scheme/host/port against the provider contract and the allowed local mapping, and forbid carrying authentication to an arbitrary host. Redirects are validated hop by hop as well; a default client that follows automatically may bypass isolation. Metadata/link-local addresses and every real target other than localhost should be rejected at the test egress; replacing only the first request URL is not enough.

URL encoding, path normalisation and parameter ordering must follow the specific signature version; a synthetic key/fixed nonce/clock can verify signatures against known vectors, but do not write a generic implementation on the assumption that "all of Alibaba Cloud uses one algorithm". A fake-auth check proves request construction, not that the real service accepts it. Do not print full authentication headers, signing material or secrets from raw responses.

## Result mapping and cancellation

Keep the provider request/operation ID for reconciliation; error categories stay as authentication, authorisation, parameter, rate limit, transport, business/final state and unknown. Map internal details to safe domain errors; do not wrap every non-200 as an empty list.

Pass down the shorter of the parent deadline and the local one; SDK retries, pagination and polling all count against the same budget. After cancellation stop further pages/retries and send no compensating writes; an async task already committed remotely may continue, and cancelling the local wait does not justify claiming the remote task was cancelled.

Verify the applicable direct HTTP and SDK paths: the synthetic transport runs without real authentication configured; all requests are captured by the recorder and network egress is forbidden; a fixed clock and responses prove construction/parsing. When the SDK is missing, state explicitly that SDK initialisation/the default chain is unverified; do not infer safety merely from the interface being injectable.

Counter examples: first page local, nextLink changed to the real cloud and authentication sent anyway; empty test-environment endpoint falling back to production; automatically trying another real region after a timeout.
