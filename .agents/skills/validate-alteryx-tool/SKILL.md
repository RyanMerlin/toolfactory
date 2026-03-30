# validate-alteryx-tool

Validate a generated Alteryx tool spec, workspace, and support files.

## Use When

- Before packaging.
- Before merging changes to templates or shared validation logic.
- Before approving a regenerated tool.

## Inputs

- Tool spec path
- Optional `--check` mode

## Workflow

- Validate the YAML spec against the schema.
- Verify compatibility metadata.
- Check workspace drift.
- Check the validation contract.
- Check output repo configuration if the workflow needs generated output.
- Run the validation workflow command if requested.

## Guardrails

- Fail fast on schema drift.
- Fail fast on workspace drift.
- Keep validation read-only unless the caller explicitly requests reconciliation.
