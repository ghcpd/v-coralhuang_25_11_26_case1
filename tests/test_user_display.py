import time
import re
from typing import Dict

import pytest

from user_display_optimized import UserDisplay, time_display


def test_display_users_basic(sample_users: list[Dict]):
    ud = UserDisplay(sample_users)
    out = ud.display_users(show_all=True)
    assert "ID:1|Name:John Doe" in out
    assert "[INFO] Processed 2 users" in out


def test_display_users_missing_keys():
    users = [{"id": 1}, {"id": 2, "name": "Has Name"}]
    ud = UserDisplay(users)
    out = ud.display_users()
    # Missing keys should result in 'N/A' placeholders
    assert "N/A" in out


def test_get_user_by_id_index(sample_users):
    ud = UserDisplay(sample_users)
    u = ud.get_user_by_id(1)
    assert u and u.get("name") == "John Doe"
    none = ud.get_user_by_id(9999)
    assert none is None


def test_get_user_by_id_no_index(sample_users):
    ud = UserDisplay(sample_users, build_index=False)
    # The fallback linear search should still work
    assert ud.get_user_by_id(2)["email"] == "jane@example.com"


def test_filter_users(sample_users):
    ud = UserDisplay(sample_users)
    filtered = ud.filter_users({"role": "User"})
    assert len(filtered) == 1
    filtered = ud.filter_users({"name": "Jane"})
    assert len(filtered) == 1


def test_export_users_to_string(sample_users):
    ud = UserDisplay(sample_users)
    s = ud.export_users_to_string()
    assert s.startswith("USER_EXPORT_START")
    assert "User ID: 1" in s
    assert "USER_EXPORT_END" in s


def test_error_handling_types():
    with pytest.raises(TypeError):
        UserDisplay("not-a-list")


def test_logging_markers(caplog, sample_users):
    caplog.set_level("DEBUG")
    ud = UserDisplay([{"id": 1}], build_index=True)
    ud.display_users(verbose=True)
    assert any("[MARKER]" in rec.getMessage() for rec in caplog.records)


def test_performance_many_users(many_users):
    # 100 users < 50ms, 1000 users < 100ms
    users_100 = many_users[:100]
    users_1000 = many_users[:1000]
    t100 = time_display(users_100)
    t1000 = time_display(users_1000)
    # Add broad guard for real-world variance; tests can be adjusted
    assert t100 < 50.0
    assert t1000 < 100.0
