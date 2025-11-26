"""Optimized user display utilities.

Goals:
- Fast string building
- Type hints and docstrings
- Graceful error handling and logging
- O(1) lookup for user by ID
- Simplified filter logic
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence
import logging
import time

logger = logging.getLogger(__name__)
if not logging.getLogger().handlers:
    # Configure default handler for standalone runs
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s [%(name)s] %(message)s"))
    logging.getLogger().addHandler(handler)
logger.setLevel(logging.INFO)


def _safe_get(user: Dict[str, Any], key: str, default: str = "N/A") -> Any:
    """Safely get value from user dict and log missing keys.

    Returns a default value if the key does not exist and logs at DEBUG level.
    """
    if key not in user:
        logger.debug("[MARKER] Missing key '%s' for user id=%s; using default=%s", key, user.get("id"), default)
        return default
    return user.get(key, default)


@dataclass
class UserDisplay:
    users: List[Dict[str, Any]]
    build_index: bool = True

    def __post_init__(self):
        if not isinstance(self.users, list):
            raise TypeError("users must be a list of dictionaries")
        self._index: Optional[Dict[Any, Dict[str, Any]]] = None
        if self.build_index:
            self._index = {u.get("id"): u for u in self.users if "id" in u}

    def display_users(self, show_all: bool = True, verbose: bool = False) -> str:
        """Return a compact, formatted string for the provided users.

        This method uses list-building and single join() to avoid repeated string concats.
        """
        start = time.perf_counter()
        if not isinstance(self.users, list):
            logger.error("[MARKER] display_users: users must be a list")
            raise TypeError("users must be a list")

        lines: List[str] = []
        processed_count = 0

        for user in self.users:
            # verbose debug logging
            if verbose:
                logger.info("[MARKER] Processing user %s", user.get("id"))

            uid = _safe_get(user, "id")
            name = _safe_get(user, "name")
            email = _safe_get(user, "email")
            role = _safe_get(user, "role")
            status = _safe_get(user, "status")
            join = _safe_get(user, "join_date")
            login = _safe_get(user, "last_login")

            line = f"ID:{uid}|Name:{name}|Email:{email}|Role:{role}|Status:{status}|JoinDate:{join}|LastLogin:{login}"
            lines.append(line)
            processed_count += 1

        if show_all:
            lines.append(f"\n[INFO] Processed {processed_count} users.")

        elapsed = (time.perf_counter() - start) * 1000.0
        logger.debug("[MARKER] display_users completed in %.3f ms", elapsed)
        return "\n".join(lines)

    def get_user_by_id(self, user_id: Any) -> Optional[Dict[str, Any]]:
        """Return a user by id in O(1) time if index is built.

        Falls back to linear search if index isn't available.
        """
        if self._index is not None:
            return self._index.get(user_id)
        logger.debug("[MARKER] Index not built; falling back to linear search")
        for user in self.users:
            if user.get("id") == user_id:
                return user
        return None

    def filter_users(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter users by criteria. criteria keys can include 'role', 'status', 'name'.

        Name searches are case-insensitive and support substring match.
        """
        if not criteria:
            return self.users.copy()

        def matches(user: Dict[str, Any]) -> bool:
            for key, value in criteria.items():
                if key == "name":
                    name_val = _safe_get(user, "name", "").lower()
                    if not (isinstance(value, str) and value.lower() in name_val):
                        return False
                else:
                    if _safe_get(user, key, None) != value:
                        return False
            return True

        return [u for u in self.users if matches(u)]

    def export_users_to_string(self) -> str:
        """Export user list as a multi-line string using join for memory efficiency.
        """
        lines: List[str] = ["USER_EXPORT_START", "=" * 100]
        for user in self.users:
            uid = _safe_get(user, "id")
            name = _safe_get(user, "name")
            email = _safe_get(user, "email")
            role = _safe_get(user, "role")
            status = _safe_get(user, "status")
            join = _safe_get(user, "join_date")
            login = _safe_get(user, "last_login")

            lines.extend([
                f"User ID: {uid}",
                f"  Name: {name}",
                f"  Email: {email}",
                f"  Role: {role}",
                f"  Status: {status}",
                f"  Join Date: {join}",
                f"  Last Login: {login}",
                "-" * 100,
            ])
        lines.append("USER_EXPORT_END")
        return "\n".join(lines)


def time_display(users: Sequence[Dict[str, Any]], build_index: bool = True) -> float:
    """Utility to time display_users with a given list.

    Returns elapsed milliseconds.
    """
    ud = UserDisplay(list(users), build_index=build_index)
    start = time.perf_counter()
    ud.display_users(show_all=False, verbose=False)
    elapsed = (time.perf_counter() - start) * 1000.0
    logger.debug("[MARKER] time_display: %.3f ms for %d users", elapsed, len(users))
    return elapsed


if __name__ == "__main__":
    # Minor runner for quick local testing
    sample_users = [
        {"id": i, "name": f"User {i}", "email": f"user{i}@example.com", "role": "User", "status": "Active", "join_date": "2024-01-01", "last_login": "2025-11-26"}
        for i in range(1, 101)
    ]

    ud = UserDisplay(sample_users)
    logger.info("Running display_users for 100 users")
    t = time_display(sample_users)
    print(ud.display_users(show_all=True))
    logger.info("Completed in %.3f ms", t)
