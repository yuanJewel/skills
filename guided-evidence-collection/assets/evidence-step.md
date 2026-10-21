# Evidence round {{round_id}}

The agent fills this template before handing it to the user; remove unused step sections and resolve missing inputs explicitly.
Use 1–3 steps; unknown results remain unverified, not assumed normal.

Hypotheses to distinguish: {{hypothesis_ids_and_predictions}}.
Outcome mapping: {{result_for_each_hypothesis_and_what_would_weaken_it}}.
Order and first split: {{why_first_step_divides_the_plausible_hypotheses}}.
First variable block: {{one_command_setting_all_round_variables_without_secret_values}}.

## Step {{step_id}}

- Execution location: {{machine_cluster_context_namespace_or_browser_page_and_confirmed_target_identity}}.
- Action and read-only rationale: {{observation_and_checked_semantics}}.
- Command or click path: {{one_command_per_block_or_numbered_panel_request_field_path}}.
- Expected normal output: {{synthetic_normal_example}}.
- Expected abnormal output: {{synthetic_abnormal_example_and_hypothesis_mapping}}.
- Fields to paste: {{minimal_fields_plus_execution_time_timezone_and_environment}}.
- Redact before pasting: {{sensitive_fields_to_remove_and_local_visual_inspection}}.
- Output budget: {{window_lines_rows_bytes_field_lengths_requests_timeout_or_sampling_limit}}.
- Alternative if unavailable: {{safe_observation_point_or_responsible_owner_and_needed_fields}}.

## Returned evidence and next round

Safe observations and source labels: {{minimal_fragments_with_labels_per_guided_evidence_collection}}.
Hypothesis update: {{systematic_diagnosis_hypothesis_ledger_locator_and_changed_support}}.
Conclusion or next round: {{narrowed_cause_or_gap_and_next_discriminating_observation}}.
Stopping/recovery: {{failed_declined_or_unknown_steps_and_confirmed_execution_state_before_resuming}}.

## Non-evidence operation (optional)

Proposed action: {{state_changing_action_excluded_from_evidence_steps}}.
Impact: {{affected_objects_users_and_failure_risk}}.
Rollback: {{how_to_restore_and_known_limits}}.
Decision-maker: user; {{decision_needed_and_separate_authorised_workflow}}.
