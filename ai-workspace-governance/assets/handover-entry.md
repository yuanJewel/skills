# Handover entry template

Embed one entry per receiver and step in the plan's `status.md` Handovers section.
Fill known values; the nine numbered fields take their meaning from [Collaboration contract section 5](../references/collaboration-contract.md).
Delete this introduction when embedding the entry. The user forwards the locating sentence; drafting does not dispatch work.

### Handover entry {{plan_id}}-H{{sequence_number}}

| Item | Value |
| --- | --- |
| State | {{pending_or_received_time_or_handed_back_time_or_void_replacement_id}} |
| Sent by | {{responsibility_and_tool}}, {{time_with_timezone}} |
| Receiver | {{responsibility_and_tool}}, mode {{mode}} |
| Preconditions | {{candidate_identity_or_workspace_conditions_pause_if_unmet}} |
| Stage limit | {{proposed_limit}}; receiver confirmation: {{confirmed_limit_or_revision_and_reason}} |

1. {{project_working_directory_and_reading_entry}}
2. {{stable_plan_and_optional_subtask_identity}}
3. {{receiver_responsibility_and_mode}}
4. {{step_goal_and_approved_object_or_candidate_identity}}
5. {{exact_write_scope_boundaries_and_report_only_condition_including_this_entry_state_field_and_receipt_section}}
6. {{input_and_evidence_locations}}
7. {{completion_checks_and_conclusions_this_receiver_cannot_sign}}
8. {{failure_and_conflict_handling_pause_and_continue_conditions}}
9. {{receipt_location_stop_writing_hand_back_and_next_reviewer}}

### {{handover_id}} receipt

{{reception_and_limit_confirmation_results_evidence_gaps_and_stop_writing_statement}}

#### Locating sentence to forward (delivery only; do not embed this section)

> Working directory {{working_directory}}. Read {{material_root_entry}} first, then handover entry {{handover_id}} in {{status_path}} and follow it; you are {{plan_id}}'s {{responsibility}}.

For the same agent continuing in another session, omit the handover ID and point to the status's Next step instead.
If project files are unreadable to the receiver, paste the nine filled fields in full and mark the entry `Switched to pasted delivery`.
