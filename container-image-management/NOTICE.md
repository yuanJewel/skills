# Sources and modification notes

This package reorganises the image management method from the sources below; it copies no upstream scripts or service implementations.

- ECC docker-patterns: adopted the scenario-check/counter-example organisation and the boundaries for build context, keeping secrets out of layers and platform verification; the original MIT license is retained. Dropped unrelated installers, production execution and global cleanup commands.
- Docker Buildx: command and content-copy facts were verified against pinned documentation and implementation; the original Apache-2.0 license is retained; the original implementation is not distributed.
- Harbor: queries and the two kinds of deletion were verified against the pinned API; the original Apache-2.0 license is retained; official web pages were used for fact checking and their text was not copied.
- This package's operation states, content-evidence grading, single-writer/recovery/retention judgments and separation of consuming-project parameters are own-authored. The method does not represent endorsement by Docker or Harbor.

Upstream links, commits and applicability limits are in SKILL.md and the technical-sources reference; this notice does not override upstream license obligations.

## Modification record

- 2026-10-09: 0.1.0 initial public version, content as above.
