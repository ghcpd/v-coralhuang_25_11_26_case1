"""Optimized user display module.

This module aims to improve performance and maintainability of the original
`user_display_current.py` by introducing type hints, logging, efficient
string handling, index-based lookups, and robust error handling.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence
import logging
import time

logger = logging.getLogger(__name__)

__all__ = [
    "display_users",
    "get_user_by_id",
    "filter_users",
    "export_users_to_string",
    "build_user_index",
]


def _safe_get(user: Dict[str, Any], key: str, default: str = "<unknown>") -> Any:
    """Helper to safely retrieve a key from a user dict.

    Logs a marker when a key is missing and returns a default value.
    """
    if key not in user:
        logger.warning("[MARKER][MISSING_KEY] Missing key '%s' for user id=%s", key, user.get("id"))
        return default
    return user[key]


def build_user_index(users: Sequence[Dict[str, Any]]) -> Dict[Any, Dict[str, Any]]:
    """Build a dictionary index mapping user id to user object.

    O(n) to build once, then O(1) lookups for get_user_by_id() operations.
    """
    return {user.get("id"): user for user in users if "id" in user}


def display_users(users: Sequence[Dict[str, Any]], show_all: bool = True, verbose: bool = False) -> str:
    """Format and return a multi-line string describing user records.

    Improvements:
    - Uses list append + join for efficient string building
    - Removes artificial sleep calls
    - Safe access via helper to avoid KeyError
    - Logging with markers
    """
    start = time.perf_counter()

    if not isinstance(users, Sequence):
        logger.error("[MARKER][INVALID_INPUT] users must be a sequence")
        raise TypeError("users must be a sequence of user dictionaries")

    lines: List[str] = []
    processed_count = 0

    for user in users:
        if verbose:
            logger.info("[MARKER][VERBOSE] Processing user id=%s", user.get("id"))

        # Safely get values to avoid KeyError
        user_id = _safe_get(user, "id")
        user_name = _safe_get(user, "name")
        user_email = _safe_get(user, "email")
        user_role = _safe_get(user, "role")
        user_status = _safe_get(user, "status")
        user_join = _safe_get(user, "join_date")
        user_login = _safe_get(user, "last_login")

        line = (
            f"ID:{user_id}|Name:{user_name}|Email:{user_email}|Role:{user_role}|"
            f"Status:{user_status}|JoinDate:{user_join}|LastLogin:{user_login}"
        )
        lines.append(line)
        processed_count += 1

    if show_all:
        lines.append("")
        lines.append(f"[INFO] Processed {processed_count} users.")

    result = "\n".join(lines)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info("[MARKER][PERF] display_users processed=%d time_ms=%.2f", processed_count, duration_ms)
    return result


def get_user_by_id(users: Sequence[Dict[str, Any]], user_id: Any, index: Optional[Dict[Any, Dict[str, Any]]] = None) -> Optional[Dict[str, Any]]:
    """Return a user by ID.

    If an index is provided (dict of id->user), lookup is O(1). If not,
    the function will build an index for performance on repeated calls.
    """
    if index is not None:
        return index.get(user_id)

    # Fallback: build index and lookup
    idx = build_user_index(users)
    return idx.get(user_id)


def filter_users(users: Sequence[Dict[str, Any]], criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Filter users by criteria.

    Supported criteria keys: 'role', 'status', 'name'.
    - 'name' does a case-insensitive substring match.
    """
    if criteria is None or not criteria:
        return list(users)

    role = criteria.get("role")
    status = criteria.get("status")
    name = criteria.get("name")

    # Use list comprehension for maintainability and speed
    def matches(user: Dict[str, Any]) -> bool:
        if role and _safe_get(user, "role") != role:
            return False
        if status and _safe_get(user, "status") != status:
            return False
        if name and name.lower() not in str(_safe_get(user, "name")).lower():
            return False
        return True

    return [user for user in users if matches(user)]


def export_users_to_string(users: Sequence[Dict[str, Any]]) -> str:
    """Export users to a readable, memory-efficient string.

    Uses list append + join and avoids temporary concatenation.
    """
    header = "USER_EXPORT_START"
    sep = "=" * 100
    footer = "USER_EXPORT_END"

    parts: List[str] = [header, sep]

    for user in users:
        uid = _safe_get(user, "id")
        parts.append(f"User ID: {uid}")
        parts.append(f"  Name: {_safe_get(user, 'name')}")
        parts.append(f"  Email: {_safe_get(user, 'email')}")
        parts.append(f"  Role: {_safe_get(user, 'role')}")
        parts.append(f"  Status: {_safe_get(user, 'status')}")
        parts.append(f"  Join Date: {_safe_get(user, 'join_date')}")
        parts.append(f"  Last Login: {_safe_get(user, 'last_login')}")
        parts.append("-" * 100)

    parts.append(footer)
    return "\n".join(parts)


if __name__ == "__main__":
    # Simple CLI for manual timing and inspection
    logging.basicConfig(level=logging.INFO)
    # Create 100 sample users for demonstration and performance timing
    users = [
        {
            "id": i,
            "name": f"User {i}",
            "email": f"user{i}@example.com",
            "role": "User" if i % 3 else "Admin",
            "status": "Active" if i % 5 else "Inactive",
            "join_date": "2023-01-01",
            "last_login": "2025-11-26",
        }
        for i in range(1, 101)
    ]

    start = time.perf_counter()
    out = display_users(users)
    elapsed = (time.perf_counter() - start) * 1000.0
    print(out[:1000])  # Print a slice so output doesn't blow up
    print(f"Elapsed display_users (ms): {elapsed:.2f}")

    idx = build_user_index(users)
    uid = users[10]["id"]
    start = time.perf_counter()
    user = get_user_by_id(users, uid, index=idx)
    elapsed = (time.perf_counter() - start) * 1000.0
    print("Lookup result:", user)
    print(f"Elapsed lookup (ms): {elapsed:.4f}")
