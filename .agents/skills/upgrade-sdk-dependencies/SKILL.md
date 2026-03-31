---
name: upgrade-sdk-dependencies
description: Upgrade Alteryx SDK dependencies and reconcile compatibility updates.
---

# upgrade-sdk-dependencies

Upgrade pinned Alteryx SDK, CLI, or support dependencies in a controlled way, then update the compatibility matrix and templates together.

## Use When

- Alteryx releases a new SDK or CLI version.
- The compatibility matrix needs to be updated.

## Workflow

- Update compatibility constants first.
- Update template pins second.
- Update docs and release notes last.
- Run validation and packaging smoke tests before export.

## Guardrails

- Never upgrade templates without updating compatibility data.
- Never change tool runtime defaults without documenting the change.
