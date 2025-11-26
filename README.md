# User Display Optimizer

This repository contains an optimized user display utility and tests. It includes:

- `user_display_original.py` — the unmodified original reference
- `user_display_optimized.py` — improved, typed, logged, and more efficient version
- Cross-platform scripts and Docker support to set up and run tests

Quick Start (Linux/macOS):

```bash
./setup.sh       # create venv and install deps
source .venv/bin/activate
./run.sh         # run optimized module and timing
./test.sh        # run tests with coverage (>85%)
./clean.sh       # clean venv and caches
```

Quick Start (Windows PowerShell):

```powershell
.\setup.ps1
& .\.venv\Scripts\Activate.ps1
.\run.ps1
.\test.ps1
.\clean.ps1
```

Docker (build & run):

```bash
docker build -t user-display-optimizer .
docker run --rm user-display-optimizer    # Runs tests then default run
```

Performance expectations:

| Operation | Target |
|-----------|--------|
| Display 100 users | <50ms |
| Display 1000 users | <100ms |
| Filter 100 users | <10ms |
| Get user by ID | <1ms |

Notes:
- The optimized version uses `UserDisplay` which builds a mapping for O(1) lookup by ID and uses list-building + join to avoid repeated string concatenation.
- All functions include safe getters to prevent KeyError and use logging markers `[MARKER]` for searchability.

Contributing:
- Use `pytest` to run tests. This repository is intended to be cross-platform; use the appropriate script for your OS.
