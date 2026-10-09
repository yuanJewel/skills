# Source record template

The author submits this to the sole maintainer of the library-level source ledger; do not copy a full ledger into every package. Each package keeps only a brief source entry and the necessary licenses.

| Field | Content |
| --- | --- |
| Source ID/type | {{external method, old workspace, own-authored; record the two kinds of source separately}} |
| Pinned location | {{repository/commit/specific file URL or approved internal location, not just the repository home page}} |
| Read evidence | {{read date, content digest/hash; partial reads name the sections}} |
| Actually adopted | {{decisions/steps/structure and where they land in the package}} |
| Dropped/rewritten | {{host commands, project parameters, outdated rules and why}} |
| Own-authored parts | {{additions absent from the external original; never claim the source verified them}} |
| License/copyright/NOTICE | {{source license version, original rights-holder text, files shipped with the package, modification statement}} |
| Conflicts/unverified | {{conflicting evidence, actions pending decision, missing rights information}} |
| Package and version | {{affected packages, candidate digest, impact on shared consumers}} |
| Historical extraction index | {{old material passage -> general method/project fact/archive/deprecated/pending verification}} |

The package's Sources section follows conventions 1 and 2 of [Design and authoring method](../references/design-and-authoring.md#library-wide-author-conventions) with three numbered items; if the library-level source ledger is not published with the library, the package does not link it, and the public notice file is synchronised by the ledger's sole maintainer. When a package is copied alone the legally required notices remain, and executing the method does not depend on the library ledger existing. Material with unclear licensing is only recorded as pending verification, and its copied/adapted content is not published; never override the obligations of different sources with a license the author chose.
