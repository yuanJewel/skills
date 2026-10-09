# Critical path and available capacity

This page computes "how these tasks can be scheduled"; it does not replace professional judgment of effort. Hour inputs come from the existing plan, comparable actuals or trials, never inferred directly from lines of code.

## 1. Record three kinds of time separately

**Accumulated effort** is the sum of participants' effective working periods. Two one-hour items finished concurrently are two hours of effort but one hour elapsed. The main task's analysis, dispatch, integration and acceptance have real cost; list them separately or count them into the matching task, neither omitting nor double-counting them.

**Feasible elapsed time** is the start-to-end span scheduled by dependencies and capacity, including phases that must wait for a previous task. **Calendar waiting** is external waiting for permissions, humans, execution channel recovery and similar; waiting that overlaps other doable work is not added in full to the tail. Unobserved interruption time is listed as unknown, not passed off as effective development.

First give a reasonable range in hours with main assumptions; when concrete dates are needed, convert using the user's time zone and actual working periods. Without evidence for human acceptance, queueing or network recovery time, list it separately as unknown; never fill in an invented constant to produce a release date.

## 2. From dependencies to capacity

Each task needs at least deliverable, dependencies, effective-hours range, file write set, environment/data occupancy, grade-word recommendation (cost tier/reasoning tier), acceptor and completion condition. Reference existing information directly.

1. Check for missing dependencies or dependency cycles; tasks with the same undecided interface are not assumed independent; complete the shared contract first.
2. Ignoring capacity for now, compute each item's earliest finish: its own time plus the maximum earliest finish of all direct prerequisites. The longest chain is the lower bound on duration and does not guarantee resources to achieve it.
3. From project configuration take each resource pool's limit and reasoning units, minus the main task, other active tasks and unknown in-flight work at that moment; different pools do not lend balance to each other unless user policy explicitly allows it.
4. Check concurrent constraints such as execution channel/host slots, machine CPU/memory/ports, sole writer and shared environment/data locks. If any is insufficient, queue or adjust approved slices; renaming a task does not create a new available unit.
5. Only tasks whose prerequisites are done and whose resources are all available enter a feasible parallel group; release resources after completion is actually confirmed, then schedule successors. Wire review, necessary rework and integration nodes in; do not assume they finish instantly outside the graph.
6. Schedule ranges separately with the optimistic/conservative input hours; the bottleneck may shift as samples change. Without statistical basis call it only an estimate range, not a confidence interval or completion guarantee.

Do not compute final concurrency only as "available units / per-task weight": different weights must be allocated by the actual mix and are bounded by other limits at the same time. Whether the main task can change its occupancy in a phase must come from actual execution capability/configuration; do not assume reasoning can be lowered just to make the schedule fit.

## 3. Synthetic worked example

The values below are only for checking arithmetic; they are not any project's default configuration or price. Task A fixes the interface, 0.5 hours; B implementation 1 hour and C UI 0.75 hours both depend on A; D independent integration and acceptance 0.5 hours depends on B/C. Total effort is 2.75 hours; ignoring resources, the critical path A->B->D is 2 hours.

Assume a resource pool of 10 units, main task 4 units, B needs 3, C needs 2, no other task occupying: the remaining 6 can hold B/C's 5 units at once. If platform and environment also allow both independently, schedule A, then B/C in parallel, then D: 2 hours elapsed.

If B/C both need exclusive use of the same test environment, they cannot run concurrently: 2.75 hours elapsed. Even with balance left in the resource pool it cannot shrink to 2 hours. If an independent environment exists but is not created/verified, 2 hours is only the path once that prerequisite holds, and its preparation time is counted separately.

When another resource pool has only 3 units left and a task requires 4, that item cannot start; an idle other pool cannot be borrowed automatically. If an unknown in-flight item still occupies 2 units, keep its occupancy; do not treat it as stopped to obtain a better estimate.

## 4. Shorten-time options must state their cost

| Option | Time it may reduce | Conditions that cannot be ignored |
| --- | --- | --- |
| Fix interfaces first, independent file write sets | Rework and mutual waiting | Up-front contract work also counts; do not expand into useless big design |
| Parallelise independent tasks | Overlappable effective hours | Resource pool, execution channel, machine, data and acceptance capacity really available |
| Deliver an independently acceptable phase first | Waiting for first delivery | State remaining scope and continuation clearly; do not claim the full release is done |
| Reuse still-valid verification evidence | Repeated runs | Candidate, environment, coverage and dependencies have not invalidated the conclusion |
| Reduce scope or change acceptance | The corresponding work | User confirms the real cost; never quietly drop tests or key behaviour |
| Model or reasoning adjustment | Possible cost/latency | Verify user configuration and quality samples first; a lower tier is not guaranteed faster or cheaper overall |

If all key work is already on the bottleneck chain, adding subtasks may only add coordination cost. State directly that there is currently no evidence-based way to speed up, and offer phased delivery or handover options; make no impossible promise.
