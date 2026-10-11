# Paper writing

Use this page for machine learning algorithm paper drafts, figures, tables, and reviewer responses. The
Introduction determines the paper's argument and the role of later sections. First establish what problem the
paper solves, what insight explains it, and how the method follows from that insight. Then expand those parts
throughout the manuscript. Turn engineering observations into a research question and a mechanism; do not
write the paper as a development log or technical report.

Keep the explanatory insight as the centre of the paper's argument. Experiments should test its predicted
behavior and boundaries, while outcome comparisons show what practical benefit follows. Do not make the
manuscript a sequence of tuning choices or infer that the explanation is correct solely from a high score.

For a full draft, fill the [paper spine](../assets/paper-spine.md) in the manuscript's existing planning
location. If the central problem, insight, comparison figure, or names of key entities cannot yet be stated,
deliver that working structure and the exact open decision before expanding a contradictory full manuscript.
A request for one section uses only the part of the spine that section depends on.

## Establish the Introduction's structure

Use this four-paragraph progression as the default working outline; adapt its length to the venue without
breaking the causal chain.

1. **Background and problem:** give the wider setting and lead to the specific problem the paper addresses.
2. **Current methods and unresolved issue:** explain how the closest methods in the same field work and the
   precise problem they leave. Usually end this paragraph with that problem. Refer to the before/problem
   panel of the central comparison figure.
3. **Insight and motivation:** investigate the problem through the method's or structure's native behavior.
   State the insight briefly and show why it suggests a way to solve the problem. Name the research principle,
   not just an engineering trick.
4. **Method overview:** following the insight, summarize the proposed framework and the role of each part.
   Refer to the after/solution panel of the comparison figure.

End with three contributions by default: the problem and motivating insight; the proposed method; and the
experimental result and performance. Do not claim an unmeasured outcome as established. Map each later
section to the Introduction paragraph it expands: motivation analysis develops paragraph 3, method design
develops paragraph 4, and experiments test the problems and claims established by all four paragraphs.

Include a visual contrast for the existing problem and proposed solution. Choose a two-panel layout suited to
the content and single- or double-column format: one panel can show the before/after mechanism and the other
the before/after performance, or the left panel can show the old method and the right panel the proposed one.
Connect the second paragraph to the problem/left panel and the fourth to the solution/right panel. A planned
performance panel is a figure specification until its data exist; do not present it as a measured result.

## Write Method as motivation and design

**Motivation analysis** expands the third Introduction paragraph. For each insight, pose the question the
analysis answers, potentially as a question-form paragraph heading. Use a simple, feasible visualization or
diagnostic experiment where it clarifies the mechanism: a statistic, heatmap, bar chart, or another plot suited
to the observation. Explain in order: what problem was observed; why it happens; how the proposed principle
addresses it; why that principle can work; and what this implies for the method design. Give each material
insight enough analysis to carry the next section. Keep benchmark comparisons and detailed run configurations
in Experiments or an appendix; a Method diagnostic still needs enough context to interpret its plot.

**Method design** expands the fourth Introduction paragraph. Introduce each new entity through a short causal
chain: the remaining problem, what resolving it requires, the entity introduced for that requirement, and why
it solves the problem. Never bring in an unexplained component. State the implementation logic needed to
understand and reproduce the method, while leaving real experimental configurations and performance results
out of this part. Avoid excessive defensive prose; check that the argument has no logical contradiction.

Choose the aid that the method actually needs: pseudocode for a procedure whose order or branching carries
the contribution, a framework figure for interacting modules and data flow, or prose alone when it is clear.
Define every symbol before using it. Maintain a one-to-one mapping between each entity or action and its name
and symbol throughout the Introduction, Method, Experiments, captions, and appendix. Once a term is chosen,
do not invent a synonym later; use the exact term from Introduction paragraph 3 for the same insight and from
paragraph 4 for the same component. A code-level handoff is a separate supporting artifact when requested:
give files, functions, state transitions, and discrepancies with a prior draft there, while the paper explains
the research mechanism.

## Write Experiments around conclusions

Make comparisons reconstructible in Experiments or the appendix: task and data, selection and split, method
versions, baselines, training and evaluation procedures, budget, outcome metric, repetitions, and aggregation
where material. A table caption should identify the comparison and metric; detailed provenance can stay in an
appendix or project evidence record. Repeated configurations must refer to the same measurement record.

In the main text, describe the trend and conclusion from each main or ablation table. Do not repeat individual
table values by default. Discuss a specific value directly when the author requests it; when you judge that
a value must be discussed, explain why to the author. Discuss ablations that bear on novelty, the proposed
mechanism, and plausible criticisms of the Method, rather than listing every row. Explain meaningful failures
and trade-offs. Use measured language without inflated adjectives; when a fair, verified field-wide comparison
establishes a new state of the art, state that directly.

Order the experiment narrative around the claims: show the problem and predicted mechanism, test the proposed
explanation with controlled evidence, then report the practical gains and limits. A main performance table can
show that the method works in the tested settings; only diagnostics and controlled comparisons can support the
stated reason. If the mechanism evidence is mixed, say so and narrow or revise the claim instead of letting
performance gains stand in for it.

Drafting may begin once the mechanism is feasible and the same-field novelty check finds no direct collision.
For an unfinished experiment, the working draft may contain a table skeleton and a proposed trend sentence,
with a LaTeX or Markdown source comment marking the claim as awaiting measurement. Do not invent numbers.
Keep verification comments out of the visible paper prose, but resolve them before treating that sentence as
a finding or delivering a submission-ready manuscript. A predicted trend never becomes evidence just because
it was written in a draft.

## Check the manuscript

Trace every quantitative statement, figure, novelty claim, and causal explanation to the actual method,
verified literature, or measurement. The current code and executed protocol determine factual method claims;
planned work remains planned. Check the full paper for terminology and symbol consistency, unexplained
entities, unsupported transitions, and any mismatch between figure panels and prose. Write the Abstract from
the established Introduction and verified results so it does not promise more than the paper shows.

The author can choose not to report details that are immaterial to the claims and do not impair scientific
integrity or necessary reproducibility. Do not silently omit a limitation, conflicting result, or materially
relevant source when that omission would mislead readers. For similar work in another field, alert the author;
do not add it to the comparison or Related Work on your own unless the author directs it. If a source is
essential to an accurate novelty claim, explain that conflict before finalizing the manuscript.

For reviewer responses, address the precise objection first, then the mechanism or evidence and its limit.
Deliver the requested paragraph, section, figure specification, or table without an unrelated work log.

Example: the Introduction identifies a failure mode in the closest method, derives an insight about why it
occurs, and sketches the proposed fix. The Method motivation uses a simple diagnostic plot to explain that
failure; the design section defines the fix; the main comparison and targeted ablation test whether it helps.
