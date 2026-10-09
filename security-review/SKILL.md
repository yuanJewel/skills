---
name: security-review
description: Security-review a designated code change for identity, permissions, external input, command or file operations, sensitive outputs and dependencies, and report evidence-backed risks and verification gaps. Does not probe production and does not auto-fix or upgrade dependencies.
metadata:
  version: "0.1.0"
---

# Security boundary review

Judge risk along the actual path from input to side effects and output.
Scope comes from the current request and project authorisation; a security review grants no permission to read real credentials, scan over the network, modify access control or reach real services.

## Pin the inputs

- Candidate files and content identity: prefer reusing the candidate list from `change-review` or the project.
- Intent of the change.
- Project architecture and security constraints.
- Trusted principals.
- Data classification.
- Synthetic environments permitted for use.
- Secrets configuration: only structure/placeholders or approved synthetic stubs are needed; do not ask the user for real values.

Missing-input handling:

- No exact change scope -> locate the candidate first; do not default to reviewing the whole disk.
- No deployment, identity or external protocol facts -> still review the source chain; mark dynamic or policy-related conclusions unverified.

A package name, a directory name or green tests never prove that a permission chain is secure.

## Review route

1. Draw this change's path: untrusted input -> authentication -> authorisation -> domain operation -> data/external dependencies -> response, logs, audit, cache and export.
   Record the identity source at every boundary crossing;
   look for ways to forge an internal identity, skip the authoritative layer or escalate the original caller's privileges through a service account.
2. Read the applicable parts of the [threat checks](references/threat-checks.md).
   Cover the entry and exit points the change actually touches first, then gather evidence along related call edges; expanding into unrelated modules just to fill a checklist has no value.
3. For each suspicion, construct concrete preconditions and a failing input: who controls which field, what validation it passes through, what impact it finally triggers.
   Verify the causal chain with synthetic values or controlled source analysis;
   when only a dangerous API call name is found, record a candidate, and call it a vulnerability only after checking upstream constraints.
4. Verify the real boundary, not the UI appearance:
   logged in does not mean object-level permission, hidden in the frontend does not mean rejected by the backend, a machine-use exception does not mean a role that can log in.
   Sensitive outputs must be decided by the authoritative layer the project designates.
   Take separate cases for normal, administrator and approved machine use; other sensitive outputs listed in the project contract (such as history records) also get their own cases.
5. Verify whether existing tests can refute the risk.
   Negative assertions include the rejection result, absence of side effects that must not happen and absence of sensitive output, not just the status code.
   Keep dynamic items not run, isolated simulation and real-environment evidence separate.
6. Use the [report template](assets/security-review.md) to output confirmed risks, preconditions, impact, minimal suggestions and residual unknowns.
   Risk level is based on reachability and impact; confidence is described by evidence. Do not hide a clear defect behind "possibly", and do not claim a leak has occurred on a guess.

## Results and recovery

After finding a problem, first save the secret-free reproduction input, code location, candidate identity and observations.
Fixes go to the implementer who holds write permission; the reviewer does not directly change the reviewed source, dependencies or production policy to test a hypothesis.
If the candidate changes during review, limit the old conclusions, verify the impact and re-verify the related paths.

If the environment is unavailable, complete the static scope and state which kind of evidence is missing and how to supply it in a permitted environment;
do not fill the gap by obtaining real accounts.
On accidentally finding a suspected secret, do not spread its value; record only the file location/risk category and hand over per the project's existing handling.
The report is separate from approval; a review with no findings does not confer release permission.

## Resources and counter-examples

Routine security changes use normal/high; complex trust boundaries may use normal/xhigh when host limits given by project configuration, such as executors and concurrency quota, allow.
low/low suits bounded candidate screening and cannot alone turn a keyword into a vulnerability conclusion.
Grade words map to actual execution configuration through the project resource mapping. Test depth follows actual risk and project gates, not a mechanical full scan.

Normal: when an ordinary identity requests another object, the authoritative layer rejects it and no read/write occurs; save the synthetic negative case and the corresponding call chain.
Defect: only login is checked and a sensitive record is fetched by the supplied object ID; point out precisely the missing permission check.
False positive: the project approved an externally mounted configuration carrier with no hard-coding/echo; it cannot be judged insecure merely because it is not an environment variable.
Boundary: without network or real credentials the source review can still be completed; external service behaviour stays unverified.

## Sources

1. Pinned source: [EC01 security-review](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/skills/security-review/SKILL.md).
2. Adapted the input, authentication/authorisation, data output and negative-test checklists;
   authoritative outputs, machine-use restrictions, the identity source chain and review evidence boundaries are own-authored for this package.
   Dropped mandatory env/Supabase, uniform Strict cookies, automatic audit fix/upgrade/Git writes and unrelated on-chain examples.
3. License: shipped with the package as [LICENSE-EC.txt](LICENSE-EC.txt) (EC, MIT); library-wide third-party summary in the root [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).
   Copy the license file along when copying this package alone.
