# Synthetic provider and pagination template

The model below opens no network and reads no environment credentials; `fetch_page(token)` is injected by the caller. It applies only to a normalised interface where "None/empty string means no further token, items is a list, id is a unique string"; the adapter first validates the actual provider response and maps it to this contract. Reporting every duplicate ID as incomplete is a conservative choice of this example; when overlapping pages are actually allowed, define a separate dedup contract.

```python
class IncompleteSnapshot(Exception):
    pass

def collect(fetch_page, cancelled, max_pages):
    if max_pages < 1:
        raise ValueError("max_pages must be positive")
    token = None
    tokens, identities, values = set(), set(), []
    for _ in range(max_pages):
        if cancelled():
            raise IncompleteSnapshot("cancelled")
        if token in tokens:
            raise IncompleteSnapshot("repeated token")
        tokens.add(token)
        try:
            page = fetch_page(token)
        except Exception as error:
            raise IncompleteSnapshot("page failed") from error
        if cancelled():
            raise IncompleteSnapshot("cancelled")
        if not isinstance(page, dict) or not isinstance(page.get("items"), list):
            raise IncompleteSnapshot("invalid page")
        for item in page["items"]:
            if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"]:
                raise IncompleteSnapshot("invalid identity")
            if item["id"] in identities:
                raise IncompleteSnapshot("duplicate identity")
            identities.add(item["id"])
            values.append(item)
        token = page.get("next")
        if token is None or token == "":
            return values
        if not isinstance(token, str):
            raise IncompleteSnapshot("invalid token")
    raise IncompleteSnapshot("page budget exhausted")
```

The return value comes only from the complete set; on exception the caller must not use the partial values as a complete snapshot. The caller also needs an overall deadline, element/response size budgets, finer error categories and auditing. This model does not implement HTTP retries, signing, SDK or polling; do not claim those pass based on it.

Synthetic input table:

| Scenario | Pages/behaviour | Expected |
| --- | --- | --- |
| Empty first page still has next | []/next=a, then id=one/end | Complete with one; no early termination |
| Complete empty | []/no next | Complete empty; may reconcile by ownership |
| Repeated token | next=a appears repeatedly | Incomplete; deletion forbidden |
| Later page fails | First page succeeds, then raises | Incomplete; existing resources kept |
| Cancellation | Cancelled before or after a page | Incomplete; later pages not requested |
| Duplicate ID/missing ID/invalid token | Construct the explicit exception | Incomplete and the category is observable |
| Budget exhausted | next still present when the page budget is used up | Incomplete |

Additionally verify against the actual client: 429/Retry-After, connection reset, unknown write result, polling pending/failed/unknown, out-of-bounds nextLink and rejection of metadata egress. The test transport rejects unregistered requests by default; only recorded requests/synthetic responses count as evidence, and no real cloud is contacted.
