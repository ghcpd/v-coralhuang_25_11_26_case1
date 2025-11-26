# User Display Optimizer

Quick-refactor project to optimize user display utilities. This repository contains a preserved original implementation and an optimized, tested replacement with cross-platform scripts and Docker support.

## Quick start (Unix / macOS / Linux)

```bash
# Setup once
bash setup.sh

# Run demo
bash run.sh

# Run tests
bash test.sh

# Clean
bash clean.sh
```

## Quick start (Windows PowerShell)

```powershell
# Setup once
powershell -File setup.ps1

# Run demo
powershell -File run.ps1

# Run tests
powershell -File test.ps1

# Clean
powershell -File clean.ps1
```

## Docker

Build image:

```bash
docker build -t user-display-optimizer .
```

Run tests inside container:

```bash
docker run --rm user-display-optimizer bash -lc "pytest -q --maxfail=1 --disable-warnings --cov=user_display_optimized"
```

Run demo (container):

```bash
docker run --rm user-display-optimizer bash run.sh
```

## Files of interest

- `user_display_original.py` — preserved original
- `user_display_optimized.py` — optimized implementation (type hints, logging, index, safe handling)
- `tests/` — pytest test-suite (includes performance checks)
- `setup.sh` / `setup.ps1` — idempotent environment setup
- `run.sh` / `run.ps1` — run demo
- `test.sh` / `test.ps1` — run tests with coverage
