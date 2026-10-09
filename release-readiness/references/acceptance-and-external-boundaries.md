# Human acceptance and real external boundaries

## Human acceptance package

After one local full suite meets the criteria, give the user a directly operable entry/path, the candidate, the key behaviours to look at with expectations, and the limitations not proven locally.
The human need not carry hashes or read internal logs; internal records can bind the candidate they saw by artefact identity. For a very small scope give short steps; no large table is mandatory.

Classify each piece of feedback: accepted, change requested, needs clarification, not yet operated.
Only explicit acceptance counts as acceptance; silence, "read" or "run with this for now" does not automatically become a final go-live decision.
An existing explicit approval is used within its real scope; do not ask again to confirm the same approved action.

When feedback causes a change, first separate requirement change from defect, then update the candidate relationship, the impact retest and any necessary re-review;
the affected part of the originally accepted scope needs reconfirmation.
If the user only changes copy, do not rerun the full suite as routine; if the user changes permissions, even a small change needs rejection, fields and adjacent call paths verified.
Unaffected human acceptance is not mechanically reset.

## Real external behaviour listed separately

Local simulation can verify interface contracts, event identity, approval state, failure recovery and final-state aggregation, but real external behaviour cannot be proven by simulation.
Which items exist is listed by the project contract; the table below shows two common examples, to be replaced or extended per the project contract.
When the project lacks a behaviour, give a not-applicable reason; do not impose a particular platform.

| Real behaviour | Locally verifiable | External manual item that must remain |
| --- | --- | --- |
| Real traffic switch, such as blue-green cutover/switch-back | Routing decision, health thresholds, simulated failure and recovery states, configuration structure | Real target identity, actual traffic destination, observation window and rollback result, recorded by the approved human process |
| Real code-hosting event trigger, such as a GitLab webhook | Authentication, fields, identity, permissions, deduplication and failure mapping of synthetic events; authentication distinguishes shared-token verification from signatures per the actual protocol, and X-Gitlab-Token is the former | Whether the platform's real event is delivered and triggers the correct target, and the mapping of event/job final states, verified by a human |

These unverified items must show as unverified in the real environment or pending human action; do not fold them into the local full suite and then claim all passed.
If the project makes them a go-live prerequisite, then while unverified only a conditional recommendation can be given, not an unconditional ready-to-go-live conclusion.
When user policy requires human execution in production, this skill cannot do it instead because "verification needs it".

## Time and final recommendation

For automated tests record actual start/end, necessary waits and the span of parallel shards;
for human acceptance give a justified range from the number of operations and available people, with response waiting listed separately; an external window with no information stays unknown.
The go-live window states its prerequisites; the end of automated tests is not the actual release time.

Give one main recommendation by evidence and list limitations:

- **Needs fixes or more evidence**: point out the required failed/blocked items, the impact and the minimal recovery; do not erase other valid passes.
- **Ready for human acceptance**: the pinned candidate, local full suite and necessary reviews are satisfied, and human acceptance is not yet complete; do not say it is ready to release.
- **Awaiting final human decision**: applicable review/re-verification and human acceptance are complete, and the remaining external manual items and risks are stated;
  whether a conditional go-live is allowed is decided by whoever holds that authority.

If the user has already given the final decision, cite its candidate/scope and conditions as fact; this skill ends at the readiness record and does not execute a release because that record exists.
Actual deployment, image push, production traffic cutover/rollback and real platform triggers are a separate action boundary, and their results still need separate evidence.

On takeover, recover the original decision, the candidate, completed shards, unfinished manual items and in-flight work;
do not infer from a lost previous author that all background work has stopped, and do not back-sign historical acceptance.
Update the conclusion by currently valid evidence and keep the historical originals.
