# User Display Optimizer

This repository refactors and optimizes a simple user display module to be
faster, more maintainable, and cross-platform.

## Quick Start

On macOS / Linux:

```bash
# Create venv and install deps
bash setup.sh

# Run the optimized module
bash run.sh

# Run tests
bash test.sh

# Clean environment
bash clean.sh
```

On Windows PowerShell:

```powershell
# Create venv and install deps
powershell -File setup.ps1

# Run the optimized module
powershell -File run.ps1

# Run tests
powershell -File test.ps1

# Clean environment
powershell -File clean.ps1
```

## Before / After

The original (reference) implementation is in `user_display_original.py` and the
optimized implementation is in `user_display_optimized.py`.

Key improvements:
- Uses list append + join instead of repeated string concatenation
- Removes artificial delays
- Adds logging and safe key retrieval
- Index-based lookups for O(1) get-by-id
- Cleaner filter logic using list comprehensions
- Type hints and docstrings

## Docker

Build and run in a container (requires Docker):

```bash
docker build -t user-display-optimizer .
docker run --rm user-display-optimizer
``` 

To run the CLI in container:

```bash
docker run --rm user-display-optimizer bash run.sh
```

## Tests

The test suite uses `pytest` and `pytest-cov` and verifies:
- Functionality and formatting
- Error handling for missing keys
- Performance targets

## Notes

- The project aims to be cross-platform and uses only standard Python tooling.
- The scripts are idempotent and safe to run multiple times.
