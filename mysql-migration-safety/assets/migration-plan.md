# MySQL migration plan

- Goal/approved scope/owner and candidate identity: {{existing_task_reference}}
- Actual version/engine and evidence: {{do_not_substitute_dependency_files}}
- Old/new schema, indexes/constraints/encoding/partitions: {{explicit_diff_and_ddl_candidates}}
- Synthetic scale and basis of estimate: {{row_count_distribution_row_size_no_production_data}}
- Lock/downtime/replication/space tolerance: {{measurement_method_threshold_and_who_stops}}
- Backup and restore capability: {{actual_rehearsal_scope_recovery_point_time_unverified}}

| Phase | Old/new application reads and writes | Action/algorithm/lock | Entry and acceptance | State/recovery after failure |
| --- | --- | --- | --- | --- |
| {{expand_sync_backfill_switch_reads_contract}} | {{consumers}} | {{exact_sql_or_tool_input}} | {{decidable_condition}} | {{reversible_forward_manual}} |

- Backfill contract: {{transform_version_stable_key_high_watermark_batch_progress_commit_concurrent_conflict_missed_rows_re_entry}}
- Startup contract: {{single_executor_schema_then_seed_then_ready_or_existing_project_order_failure_not_ready}}
- Irreversible list: {{possible_data_loss_approval_boundary_and_recovery_no_universal_down}}
- Archive/time: {{integrity_and_online_plus_archive_reachability_same_instant_encoding_and_month_boundary_or_not_applicable}}

| Synthetic scenario | Independent expectation | Environment/command | Actual result | Evidence |
| --- | --- | --- | --- | --- |
| New database / old database upgrade | {{schema_and_behaviour}} | {{local_version}} | {{actual_run_or_unverified}} | {{record}} |
| Interrupt / re-entry | {{no_missed_rows_no_duplicates}} | {{failure_position}} | {{final_state}} | {{checkpoint}} |
| NULL/unique/concurrency/locks | {{constraint_invariant}} | {{two_connection_barrier}} | {{result}} | {{row_count_and_errors}} |
| Mixed old/new / time | {{compatibility_and_same_instant}} | {{input}} | {{result}} | {{comparison}} |

- Current schema/migration progress/in-flight work: {{verify_real_state_before_restart}}
- Unverified items and next step: {{documentation_check_does_not_replace_database_run_external_actions_stay_with_authorised_owner}}
