# Environment failure diagnostic tree

First record node/image/candidate version, the first failure, the deadline and the single variable that just changed. Prefer state and a small amount of synthetic logs; with `inspect` select only necessary fields and never print environment variables or full mount configuration.
Change only one candidate cause at a time; keep evidence of a failure before switching hypotheses.

| Symptom | Next discriminating observation | Common fix and limits |
| --- | --- | --- |
| CLI cannot reach the engine | Actual endpoint, socket ownership, engine availability | Do not change remote permissions/global context; handle only known local startup prerequisites |
| config fails | First parse/interpolation error and the explicit file list | Fix this run's synthetic fields; do not load a real `.env` to fill gaps |
| exec format error/program not found | Image platform, entrypoint path and tool version | Verify the matching architecture image or record emulation; do not claim emulation equals native performance |
| DNS failure | Network of the caller, service alias, both sides' project | Fix this run's network attachment; do not attach an external shared network "to try" |
| Connection refused/timeout | Name resolution -> listening port -> bind address -> network reachability | Distinguish container localhost from host localhost; do not disable the whole firewall |
| permission denied | Process UID/GID, real target path, read-only mount | Adjust only directories needed this run; do not chmod the whole repository or host |
| health stuck starting/unhealthy | Probe command exists, timeout, seed version and dependency state | Distinguish probe error from business not ready; do not loosen health to a fixed 200 |
| Repeated restarts/137 | OOM flag, resource peak, exit reason and time | Exit 137 alone does not uniquely prove OOM; first reduce this task's concurrency |
| Test cross-contamination | Node resource mapping, global prefixes, seed and clock | Add isolation or serialise genuinely shared resources; do not add random sleeps to mask it |
| Old data remains after reset | Actual mount ID, whether init runs only on an empty directory | Reset only dedicated resources you are entitled to; do not delete volumes that "look similar" |

Deliver one minimal reproduction, how it differs from the counter-example, the object fixed, the retest scope and remaining gaps.
Have two nodes write and read different identifiers, and retest that when one node is stopped/cleaned up the other can still read; this proves isolation of the tested path only.
When the engine cannot start, a static configuration review can be delivered, but the runtime observations above cannot be signed off.
