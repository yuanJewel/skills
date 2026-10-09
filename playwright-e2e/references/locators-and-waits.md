# Locators, waits and results

## Observe first, then drive

On a dynamic page, wait for an explainable business-ready signal, then read the rendered role, accessible name, label or stable test id.
Prefer getByRole/getByLabel; when no reasonable accessible name exists, use a test id per the project contract and record the accessibility problem.
When several elements match, narrow to an explicit region first; do not hide ambiguity with first/nth. CSS classes/deep structure change often; depend on them only when they are a stable contract.

Playwright actions auto-wait for actionability, which still does not prove the business operation completed.
For results use the auto-retrying expect (available only with the Test runner) or core's locator.waitFor/a page business condition;
the timeout comes from the project's latency criterion and has an upper bound.
networkidle is not business readiness: long polling never goes idle, and a statically idle page may still have no successful data. A fixed sleep cannot serve as a criterion.

## Register the response before the action

The function below works with the page of an existing `playwright` or `playwright-core` and does not need `@playwright/test`.
The page contract is a title input, a save button and a success status; endpoint is the exact URL of the local environment allowed for this run; the response is `{id}`.
The caller verifies the address and candidate first; do not copy a production address directly.

```js
import assert from 'node:assert/strict'

export async function saveAndObserve(page, { endpoint, title, timeoutMs }) {
  assert(Number.isFinite(timeoutMs) && timeoutMs > 0)
  await page.getByLabel('Title', { exact: true }).fill(title)
  const [response] = await Promise.all([
    page.waitForResponse(response =>
      response.url() === endpoint && response.request().method() === 'POST',
      { timeout: timeoutMs }),
    page.getByRole('button', { name: 'Save', exact: true }).click({ timeout: timeoutMs })
  ])
  assert.equal(response.status(), 201, 'save should return created')
  const body = await response.json()
  assert.equal(typeof body.id, 'string')
  assert(body.id.length > 0)
  await page.getByRole('status').filter({ hasText: 'Saved' })
    .waitFor({ state: 'visible', timeout: timeoutMs })
  return body.id
}
```

This function requires that the scenario has no parallel save to the same endpoint;
with parallel requests, also match the synthetic object/operation ID in the request so that someone else's response is not captured.
The predicate should not accept only 2xx, otherwise a 401/500 is disguised as a timeout.
Even with a correct network response, still verify the page result; to prove persistence, refresh/query the same ID over the allowed chain instead of looking only at the toast.
The example implements no product and starts no service; real browser execution is provided by the consuming project.

Navigation, popups and downloads work the same way: register the corresponding event first, then trigger the operation, and assert the URL/target identity/file content.
A failed wait keeps the original error; both Promises of the controlled click/wait pair must be observed to avoid unhandled rejections.
core has no automatic test timeout, so the caller must give the scenario an overall deadline and finally cleanup.

## Locator failures

Classify the fault as not appeared, not actionable, response missing, error response, or business state not transitioned; save the necessary synthetic screenshots/trace and request metadata.
Occlusion or a disabled state is usually a product-state problem; do not bypass it with force:true by default.
Use it only when the test explicitly requires bypassing actionability, and explain that it cannot prove the user can click.

Normal example: listen for the create response first, then click, identify 409 as a business conflict and assert the error region.
Counterexample: waiting for networkidle and writing "passed" directly, or clicking the wrong row with first and then asserting only "request sent".
