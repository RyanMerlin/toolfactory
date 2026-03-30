# package-yxi

Build a YXI package for a validated tool.

## Use When

- The workspace is reconciled and ready to package.

## Inputs

- Tool spec path
- Resolved output repo path

## Workflow

- Confirm the workspace exists.
- Run the YXI build flow.
- Copy the produced YXI into the tool's dist folder.
- Record the package location for release and catalog updates.

## Guardrails

- Do not package if validation or reconciliation fails.
- Do not package into the harness repo.
