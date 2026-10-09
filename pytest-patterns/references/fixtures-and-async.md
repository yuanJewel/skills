# Fixtures, parametrization and async

## Arrange release as soon as a resource is acquired

Scope is decided by whether mutable state can be shared safely, not by "initialisation is slow" alone.
Default to function; when widening to module/session, explain state reset, concurrency and lifecycle. Do not depend on a function fixture inside a session fixture.
tmp_path is a path private to each case; when tmp_path_factory creates a longer-lived directory, mutable content must still be isolated.

The teardown after yield runs only if setup succeeded in reaching yield.
Split each acquisition step into its own fixture, or use a context manager/ExitStack:
register a release for every successful acquisition, so that a later preparation failure also unwinds the registered cleanup.

The helper (not a pytest built-in) and fixture example below use this case's tmp_path; if acquire fails internally before returning, acquire itself is responsible for its partial resources.

```python
from contextlib import contextmanager
import pytest

@contextmanager
def prepared_resource(acquire, prepare):
    resource = acquire()
    try:
        prepare(resource)
        yield resource
    finally:
        resource.close()

@pytest.fixture
def payload_file(tmp_path):
    with prepared_resource(
        lambda: (tmp_path / "payload.txt").open("w+", encoding="utf-8"),
        lambda handle: handle.write("synthetic seed"),
    ) as handle:
        handle.seek(0)
        yield handle

def test_seed(payload_file):
    assert payload_file.read() == "synthetic seed"
```

When close may fail, record the cleanup error and resource identity separately; a successful cleanup does not cover a call failure.
Close only the connections/files this case owns; do not run a global reset on a shared directory or database.
autouse is only for invariants that every case really needs and must not hide real dependencies.

## Parametrization and patch

Give each case an input and an independent expectation, for example empty collection -> empty output, no permission -> a specific rejection, duplicate ID -> an explicit conflict;
do not call the algorithm under test inside the test to generate expected. Readable ids use stable business meaning and must not contain secrets.
raises pins the exception type and a stable error code/necessary message; avoid asserting only an arbitrary Exception.

Patch the symbol the caller looks up: if consumer imports fetch from client, patch consumer.fetch; patching client.fetch does not necessarily affect the already bound reference.
Use autospec/spec_set to expose signature misuse; dynamic attributes need an explicit minimal interface. For async calls use AsyncMock and assert awaited/arguments, not just called.
When pytest-mock is absent, use the unittest.mock.patch context manager, which restores automatically on exit.

## Async mode and loop lifecycle

Verify the actual plugin and configuration first:

- In pytest-asyncio strict mode, async fixtures use pytest_asyncio.fixture.
- auto mode can take over ordinary async fixtures, but do not copy this when the mode is unknown.
- anyio and pytest-asyncio do not compete for the same test.
- The loop scope must contain the object's lifetime; a client created on one loop cannot be run or closed on another.
- loop_scope/configuration keys differ across plugin versions; verify against the current version, and do not override project configuration to force auto.

With a plugin, await the function under test and control progress through Event/Future; wrap timeout around the await that may really hang, and in finally cancel and await the tasks you created.
CancelledError is not an ordinary success; task.cancel() alone without waiting for completion is not enough.

A standalone case with no plugin and no loop-bound fixture can use asyncio.run, as in the example below;
this example verifies that cancellation completes and finally runs, not a real client integration:

```python
import asyncio
from contextlib import suppress

def test_owned_task_cancelled_and_joined():
    async def scenario():
        started = asyncio.Event()
        released = asyncio.Event()
        async def worker():
            try:
                started.set()
                await asyncio.Event().wait()
            finally:
                released.set()
        task = asyncio.create_task(worker())
        try:
            await asyncio.wait_for(started.wait(), timeout=1)
        finally:
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task
        assert task.cancelled()
        assert released.is_set()
    asyncio.run(scenario())
```

A timeout test must additionally simulate the target await timing out and verify the same cleanup; do not call timeout covered on the strength of the cancellation test above.
Real networking uses a local synthetic service and explicit deadlines; do not manufacture flaky failures with random sleeps.

Counterexamples:

- prepare raises after the resource is created, and close happens only after yield.
- All fixtures share one loop object, but each case starts a new loop.
- A bare async case is skipped and still counted green.
- Patching the defining module while the real network call goes through.
