# Data Obfuscator Harness Issues

This checkpoint records harness issues encountered while building the `data_obfuscator` SDK tool.

## Resolved

- `toolsmith scaffold` needed to enforce a CLI-only workspace bootstrap.
- `toolsmith scaffold` initially failed on interactive `ayx_plugin_cli` prompts.
- The factory venv was missing `pip`, which blocked `create-yxi`.
- The build path needed `NODE_OPTIONS=--openssl-legacy-provider` for the generated UI webpack step.
- The factory compatibility matrix needed to pin `ayx-plugin-cli` to `1.3.2` only.

## Open

- `designer-install` currently fails at runtime because `grpc._cython.cygrpc` cannot load from the installed YXI runtime.
- The validation workflow is still a placeholder and needs a real headless workflow pattern that the engine can execute.

## Follow-Up

- Make the CLI-only scaffold rule explicit in every new-tool skill and guardrail file.
- Add a regression test for non-interactive `sdk-workspace-init` and `create-ayx-plugin`.
- Add a regression test for `create-yxi` with `pip` missing from the factory venv.
- Add a regression test for the Node/OpenSSL legacy-provider workaround in YXI builds.
- Add a preflight that checks the build-time CLI and SDK dependency stack before scaffold/build starts.
