# Samples, accumulated usage and variance review

## Samples must be comparable

For the first group choose tasks representative of later work in method complexity, external dependencies and acceptance difficulty. Extrapolating complex work from only the simplest item underestimates rework; extrapolating everything from only the longest-failing item loses reference value. Record sample differences rather than hiding outliers.

Each sample records: delivery and acceptance scope, actual periods for authoring/review/fixes/integration, parallel overlap, waiting, failed requests, visible information on actual model and reasoning, result quality and unverified items. When the host does not provide exact periods, use an evidence-based range marked as estimate; do not infer continuous work from chat gaps.

After the first calibration keep the original estimate and update the remaining effort and feasible timeline. Re-estimate later only when task size, capacity, rework or key prerequisites change clearly; do not generate a new budget document for every small step. The user should understand the change on the current page; the detailed ledger is maintained with the task record.

## Counting boundaries for usage and cost

Prefer actual execution or vendor metering records, and verify request/execution identity. Record request parameters, model display name and actually effective information separately; without observation mark requested or unknown, and never claim an execution channel took effect.

| Visible metric | How to use | Common miscount |
| --- | --- | --- |
| Input tokens and cache hits | Verify the service definition, separate included from separately counted, then convert at the correct rate | Input total already includes cache, yet cache tokens are added again |
| Output and reasoning tokens | Record only fields the host provides and their inclusion relation | Guessing invisible reasoning volume from reasoning effort; adding reasoning again to output that already includes it |
| Call cost/bill | Verify currency, price date, model/cache/batch counting scope and coverage | Adding both the bill and the token-computed cost for the same spend |
| Retries/failed requests | Count when actually metered; list unknown results separately; first check whether it executed | Recording every failure as 0, or counting two receipts of the same execution as two charges |
| Tool, host and machine occupancy | Record visible resources and duration as the project needs | Treating scheduling units as money, or wall-clock waiting as continuous compute usage |

Without a valid price, report tokens and an unknown amount; a price without usage cannot give an exact actual cost either. At planning time a budget range with usage assumptions may be given, but it must be distinguished from the actual ledger. Budget-unit weights only control admission; do not claim they are cost multipliers.

## Interruption and retry

First save current results and the task accumulated totals, then verify whether the request is still in flight and whether it has produced files or an execution handle. Approved transient retries record count and waiting per policy; for a mutation with unclear result, check the actual state first, and do not equate a network failure with a business failure. For parameter/authentication/permission errors, correct the input or handle per boundary first; do not repeat mechanically as for transient requests.

When a retry resumes the same task, keep the stable task identity; execution attempts may be distinguished for reconciliation, but do not automatically create unlimited attempt directories or keep all output forever. Deduplicate duplicated evidence by execution identity; when different requests really each consumed, count each. Unknown usage stays unknown until evidence is obtained; never lose it in the name of deduplication.

## Variance explanation and end-of-phase reconciliation

The phase review compares original scope and results and answers at least: what the original estimate was, what was actually completed, what effective effort and elapsed time were, which waiting explains the difference, where rework came from, and how the remaining forecast and assumptions changed. When parallel periods cannot be separated, state the precision boundary; do not force out seemingly exact per-person minutes.

When clearly over expectation, state current evidence, cause and feasible options before incurring unacceptable cost; do not repeatedly say only "almost done". If the user asks for handover or phase wrap-up, save unfinished, in-flight and accumulated items within authorised scope; never mark unverified items done for a nicer actual duration. Reaching the normal estimate range is not by itself an automatic stop instruction.

Calibration knowledge keeps comparable methods and actual ranges; project values go to that project's plan/resource configuration. Configuration updates are decided by the current user; do not automatically modify all later sessions because a sample looks cheaper.
