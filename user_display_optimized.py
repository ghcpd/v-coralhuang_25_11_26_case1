"""Optimized user display and utilities.

This module provides efficient, readable, and testable helpers for user display,
filtering, indexing, and export. It is cross-platform friendly and avoids
unnecessary delays or quadratic string concatenation.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from dataclasses import dataclass, asdict
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Union

logger = logging.getLogger(__name__)
MARKER = "[USER_DISPLAY]"

# Default user field order
DEFAULT_FIELDS: Sequence[str] = (
    "id",
    "name",
    "email",
    "role",
    "status",
    "join_date",
    "last_login",
)


@dataclass(frozen=True)
class User:
    """Lightweight user data container.

    The optimized utilities operate on any mapping-like object; this dataclass is
    provided for convenience and type safety in tests and examples.
    """

    id: Any
    name: str
    email: str
    role: str
    status: str
    join_date: str
    last_login: str

    def to_mapping(self) -> Dict[str, Any]:
        return asdict(self)


def _safe_get(user: Mapping[str, Any], key: str) -> Any:
    """Retrieve a key from a user mapping, logging if missing.

    Missing keys return "N/A" while emitting a warning marker. This keeps
    display/export resilient without raising exceptions.
    """

    if key in user:
        return user[key]
    logger.warning("%s missing key '%s' in user %s", MARKER, key, user)
    return "N/A"


def display_users(
    users: Iterable[Mapping[str, Any]],
    *,
    show_all: bool = True,
    verbose: bool = False,
    fields: Sequence[str] = DEFAULT_FIELDS,
    prefix: str = "ID",
) -> str:
    """Render users in a compact, readable format.

    - Uses list accumulation + join for O(n) string building.
    - Handles missing keys gracefully (logs warnings, substitutes "N/A").
    - Optional verbose tracing for debug.
    """

    lines: List[str] = []
    count = 0

    for user in users:
        if verbose:
            logger.info("%s processing user %s", MARKER, _safe_get(user, "id"))
        parts = [f"{field.capitalize()}:{_safe_get(user, field)}" for field in fields]
        lines.append(" | ".join(parts))
        count += 1

    if show_all:
        lines.append("")
        lines.append(f"{MARKER} Processed {count} users.")

    return "\n".join(lines) + ("\n" if lines else "")


def build_user_index(
    users: Iterable[Mapping[str, Any]],
    key: str = "id",
) -> Dict[Any, Mapping[str, Any]]:
    """Build an index mapping `key` to user mapping; logs duplicates and keeps first.

    Returns a dictionary for O(1) lookup by the chosen key.
    """

    index: Dict[Any, Mapping[str, Any]] = {}
    for user in users:
        if key in user:
            user_id = user[key]
            if user_id in index:
                logger.warning("%s duplicate %s '%s' encountered; keeping first", MARKER, key, user_id)
                continue
            index[user_id] = user
        else:
            logger.warning("%s missing key '%s' during index build: %s", MARKER, key, user)
    return index


def get_user_by_id(
    users_or_index: Union[Sequence[Mapping[str, Any]], Mapping[Any, Mapping[str, Any]]],
    user_id: Any,
    *,
    prebuilt_index: Optional[Mapping[Any, Mapping[str, Any]]] = None,
) -> Optional[Mapping[str, Any]]:
    """Retrieve a user by id using O(1) indexed lookup when possible.

    Accepts either a sequence of user mappings or a pre-built index. If both a
    sequence and `prebuilt_index` are provided, the prebuilt index is used.
    """

    # If a mapping is passed (likely already an index), try direct lookup
    if isinstance(users_or_index, Mapping):
        return users_or_index.get(user_id)

    if prebuilt_index is not None:
        return prebuilt_index.get(user_id)

    # Fallback: build a temporary index (O(n))
    idx = build_user_index(users_or_index)
    return idx.get(user_id)


def filter_users(
    users: Iterable[Mapping[str, Any]],
    criteria: Mapping[str, Any],
) -> List[Mapping[str, Any]]:
    """Filter users by arbitrary criteria with readable logic.

    Special handling:
    - `name`: case-insensitive substring match
    - Other keys: equality
    Missing keys return False (user excluded) with a logged warning.
    """

    def match(user: Mapping[str, Any]) -> bool:
        for key, expected in criteria.items():
            if key == "name":
                value = _safe_get(user, key)
                if value == "N/A":
                    return False
                if str(expected).lower() not in str(value).lower():
                    return False
            else:
                value = _safe_get(user, key)
                if value != expected:
                    return False
        return True

    return [user for user in users if match(user)]


def export_users_to_string(users: Iterable[Mapping[str, Any]]) -> str:
    """Export users to a formatted string efficiently.

    Uses list accumulation and join to avoid excessive temporaries.
    """

    lines: List[str] = ["USER_EXPORT_START", "=" * 100]
    for user in users:
        lines.extend(
            [
                f"User ID: {_safe_get(user, 'id')}",
                f"  Name: {_safe_get(user, 'name')}",
                f"  Email: {_safe_get(user, 'email')}",
                f"  Role: {_safe_get(user, 'role')}",
                f"  Status: {_safe_get(user, 'status')}",
                f"  Join Date: {_safe_get(user, 'join_date')}",
                f"  Last Login: {_safe_get(user, 'last_login')}",
                "-" * 100,
            ]
        )
    lines.append("USER_EXPORT_END")
    return "\n".join(lines) + "\n"


# Sample data for manual runs
SAMPLE_USERS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "role": "Admin",
        "status": "Active",
        "join_date": "2023-01-15",
        "last_login": "2025-11-26",
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "email": "jane@example.com",
        "role": "User",
        "status": "Inactive",
        "join_date": "2023-06-20",
        "last_login": "2025-11-20",
    },
]


def generate_dummy_users(n: int) -> List[Dict[str, Any]]:
    """Generate `n` lightweight dummy users for performance testing."""
    base = SAMPLE_USERS[0]
    users: List[Dict[str, Any]] = []
    for i in range(n):
        users.append(
            {
                "id": i,
                "name": f"User {i}",
                "email": f"user{i}@example.com",
                "role": "User" if i % 5 else "Admin",
                "status": "Active" if i % 3 else "Inactive",
                "join_date": "2024-01-01",
                "last_login": "2025-11-26",
            }
        )
    return users


def configure_logging(level: int = logging.INFO) -> None:
    """Configure basic logging if not already configured."""
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=level,
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        )


def _cli(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Optimized user display demo")
    parser.add_argument("--count", type=int, default=5, help="Number of dummy users to generate")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of formatted text")
    parser.add_argument("--no-summary", dest="show_all", action="store_false", help="Omit summary line")
    args = parser.parse_args(argv)

    configure_logging(logging.DEBUG if args.verbose else logging.INFO)

    users = generate_dummy_users(args.count)

    start = time.perf_counter()
    if args.json:
        data = json.dumps(users)
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info("%s rendered %s users to JSON in %.2f ms", MARKER, len(users), duration_ms)
        print(data)
    else:
        output = display_users(users, show_all=args.show_all, verbose=args.verbose)
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info("%s rendered %s users in %.2f ms", MARKER, len(users), duration_ms)
        print(output)

    return 0


if __name__ == "__main__":  # pragma: no cover - manual entrypoint
    sys.exit(_cli())
