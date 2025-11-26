# User Display Optimizer

Fast, maintainable user display utilities with cross-platform one-click scripts and Docker support.

## Quick Start

### Bash (Linux/macOS/WSL)
```bash
bash setup.sh      # create .venv and install deps
bash run.sh        # run optimized module (see --help)
bash test.sh       # pytest + coverage
bash clean.sh      # remove venv/artifacts
```

### PowerShell (Windows)
```powershell
powershell -File setup.ps1
powershell -File run.ps1 --count 10
powershell -File test.ps1
powershell -File clean.ps1
```

### Docker
```bash
docker build -t user-display-optimizer .
docker run --rm user-display-optimizer                    # runs tests
docker run --rm user-display-optimizer bash run.sh --count 20
```

## Before vs After

| Aspect | Original (`user_display_original.py`) | Optimized (`user_display_optimized.py`) |
|--------|----------------------------------------|-----------------------------------------|
| String building | `+=` in loop (O(n²)) | list accumulation + `"\n".join` (O(n)) |
| Delays | `time.sleep(0.01)` per user | No artificial delays |
| Lookup | Linear search | Indexed lookups (`build_user_index`) |
| Filtering | Nested `if` | Clean comprehension with handling |
| Error handling | None (KeyError) | Graceful logging + `"N/A"` placeholder |
| Logging | `print` | `logging` with `[USER_DISPLAY]` marker |
| Type hints | None | Comprehensive typing, dataclass helper |
| Tests | None | Pytest + coverage (>85%) |
| Cross-platform | Not provided | Bash + PowerShell scripts, Docker |

## Modules

- `user_display_original.py`: Unmodified reference implementation.
- `user_display_optimized.py`: Refactored, typed, logged, and efficient.

## Key Functions (Optimized)

- `display_users(users, show_all=True, verbose=False, fields=DEFAULT_FIELDS) -> str`
- `build_user_index(users, key="id") -> dict`
- `get_user_by_id(users_or_index, user_id, prebuilt_index=None) -> Optional[Mapping]`
- `filter_users(users, criteria) -> list`
- `export_users_to_string(users) -> str`
- `generate_dummy_users(n) -> list`

Run `python user_display_optimized.py --help` for CLI flags (JSON output, counts, verbosity).

## Performance Targets

- Display 100 users < 50 ms
- Display 1000 users < 100 ms
- Filter 100 users < 10 ms
- Indexed lookup avg < 1 ms

> Verified via pytest performance tests (see `tests/test_user_display.py`).

## Project Structure
```
.
├── user_display_original.py
├── user_display_optimized.py
├── requirements.txt
├── setup.sh / setup.ps1
├── run.sh / run.ps1
├── test.sh / test.ps1
├── clean.sh / clean.ps1
├── Dockerfile / .dockerignore
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_user_display.py
```

## Notes
- Python 3.10+ required.
- Scripts are idempotent; rerunning `setup` is safe.
- Logging uses marker `[USER_DISPLAY]` for easy filtering.
