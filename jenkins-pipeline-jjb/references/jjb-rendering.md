# JJB offline rendering

First lock down the YAML and include/defaults/macro sources allowed to be read; do not scan the whole working directory to fill in templates.
Entry points, template variables and Jenkins build parameters are different layers: JJB `{name}` is substituted at generation time; Jenkins parameters are read at build time. Never treat the two as one variable.

JJB [Job Definitions](https://jenkins-job-builder.readthedocs.io/en/stable/definition.html) currently shows 6.5.0: brace variables in job templates need explicit values, and literal braces are doubled inside templates.
List parameters may produce a Cartesian product, so list expected job names and counts before rendering. Missing sources, duplicate names or unexpected combinations are not correct by default.

[Pipeline Project](https://jenkins-job-builder.readthedocs.io/en/stable/project_pipeline.html) defines `project-type: pipeline`; `dsl` and `pipeline-scm` are mutually exclusive, and sandbox must be chosen explicitly.
For an existing SCM entry, record the script path, version and shared library version; correct generated XML does not prove the script in SCM is this run's script.

## Procedure

1. List the source -> job template/macro -> expected job mapping; classify parameters as required, default, empty string, boolean and list; check whether YAML implicit typing changes content.
2. Use an installed JJB of matching version and output to a new approved directory. The example is offline only:

```sh
jenkins-jobs test -o {{approved_output_dir}} {{synthetic_job_yaml_in_approved_dir}}
```

Provide no real server configuration/credentials; do not run update, delete or remove old jobs.
The tool may read environment/default configuration: first verify offline inputs for its version and use an approved blank/synthetic configuration; do not invoke it until confirmed.
A missing tool is recorded as blocked; do not fake JJB rendering with string replacement.

3. Check exit code, output file count and job names, XML parseability, script/SCM content, parameter defaults, sandbox, labels, triggers and permission differences.
   Ignore only known non-semantic serialisation differences; never ignore fields such as disabled, credentials IDs or triggers to shrink the diff.
4. Missing macros/required parameters, wrong types, duplicate job names and extra combinations form negative cases.
   If a version leniently accepts unknown fields, report them in this run's schema check; "JJB reported no error" does not prove the input is valid.
5. Keep the generating source identity together with the XML identity. A source change requires re-rendering; editing only the generated XML is lost at the next generation and does not count as a template fix.

After JJB, the doubled braces in the example should be restored to Groovy blocks; if residual `{{` or wrongly substituted runtime variables appear, stop further steps.
A plain YAML parser only validates YAML syntax; it does not prove JJB macros, XML or plugin support.

Normal: generate exactly one synthetic job, with parameters and agent node from determinate scalars in the project.
Counter-example: two lists unintentionally expand into multiple real-named jobs; such overreach must be caught against the list before pushing.
When output already exists or the request result is unknown, verify existing artefacts first; do not overwrite the only failure evidence.
