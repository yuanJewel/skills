# {{plan ID}}: {{goal name}}

> Template note: continue an existing plan and fill only the parts relevant to the task. Replace `{{...}}` with real values, named pending items or a reasoned "not applicable"; keep no meaningless placeholders. Small tasks may merge sections. A complete existing design is only verified and completed, never copied into a second plan. The plan records the design baseline; dynamic state stays at the project's existing location; no extra file is required.

## 1. Identity, scope and authorisation baseline

| Field | Value |
| --- | --- |
| Plan ID / version / updated | {{stable ID; this candidate version; timezone}} |
| Mode and status | {{design/review/implementation; draft/pending/approved scope etc., per evidence}} |
| Workspace and project root | {{root given by user or host; name each root in multi-repo setups, never guess another project from cwd}} |
| Single plan location and writer | {{current original location, owner; others submit deltas only}} |
| Requirement baseline | {{original requirement location, date/version/content identity; approved requirements separated from suggestions}} |
| Current status entry | {{existing status section/file or the section this plan designates; no duplicate status record}} |
| Continuation basis (if any) | {{old task/phase, results, unfinished items, in-flight work and write-handover evidence}} |

Goal: {{observable result the user obtains and success indicators.}}

Includes: {{behaviour delivered this time, user/data/environment boundaries.}}

Excludes: {{adjacent scope easily confused, and its impact on this work.}}

