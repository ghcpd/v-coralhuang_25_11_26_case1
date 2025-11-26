"""Optimized and safer user display utilities.

Improvements over original:
- Efficient string building (list + join)
- No artificial delays
- Type hints and docstrings
- Graceful handling of missing keys using defaults
- Logging with `[MARKER]` tags
- O(1) lookup by building an index
- Cleaner, testable functions
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence
import logging
import time

LOG_MARKER = "[USER-DISPLAY]"

logger = logging.getLogger("user_display_optimized")
handler = logging.StreamHandler()
formatter = logging.Formatter(f"%(asctime)s %(levelname)s {LOG_MARKER} %(message)s")
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


def display_users(users: Sequence[Mapping[str, Any]], show_all: bool = True, verbose: bool = False) -> str:
    """Return a compact, readable string listing users.

    This function is optimized for large lists: it uses list accumulation and
    str.join() instead of repeated concatenation. Missing keys are handled
    gracefully and logged at DEBUG level.

    Args:
        users: sequence of user-like mappings (must include 'id', 'name', etc.)
        show_all: whether to append a summary footer
        verbose: whether to log a per-user processing message

    Returns:
        A string containing the formatted user lines.
    """
    out_lines: List[str] = []
    processed_count = 0

    for user in users:
        processed_count += 1
        # Use .get to avoid KeyError and provide placeholder
        try:
            uid = user.get('id', '<missing>')
            name = user.get('name', '<missing>')
            email = user.get('email', '<missing>')
            role = user.get('role', '<missing>')
            status = user.get('status', '<missing>')
            join_date = user.get('join_date', '<missing>')
            last_login = user.get('last_login', '<missing>')
        except Exception as exc:  # pragma: no cover - defensive
            logger.exception("Unexpected error reading user mapping: %r", exc)
            uid = '<error>'
            name = email = role = status = join_date = last_login = '<error>'

        if verbose:
            logger.debug("Processing user %s", uid)

        # Build a single, compact line
        out_lines.append(
            f"ID:{uid} | Name:{name} | Email:{email} | Role:{role} | Status:{status} | JoinDate:{join_date} | LastLogin:{last_login}"
        )

    if show_all:
        out_lines.append(f"\n[INFO] Processed {processed_count} users.")

    return "\n".join(out_lines)


def build_user_index(users: Iterable[Mapping[str, Any]]) -> Dict[Any, Mapping[str, Any]]:
    """Return a dict mapping user IDs to user mapping for O(1) lookup.

    If multiple users share the same id, the last one encountered wins.
    """
    index: Dict[Any, Mapping[str, Any]] = {}
    for u in users:
        # ignore users that don't have an id key
        if not isinstance(u, Mapping):
            logger.debug("Skipping non-mapping user: %r", u)
            continue
        if 'id' in u:
            index[u['id']] = u
        else:
            logger.debug("User has no id, skipping: %r", u)
    return index


def get_user_by_id(users: Iterable[Mapping[str, Any]], user_id: Any, *, index: Optional[Mapping[Any, Mapping[str, Any]]] = None) -> Optional[Mapping[str, Any]]:
    """Return the user mapping for `user_id`.

    This function uses the provided `index` (if given) for O(1) lookup, otherwise
    it will fall back to building an index internally (still efficient for many
    lookups).
    """
    if index is not None:
        logger.debug("Looking up user_id %r using provided index", user_id)
        return index.get(user_id)

    logger.debug("Building internal index to look up user_id %r", user_id)
    idx = build_user_index(users)
    return idx.get(user_id)


def filter_users(users: Iterable[Mapping[str, Any]], criteria: Mapping[str, Any]) -> List[Mapping[str, Any]]:
    """Filter users by a criteria mapping.

    Supported keys in `criteria`:
      - role: exact match
      - status: exact match
      - name: substring case-insensitive match

    Any unknown criteria keys are ignored (allowing forward compatibility).
    """
    role = criteria.get('role')
    status = criteria.get('status')
    name = criteria.get('name')

    def matches(u: Mapping[str, Any]) -> bool:
        try:
            if role is not None and u.get('role') != role:
                return False
            if status is not None and u.get('status') != status:
                return False
            if name is not None and name.lower() not in (u.get('name') or '').lower():
                return False
            return True
        except Exception:
            logger.debug("Skipping user during filtering due to unexpected shape: %r", u)
            return False

    return [u for u in users if matches(u)]


def export_users_to_string(users: Sequence[Mapping[str, Any]]) -> str:
    """Export users into a human readable multi-line string efficiently.

    Avoids creating many temporary strings and uses a list + join approach.
    """
    lines: List[str] = ["USER_EXPORT_START", "=" * 100]

    for u in users:
        uid = u.get('id', '<missing>')
        lines.append(f"User ID: {uid}")
        lines.append(f"  Name: {u.get('name', '<missing>')}")
        lines.append(f"  Email: {u.get('email', '<missing>')}")
        lines.append(f"  Role: {u.get('role', '<missing>')}")
        lines.append(f"  Status: {u.get('status', '<missing>')}")
        lines.append(f"  Join Date: {u.get('join_date', '<missing>')}")
        lines.append(f"  Last Login: {u.get('last_login', '<missing>')}")
        lines.append("-" * 100)

    lines.append("USER_EXPORT_END")
    return "\n".join(lines)


# Minimal sample dataset for manual runs
sample_users = [
    {
        'id': 1,
        'name': 'John Doe',
        'email': 'john@example.com',
        'role': 'Admin',
        'status': 'Active',
        'join_date': '2023-01-15',
        'last_login': '2025-11-26'
    },
    {
        'id': 2,
        'name': 'Jane Smith',
        'email': 'jane@example.com',
        'role': 'User',
        'status': 'Inactive',
        'join_date': '2023-06-20',
        'last_login': '2025-11-20'
    },
]


if __name__ == '__main__':
    # Basic demonstration and timing for quick feedback
    logger.info("Running demo of optimized functions")
    start = time.perf_counter()
    out = display_users(sample_users)
    elapsed = (time.perf_counter() - start) * 1000
    logger.info("display_users executed in %.2f ms", elapsed)
    print(out)
