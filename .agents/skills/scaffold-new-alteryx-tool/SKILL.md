# scaffold-new-alteryx-tool

Create a new modern Alteryx Platform SDK tool in the output repo.

## Use When

- A new tool is being started.
- A new generated tool workspace needs to be created from the factory templates.

## Inputs

- Tool name
- Tool slug
- Target Alteryx version
- Tool type
- Output repo path from `toolfactory.config.json` or `TOOLFACTORY_OUTPUT_REPO_PATH`

## Workflow

- Validate the tool spec.
- Resolve the configured output repo path.
- Create the tool directory in the output repo.
- Scaffold the workspace from the factory template.
- Write the tool README and metadata.

## Guardrails

- Never hardcode repo paths.
- Never write outside the configured output repo.
- Do not overwrite an existing tool without an explicit update request.

## Implementation Notes

- Prefer `toolsmith scaffold` and shared template files over ad hoc generation.
- Keep output deterministic.
