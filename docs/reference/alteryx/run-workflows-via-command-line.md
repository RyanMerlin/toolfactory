# Run Workflows via Command Line

Source:
- https://help.alteryx.com/current/en/designer/workflows/run-workflows-via-command-line.html

Key points for Tool Factory:
- `AlteryxEngineCmd.exe` is the supported command-line runner for workflows and analytic apps.
- The default installation path is `C:\Program Files\Alteryx\bin`.
- Return codes matter:
  - `0` success
  - `1` warnings
  - `2` errors
- `/amp` can be used for AMP-enabled execution on Windows.
- Validation workflows should be able to run headlessly and write local outputs.

Operational use in Tool Factory:
- `toolsmith validate` should run or prepare a workflow that is executable through `AlteryxEngineCmd.exe`.
- `toolsmith doctor` should report whether the engine executable is discoverable.
