# Authentication, authorisation and revocation acceptance template

Roles/categories written as `{{...}}` in the table are placeholders, replaced per the project contract; reader-one, writer-one, readers and writers are synthetic directory identities.

Contract version/basis: {{contract_version_basis}}; directory product/schema: {{directory_product_schema}}; stable key/directory source: {{stable_key_directory_source}}.
scope: {{global_category_or_existing_resource_ownership}}; multi-group computation/explicit deny: {{multi_group_rule}}; no-group behaviour: {{no_group_behaviour}}.
Disable source: {{disable_source}}; complete-sync flag: {{complete_sync_flag}}; maximum invalidation delay and in-flight effective point: {{invalidation_deadline_and_effective_point}}.

| Synthetic principal/directory state | Expected authentication | Groups and roles | Resource/action/scope | Expected API/field egress | Approval condition | Actual and evidence |
|---|---|---|---|---|---|---|
| reader-one valid password | Success | Complete readers | Fill read actions per contract | Output approved fields | Judged independently | Unverified |
| writer-one multiple groups | Success | readers + writers | If the contract states {{global_write_role}} may write across resource ownership, write at that scope | Allowed scenarios must not be wrongly denied | No automatic approval permission | Unverified |
| reader-one removed from all groups | Success, if the contract defines {{read_only_guest_role}} | {{read_only_guest_role}} | Restricted write API | Rejected; also check old write sessions | Judged independently | Unverified |
| disabled synthetic state | Rejected | Cannot log in | Old session access | Invalidated per deadline | None | Unverified |
| Valid user but second page lost | Do not claim the mapping is complete | unknown | Restricted API | Rejected per failure contract | None | Unverified |

Authentication negative cases: empty username/empty password, wrong password, username `a*(b)`, duplicate identity, service bind failure, wrong CA/hostname, connection timeout, identity isolation of concurrent user binds.
Sync negative cases: same name with different key, DN change with same key, cycle/depth limit, repeated cookie, missing attribute, late old epoch.
Revocation timeline: directory change -> discovery -> authoritative version update -> requests on each node -> cache invalidation; record the time of each step and how existing requests were handled. Distinguish the maximum propagation window from actual measurement; never fill in "instant".
Bypass verification: calling the API directly, swapping resource IDs, bulk/export/download, forged body role, writes to unauthorised fields. Without actual tenant isolation, verify by global category; if the contract defines {{approval_role}}, verify its approval separately; do not fabricate tenant tests.

Conclusion: {{list_format_check_static_reasoning_protocol_synthetic_verification_unverified_separately}}. Resource ownership/cleanup evidence: {{evidence}}; items not covered against a real directory: {{uncovered_items}}; do not record passwords, tokens or real directory entries.
