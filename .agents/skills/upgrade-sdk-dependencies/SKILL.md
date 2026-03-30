# upgrade-sdk-dependencies

Upgrade pinned Alteryx SDK, CLI, or support dependencies in a controlled way.

## Use When

- Alteryx releases a new SDK or CLI version.
- The compatibility matrix needs to be updated.

## Workflow

- Update compatibility constants.
- Update template pins.
- Update docs and release notes.
- Run validation and packaging smoke tests.

## Guardrails

- Never upgrade templates without updating compatibility data.
- Never change tool runtime defaults without documenting the change.
