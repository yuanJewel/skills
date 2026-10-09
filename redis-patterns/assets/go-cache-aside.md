# Go cache-aside base template

Applies to: a losable display cache whose authoritative source lives elsewhere; inject an already built go-redis client; the template creates no connections and reads no configuration.
It requires an explicit contract that cache failure may degrade to the source. Do not reuse it directly for permission/session/lock/idempotency authority.

The code below uses the Get/Set result interfaces of go-redis/v9; read the actual dependency version from the project. TTL and the cache operation budget are passed in by the project; a zero value must never accidentally become persistent.
Found distinguishes not-found from a legitimate empty string; only cache negatively when the authoritative source explicitly reports not-found. notify receives an error category, not the value or full error; the project may add non-sensitive metrics.

```go
package cacheexample

import (
    "context"
    "encoding/json"
    "errors"
    "time"

    "github.com/redis/go-redis/v9"
)

type Client interface {
    Get(context.Context, string) *redis.StringCmd
    Set(context.Context, string, interface{}, time.Duration) *redis.StatusCmd
}

type Entry struct {
    Found bool   `json:"found"`
    Value string `json:"value"`
}

type envelope struct {
    Version int `json:"version"`
    Entry
}

func ReadThrough(ctx context.Context, client Client, key string,
    ttl, negativeTTL, cacheBudget time.Duration,
    load func(context.Context) (Entry, error), notify func(string),
) (Entry, error) {
    if ttl < time.Millisecond || negativeTTL < time.Millisecond || cacheBudget <= 0 {
        return Entry{}, errors.New("invalid cache durations")
    }
    if err := ctx.Err(); err != nil { return Entry{}, err }
    report := func(kind string) { if notify != nil { notify(kind) } }
    readCtx, cancelRead := context.WithTimeout(ctx, cacheBudget)
    raw, err := client.Get(readCtx, key).Result()
    cancelRead()
    if err == nil {
        var item envelope
        if json.Unmarshal([]byte(raw), &item) == nil && item.Version == 1 {
            if err := ctx.Err(); err != nil { return Entry{}, err }
            return item.Entry, nil
        }
        report("cache_decode")
    } else if !errors.Is(err, redis.Nil) {
        report("cache_read")
    }
    if err := ctx.Err(); err != nil { return Entry{}, err }
    value, err := load(ctx)
    if err != nil { return Entry{}, err }
    if err := ctx.Err(); err != nil { return Entry{}, err }
    lifetime := ttl
    if !value.Found { value.Value = ""; lifetime = negativeTTL }
    body, err := json.Marshal(envelope{Version: 1, Entry: value})
    if err != nil { return Entry{}, err }
    writeCtx, cancelWrite := context.WithTimeout(ctx, cacheBudget)
    err = client.Set(writeCtx, key, string(body), lifetime).Err()
    cancelWrite()
    if err != nil { report("cache_write") }
    if err := ctx.Err(); err != nil { return Entry{}, err }
    return value, nil
}
```

Limitations: no miss coalescing, version fence, jitter, source rate limiting or cross-instance coordination; concurrent misses on the same key hit the source multiple times.
Before hot-key use, add bounded in-flight coalescing per the "cache consistency" topic; when strict update consistency is required, use a version/authority strategy rather than deploying this base template directly.
Decode version 1 has only this example's fields; real objects must add schema validity checks and a size limit, and must not accept arbitrary untrusted JSON.

Usage and results table:

| Item | Fill in |
| --- | --- |
| Source authority/degradation condition | {{why_source_data_may_be_returned_on_cache_failure}} |
| key/encoding/TTL | {{tenant_view_version_normal_negative_budget_and_jitter_range}} |
| Concurrency/invalidation | {{hot_key_coalescing_update_version_strategy_delete_ordering_and_limits}} |
| Runtime identity | {{go_client_redis_version_real_isolated_instance_or_stub}} |
| Verification | {{hit_empty_value_negative_cache_expiry_corruption_source_error_cancellation_write_failure_concurrency}} |
| Recovery/unverified | {{namespace_resource_owner_unknown_results_remaining_protocol_proof}} |

Positive example: the cache read times out, the parent request is still valid, the authoritative source returns a displayable object, and the degradation is recorded.
Counter-example: a source rejection is wrapped as Found=false and written to the cache. A cache Set error does not erase the source success, but parent cancellation still returns cancellation.
