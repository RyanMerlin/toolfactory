---
name: package-yxi
description: Package a generated Alteryx tool workspace into a distributable YXI.
---

# package-yxi

Build a YXI package for a validated tool in the configured output repo.

## Use When

- The workspace is reconciled and ready to package.

## Inputs

- Tool spec path
- Resolved output repo path

## Workflow

- Confirm the workspace exists and has already passed validation.
- Run the YXI build flow.
- Copy the produced YXI into the tool's dist folder in the output repo.
- Record the package location for release and catalog updates.

## Guardrails

- Do not package if validation or reconciliation fails.
- Do not package into the harness repo.
