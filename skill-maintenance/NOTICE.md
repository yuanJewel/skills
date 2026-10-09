# Source and modification notice

The method structure of this package is partly adapted from skill-creator in Anthropic's anthropics/skills project:
https://github.com/anthropics/skills/blob/683bc88e56f3e09ba94f7055977f3d3aa499f202/skills/skill-creator/SKILL.md

The source version is pinned at 683bc88e56f3e09ba94f7055977f3d3aa499f202 and is licensed under the Apache License 2.0; the full license is in LICENSE-AN.txt.

Modifications: the method was rewritten and reorganised; adopted progressive disclosure and the goal, draft, behaviour evaluation and feedback loop; added three independent task modes, extraction from two kinds of sources, shared upgrades and failure recovery; removed the fixed host CLI, viewer, automatic installation and the per-round human round-trip requirement. The lint script is own-authored for this package; it is not a copy of an Anthropic script. This notice describes the adapted source; it does not claim Anthropic endorses this package, nor does it relicense any other source.

## Modification record

- 2026-10-09: 0.1.0 initial public version, content as above.