| A-ID | Actual authorisation source/date/evidence location | Covered version and tasks/actions | Conditions, exclusions and current effect |
| --- | --- | --- | --- |
| A01 | {{user's original instruction or the approval original the project requires; never fabricate quotes}} | {{explicit candidate identity/scope; design only, or including implementation, etc.}} | {{effective/partially covering/pending; uncovered actions}} |

Authorisation conclusion: {{which work may continue; which concrete actions lack basis and why. Authorised scope is not re-requested because a template was filled; original approvals are not rewritten.}}

## 2. Requirements, facts and design choices

| R-ID | Type | Content and observable result | Source location/date/version | Status and boundary |
| --- | --- | --- | --- | --- |
| R01 | {{user requirement/author suggestion}} | {{user's problem separated from the proposed solution}} | {{source; author suggestions name the author}} | {{included/pending decision/excluded with reason}} |

| E-ID | Fact or assumption | Evidence location and applicable version/environment | Verified scope / impact if pending |
| --- | --- | --- | --- |
| E01 | {{verified fact/pending assumption}} | {{source symbol, interface doc, observation record; current vs historical}} | {{what it proves; which T/I/V-IDs a missing evidence affects}} |

Existing implementation and reuse: {{exact location, behaviour and version; capabilities that already exist, real gaps and the reuse method.}}

Approach: {{key method, reasons, necessary candidate comparison and costs; routine details left to the executor.}}

| D-ID | Real conflict needing a decision | Options, impact and recommendation | Blocked tasks / independently continuable parts | Decision basis |
| --- | --- | --- | --- | --- |
| D01 | {{only items affecting scope or implementation; write "none" and the verified scope otherwise}} | {{author recommendations do not pose as requirements}} | {{T-ID/concrete actions}} | {{pending or the actual user decision location}} |

## 3. Files and cross-module contracts

Paths are relative to the project root stated above; in multi-repo setups write the root name and the full in-repo path. Mark proposed new paths "new candidate"; existing paths list the actually verified location; avoid unlocatable descriptions such as `related files`.

| File ID | Project root + exact path/symbol | Current fact and planned action | Sole writer/owning T-ID | Related R/I/V-ID |
| --- | --- | --- | --- | --- |
| P01 | {{root name; path; symbol/line locator when needed}} | {{exists and verified/new candidate; what changes}} | {{writer and task}} | {{links}} |

### I01: {{interface name and authoritative definition location}}

- Baseline and proposed version: {{current doc/schema/symbol and version; new contract identity.}}
- Producer/consumers: {{modules, T-IDs; all affected parties; consumers reference this definition.}}
- Call contract: {{exact function name, parameter order and types, return type; or HTTP method/path, RPC service/method, event schema.}}
- Data semantics: {{field names, units, default/nullable, enums, identity source and relevant pagination/ordering semantics.}}
- Success and failure: {{returns, errors, state changes; relevant auth, timeout, cancellation, retry idempotency, concurrency and final state.}}
- Generation/adaptation: {{exact location and task of generated artefacts; old-client adaptation and dependency order; reason when not applicable.}}
- Verification and proof: {{facts E-ID read on both sides; type/semantic check result; V-ID; unknowns.}}

{{Other interfaces reuse the same structure; an existing exact contract is referenced by version and symbol with only the delta, never two drifting copies.}}

## 4. Phases, dependencies and acceptable tasks

| Phase ID | Observable delivery/exit condition | Tasks | Prerequisites and recipient | Parallel conditions/limits |
| --- | --- | --- | --- | --- |
| S01 | {{ends with artefacts and acceptance, not cut by day}} | {{set of T-IDs}} | {{dependency tasks and required evidence}} | {{what write sets, interfaces and environment resources allow}} |

### T01: {{loop that can be accepted or returned independently}}

- Requirement and phase: {{R-ID, S-ID; preparation that is not an independent requirement belongs to its artefact.}}
- Inputs and prerequisites: {{exact versions of upstream T-ID/I-ID, data/environment/authorisation conditions; evidence that they hold.}}
- Sole writer and write scope: {{owner; P-IDs and allowed actions; who integrates shared files.}}
- Consumes / produces: {{exact signature and semantics referenced by I-ID; artefacts and their consumers; no duplicated interface definition.}}
- Concrete steps:
  1. {{action and key decision; exact file/symbol; constrained values.}}
  2. {{implementation or adaptation result; algorithm only when necessary, no full function body.}}
  3. {{verification V-ID, which observation proves the result; closing configuration/documentation depending on the artefact.}}
- Completion condition: {{decidable artefacts and checks; which unmet conditions block handover.}}
- Failure/recovery and compatibility: {{related F-ID/K-ID; failure blocking scope and who closes it.}}
- Acceptance and evidence: {{automated/manual V-IDs; planned evidence location; not executed stated as not executed.}}
- Hour expectation and resources: {{range; assumptions; grade-word suggestion, tool/environment needs; see section 7.}}

{{Other tasks follow the same contract; loops that cannot be delivered independently are not split apart under headings like "tests" or "configuration".}}

## 5. Failure, recovery and compatibility

| F-ID / T-ID | Trigger and observable signal | State/side effects produced | Stop condition, retry/compensation/rollback path | Execution owner and permission | Recovery acceptance V-ID |
| --- | --- | --- | --- | --- | --- |
| F01 / {{T-ID}} | {{concrete failure condition}} | {{persistent or external state; "no side effect" also needs a basis}} | {{recovery baseline, steps, irreversible points; forward-fix/isolation path when rollback is impossible}} | {{who may execute; no claimed ability without permission}} | {{what to check after recovery}} |

| K-ID | Old/new consumers, producers and data | Mixed versions and migration order | Rollback window and limits | Verification/pending |
| --- | --- | --- | --- | --- |
| K01 | {{actual versions, formats, persistence}} | {{old-reads-new/new-reads-old requirements; adaptation and deployment order}} | {{whether old program can read new data; window and failure conditions}} | {{V-ID or pending E-ID; reason when not involved}} |

## 6. Tests, manual acceptance and coverage

| V-ID | R/T/I/F/K-ID | Level and prerequisite environment | Concrete input/operation/command | Expected result and independent assertion | Executor and evidence location | Actual status |
| --- | --- | --- | --- | --- | --- | --- |
| V01 | {{links}} | {{automated test/manual acceptance/static check; version and isolation conditions}} | {{executable steps; not "appropriate tests"}} | {{success/failure signal; must distinguish wrong behaviour}} | {{owner; result location}} | {{not executed/pass/fail/blocked/not applicable with basis}} |

Verification choice basis: {{changed behaviour and risk, current mandatory checks, why this level; low-risk small changes may use targeted checks without a forced suite.}}

Manual acceptance: {{who, which candidate/environment, operations and criteria; reason if not needed. Automated passes do not sign manual acceptance.}}

| R-ID | Implementing T-ID / file P-ID | Key boundaries and interfaces | Acceptance V-ID | Coverage gap and handling |
| --- | --- | --- | --- | --- |
| R01 | {{traceable to artefacts}} | {{actually relevant items among normal, error, boundary, permission, concurrency, recovery; others stated not applicable}} | {{corresponding acceptance}} | {{none/gap and owner; no pass without evidence}} |

## 7. Hour expectation and resources

The full estimate (original and current forecast, critical path, accumulated usage, cost and calibration) is filled per the `estimation` package's template; this section keeps only the three items the plan needs. Estimate location: {{estimate original location; state if not estimated separately}}.

| T-ID/shared work | Hour range | Resource assumptions |
| --- | --- | --- |
| T01 | {{research, implementation, verification etc.; integration not double-counted}} | {{grade words (cost tier/reasoning tier), tools, machines and exclusive resources}} |
| {{integration and acceptance}} | {{counted once}} | {{resources}} |

- Elapsed time: {{range and reasoning after longest dependency chain and resource-constrained scheduling; no division by concurrency; human waiting listed separately}}.
- Grade words map to actual execution configuration through the project resource mapping; record suggestion and actual configuration separately.

## 8. Self-check, delivery and continuation conditions

| Check | Actual result, location and unverified items |
| --- | --- |
| Original requirement -> task -> file/interface -> acceptance, and reverse basis | {{covered R-IDs and gaps; author suggestions not posing as user requirements}} |
| Cross-module producer and consumer signatures/fields/semantics/versions agree | {{I-IDs; verification evidence; conflicts and affected tasks}} |
| Missed boundaries, failure recovery and compatibility paths | {{F/K/V-IDs and uncovered scope}} |
| Files exact, verification executable, dependencies and sole writer hold | {{what was actually verified; missing conditions}} |
| Hours/resources, real approved version and continuation scope | {{A-IDs and actions not covered by approval; unknown not filled as pass}} |

Author self-check conclusion: {{design complete/with gaps/awaiting evidence and concrete scope; does not sign implementation, runs or independent review.}}

Independent review/manual acceptance: {{when present, point to the actual report, candidate and conclusion; state "not performed" otherwise, never signed by this table.}}

Delivery: {{single plan location and version; continuable tasks; open items; next step. An existing complete design or decided execution method creates no repeated confirmation gate.}}

Change log: {{changed version, requirement source, affected tasks and scope of invalidated old approvals/verifications; original approval evidence retained. Dynamic progress stays at the existing status entry, not appended round by round here.}}
