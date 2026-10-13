<!-- Rebuild the entire page from current facts.
Delete this comment when generating the page.
Rules and pre-publish self-check: ../references/workbench.md. -->

# User workbench — {{current_development_version}}

Updated: {{date_time_timezone}}

## Q Waiting on you

### Q1 Decision: {{decision_title}} [{{requirement_id}}]

Recommended: {{option_number_and_reason}}.

1. {{first_real_option_and_tradeoff}}
2. {{second_real_option_and_tradeoff}}
3. {{third_real_option_if_needed}}

| Decision basis | Current specifics |
| --- | --- |
| What is done this time | {{scope_target_boundaries_and_existing_authorisation}} |
| Why now | {{verified_facts_change_impact_and_unverified_assumptions}} |
| Which files/artefacts change | {{concrete_reviewable_artefacts_and_affected_items}} |
| Verification and failure handling | {{pass_criteria_actual_checks_gaps_and_recovery}} |
| Time and resources | {{waiting_range_relevant_usage_prerequisites_and_unknowns}} |
| What your choice changes | {{outcomes_deferral_impact_and_required_user_actions}} |

Choose {{numbered_choice}}; {{key_information_needed_to_decide_here}}.

### Q2 Acceptance: {{result_title}} [{{requirement_id}}]

Entry: {{viewable_result_link}}. Pass criteria: {{actual_criteria}}.
Verified: {{coverage}}. Limits: {{unverified_items}}. {{exact_acceptance_action}}.

### Q3 Operation: {{action_title}} [{{requirement_id}}]

{{exact_action_and_object}}. After completion: {{observable_result}}.
For a necessary handover, forward to {{receiver}} to {{purpose}}:

> Working directory {{working_directory}}. Read {{material_root_entry}} first, then handover entry {{handover_id}} in {{status_path}} and follow it; you are {{plan_id}}'s {{responsibility}}.

## N In progress

| Task | Stage | Executor | Committed completion | Remaining |
| --- | --- | --- | --- | --- |
| {{task}} [{{requirement_id}}] | {{stage}} | {{responsibility_and_tool}} | {{absolute_time_or_waiting_on_you_q}} | {{clock_based_remaining}} |

## P Scheduled

| Task | Next stage and executor | Planned start | Estimate | Dependencies |
| --- | --- | --- | --- | --- |
| {{task}} [{{requirement_id}}] | {{stage_and_executor}} | {{planned_start}} | {{estimate_range}} | {{dependencies}} |

{{count}} backlog items: see {{task_register_link}}.

## E Ended this cycle

- {{task}} [{{requirement_id}}] — {{one_sentence_result}}, {{end_date}}, {{archive_or_result_link}}

---

Synthetic example — fictional project Cedar, version 2.4.0; replace the template with actual current facts, omitting this example.

# User workbench — 2.4.0

Updated: 2030-04-08 10:00 UTC

## Q Waiting on you

None

## N In progress

| Task | Stage | Executor | Committed completion | Remaining |
| --- | --- | --- | --- | --- |
| Export compatibility [R2] | Implementation | Implementer · Tool A | 2030-04-08 12:00 UTC | 2h |

## P Scheduled

| Task | Next stage and executor | Planned start | Estimate | Dependencies |
| --- | --- | --- | --- | --- |
| Export guide [R3] | Design · Tool B | 2030-04-09 09:00 UTC | 1–2h | Export compatibility |

0 backlog items: see the project task register.

## E Ended this cycle

- Preview layout [R1] — Accepted preview aligns with the sample, 2030-04-07, project result entry `results/preview.md`.
