# Expansion layers and secret egress

Label the interpreter of every string segment: YAML -> JJB template format -> Groovy literal/GString -> shell -> invoked program.
Write the expected input and output layer by layer; doubled template braces only address JJB placeholders and do not prevent shell injection.

Validate parameter types and allowed values first; pass complex parameters through explicit data files/argument arrays, avoiding concatenated executable code.
A Groovy GString `${...}` is evaluated before the shell; a shell `$VAR` must survive to the shell through the chosen Groovy literal.
Prefer non-interpolating Groovy single-quoted strings and let the shell use quoted variables, rather than inlining untrusted params into the command.

```groovy
// Fragment: MESSAGE has been validated per business rules and bound via a trusted environment; it is not inlined into shell source.
sh 'printf "%s\\n" "$MESSAGE"'
```

This still requires controlling the environment value's origin, length and program argument semantics; never hand the string to eval. Separating options with `--` also requires support from the target program.
Verify parameters containing quotes, newlines, dollar signs, semicolons, backticks and braces with synthetic markers; do not test only alphanumerics.

Secrets come from the consuming project's existing credentials mechanism (credentials binding); templates reference only logical credentials IDs; never read real values to build examples.
Do not interpolate secrets in Groovy, enable set -x in the shell, embed secrets in URLs, or save the whole environment/request/console log as evidence.
Masking is only a log defence; it does not guarantee nothing leaks through process lists, artefacts, exceptions or the workspace.

Define field allowlists separately for authentication headers, callback bodies, error logs and archived artefacts; operation/job/build identifiers may be used for correlation, and secret parameters are never recorded verbatim.
Synthetic tests use a recognisable fake-secret marker; verify the marker is absent from logs and artefacts, without connecting to a real credentials store.

Locate failures starting from the earliest interpretation layer: report YAML parse errors, missing JJB variables, XML script mismatches, Groovy compile errors, shell syntax errors and business parameter errors separately.
Never replace recording the actual expanded text with "add more backslashes until it runs".
For sensitive candidates keep only redacted information; never write secret text to disk to produce a full diff.
