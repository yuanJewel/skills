# Local resource cleanup

Temporary resources produced during development, testing, diagnosis and builds are reclaimed when the task ends or is wrapped up after interruption, keeping the local machine tidy. This page is the library's single cleanup rule; other packages reference it by package name and add only the concrete objects of their own domain.

## What to reclaim

| Category | Typical objects |
| --- | --- |
| Containers and images | Containers, Compose projects, networks, anonymous and named volumes started this run; temporary images built this run that are untagged or no longer needed; temporary buildx builders |
| Processes and ports | Background dev servers, stub services, browsers and drivers, watchers, debuggers, test child processes; the ports they hold |
| Files and directories | Temporary directories, generated intermediate files, downloaded packages, log copies, coverage and trace output, reproduction scripts, temporary instrumentation code, local test repositories |
| Test data | Synthetic databases/schemas, Redis namespaces, queues, test users and directory entries, Jenkins test jobs |

## How to reclaim

1. **Register on creation.**
   - What: when starting or generating a resource, record its identity (container/image ID, process PID, absolute path, namespace, project name) and purpose in the task's resource list or receipt.
   - Stop condition: a resource whose stable identity cannot be obtained is not created, or is started in a way that allows registering its identity.
   - Artefact: this run's resource list.
2. **Reclaim item by item at wrap-up.**
   - What: after completion, abandonment or recovery from interruption, verify per the list that each identity still belongs to this run, then stop processes and delete containers/images/files/test data. Stop before delete; reclaim dependents in reverse dependency order.
   - Stop condition: objects whose identity does not match, that may be in use by others or other tasks, or that are still needed as evidence are not deleted.
   - Artefact: reclaimed list and remaining list.
3. **Report the remainder.**
   - What: state in the receipt what was reclaimed, what was kept and why (evidence retention, user request, still referenced, no permission to delete), plus objects whose cleanup failed and the next step.
   - Artefact: the "Resource cleanup" item of the receipt. Without it the task cannot be called complete.

## Boundaries

- Reclaim only objects this task registered as its own. Do not infer ownership from name prefix, time or "looks unused".
- No resource list -> report suspected leftovers only, delete nothing.
- No global cleanup: no `docker system prune`, `docker image prune -a`, `pkill <wildcard>`, deleting whole cache directories or similar commands that affect others' resources. Batch cleanup explicitly authorised by the project is the exception.
- The user's existing containers, images, processes, files and data are untouched even when they share a name or type with this run's objects.
- Failure evidence that must be kept (traces, logs, reproduction inputs) is stored first per the project retention rule or `archive-maintenance`, then the remaining temporaries are reclaimed.
- Resources left by subtasks are taken over and reclaimed by the dispatcher per the `subtask-dispatch` receipt; the end of a session does not mean cleanup happened.
