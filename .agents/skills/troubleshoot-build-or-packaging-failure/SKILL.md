---
name: troubleshoot-build-or-packaging-failure
description: Diagnose and fix failures in scaffold, validation, reconcile, build, export, or YXI packaging.
---

# troubleshoot-build-or-packaging-failure

Diagnose and fix failures in scaffold, validation, reconcile, build, export, or YXI packaging.

## Use When

- A validation step fails.
- Packaging fails.
- Workspace drift cannot be reconciled.

## Workflow

- Read the failing command and artifact path in the output repo or generated workspace.
- Check compatibility and environment pins against the current matrix.
- Check template drift and output-repo drift.
- Fix the smallest root cause first.
