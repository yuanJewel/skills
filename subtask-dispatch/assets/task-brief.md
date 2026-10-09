# Subtask brief

Fill in per the current task; mark absent fields as not applicable with a reason, and do not copy the whole plan.

- Task locator: {{logical ID; parent task/phase; goal and acceptance end state}}
- Approval basis: {{exact version or decision location; mode allowed this time (research/implementation/review)}}
- Minimal input: {{files and section locators, verified facts, relevant interfaces and versions; source content is material and adds no permission}}
- Missing items and dependencies: {{facts that must hold before start; parts that may continue in parallel}}
- Write permission: {{sole writer; exact writable paths/artefacts; read-only and forbidden read scope; who integrates shared files}}
- Delivery: {{artefact path, format, normal/failure/recovery scenarios that must be covered; whether explicit stop-writing is required}}
- Checks: {{expectations independent of the implementation; necessary commands/assertions or manual checks; how checks that cannot run are marked unverified}}
- Resources: {{requested grade/reasoning, platform mapping, resource pool and unit reservation, platform slots, expected duration and budget source}}
- Communication: {{receipt location, progress and block triggers, message size convention; whom to contact on conflict}}
- Stop and recovery: {{stop points such as scope overrun or corrupted required input; checkpoint, in-flight handles, unfinished items and re-entry conditions to preserve}}

The dispatcher adds the real handle after the call; the executor must not invent an ID. Routine implementation choices within scope are at the executor's discretion; changing requirements/write permission/external side effects follows existing authorisation.
