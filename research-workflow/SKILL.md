---
name: research-workflow
description: Guide machine learning ideas, comparable experiments and Introduction-led paper drafts. Excludes routine coding and general documentation.
metadata:
  version: "0.1.0"
---

# Research workflow

Keep the research question, implemented method, experiment and paper claim aligned. This package serves
machine learning algorithm research across projects; the current project's data, resources, permissions and
existing scripts remain inputs, not constants supplied by this skill. Paper drafting is a mode of this package,
not a separate skill.

Make the paper's testable explanation of the problem its primary research claim. Design experiments to test the
predicted mechanism and limits; use outcome gains to establish practical value. A stronger score alone does not
establish the explanation, and tuning alone does not supply the paper's argument.

## Start and inputs

Choose the requested mode and deliver its artefact. An author may ask for more than one mode in one task; read
only the supporting pages needed for those decisions.

| Mode | Entry | Deliverable |
| --- | --- | --- |
| Idea assessment | New mechanism or novelty question | Same-field overlap, decisive test and verdict; [method](references/ideas.md) |
| Experiment | Design, run, replay or interpretation | Protocol, measurement and next decision; [method](references/experiments.md) |
| Paper drafting | Section, figure, table or response | Requested text and claim structure; [method](references/paper-writing.md) |

Resolve missing inputs only where they affect the next decision:

- Research question, target task or modality missing -> recover the latest author decision; if still ambiguous,
  ask before substituting a task from an older plan.
- Current method or measurement identity missing -> inspect implementation, metadata, original command, script
  and raw record; mark a claim provisional when its evidence cannot be recovered.
- New idea's same-field open-source baseline missing -> search primary papers and code; if the closest work has
  no usable framework, adapt a general baseline from the next broader field. Do not invent a new experiment
  framework merely to fill the gap.
- Paper audience, template or requested section missing -> use the existing manuscript convention; ask only
  when the choice changes the structure or claim. A request for one section does not create a full paper.
- Execution resources or project rules missing -> settle the scientific design, then obtain the required run
  context before starting dependent work. This skill grants no device, budget or external-write permission.

## Method

Run the relevant steps as **action / stop condition / artefact**. A narrow discussion or paragraph edit uses
only its relevant steps; a formal idea validation continues through the experiment decision.

1. **Fix the claim and evidence state.** State the problem, proposed insight, closest alternative, predicted
   mechanism observation, practical outcome and result that would change the conclusion. Separate author
   decision, code, executed protocol, raw result and inference. Stop a factual claim if its implementation
   or record is unknown; keep the question and missing evidence visible. Artefact: a short claim chain tied
   to actual sources.
2. **Select the comparison.** For an actionable new idea, inspect the closest open-source paper in the same
   field, clone its code and adopt its experimental framework. Compare the mechanism and setting, not just
   names. For a replay or related experiment, inspect the original script and metadata first. Stop causal
   attribution when multiple factors change together; label the result as a combined comparison. Artefact:
   baseline identity, intended sole change and the smallest discriminating test.
3. **Design and advance the experiment.** Fix measurement units, controls, correctness checks and decision
   criteria before a run. Track each active idea in [`TASK.md`](assets/TASK.md) and
   [`PROGRESS.md`](assets/PROGRESS.md); re-read the task before each step and update progress after completion.
   Reuse a valid original script; for a similar new experiment copy its author-designated final script and
   change only method logic. Stop at an unsupported resume boundary or incomparable protocol; preserve all
   existing raw records. Artefact: a [protocol card](assets/experiment-protocol.md), run evidence, conclusion
   and next test. After each experiment, ask whether its script should become that experiment's final script.
4. **Draft from the Introduction.** For a full paper, set the four-part Introduction spine, paired problem
   and solution figure, and three contributions before expanding Method and Experiments; the optional
   [paper spine](assets/paper-spine.md) records those decisions. Motivation analysis expands the insight;
   method design expands the proposed framework. Keep one term and one symbol per named entity or action
   throughout. Stop a submission-ready claim when its result or source is unverified. Artefact: the requested
   manuscript text, with pending results marked in LaTeX or Markdown source comments in a working draft.
5. **Reconcile and deliver.** Check that prose, figure, table, code and measurement describe the same method
   and event. A changed protocol or corrected result keeps its old raw source and a separate output identity.
   Stop publication claims that depend on a missing or non-comparable result; continue the valid parts of the
   task. Artefact: the requested answer or table first, with provenance in the project's evidence location,
   actual completion state and the next dependency when work remains.

Do not turn a research question into an automatic benchmark or manuscript. Once mechanism feasibility and no
direct same-field collision are established, drafting can begin while main comparisons mature. An unfinished
trend in a working draft is a hypothesis with a source comment, never measured evidence or a submission-ready
result. A completed main table is a prompt to remind the author that the paper can proceed.

## Boundaries and scenarios

- Normal: an augmentation idea is compared in the closest same-field open-source framework, with data,
  backbone and training budget matched; an ablation isolates the proposed part. The conclusion says which
  gain is measured and which mechanism remains uncertain.
- Adjacent non-trigger: renaming a variable in research code follows ordinary implementation practice unless
  it changes the method claim or reported protocol. A request for a Method paragraph does not launch runs.
- Failure: a previous run used a different model or metric boundary. Preserve both records, identify the
  difference, and rerun only a matched comparison before claiming improvement. If a manuscript sentence
  predicts an unrun trend, keep its verification comment in the source and withhold it from final claims.

Use `project-context` for project-source retrieval, `systematic-diagnosis` for a performance anomaly and
`verification-gate` for completion claims when those packages are available. Routine reading and drafting
use low/low; novelty disputes and experiment design use normal/high. Grade words map through the project's
resource configuration; actual machines and execution order are project inputs.

## Sources

1. First-party source: the author's research instructions and corrections in the conversation that created
   this package; no external research method was adapted.
2. Own-authored synthesis: claim-to-evidence reasoning, same-field baseline selection, controlled experiment
   progression and Introduction-led drafting. Project-specific commands and GPU rules remain runtime inputs;
   no third-party skill text was adapted.
3. License: package content is under the library [MIT license](LICENSE-LIB.txt); see the library
   [third-party summary](../THIRD_PARTY_NOTICES.md) for other packages.
