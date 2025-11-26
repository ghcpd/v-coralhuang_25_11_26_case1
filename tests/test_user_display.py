"""Tests for user_display_optimized.py"""

import logging
import time
from typing import Any

import pytest

from user_display_optimized import (
    build_user_index,
    display_users,
    export_users_to_string,
    filter_users,
    get_user_by_id,
)


def test_display_empty_list():
    out = display_users([])
    assert "Processed 0 users" in out or "Processed 0" in out


def test_display_missing_keys_and_logging(caplog):
    caplog.set_level(logging.WARNING)

    users = [{"id": 1, "email": "no_name@example.com"}]
    out = display_users(users)
    assert "<unknown>" in out
    assert any("[MARKER][MISSING_KEY]" in rec.message for rec in caplog.records)


def test_get_user_by_id_with_index_and_without(sample_users):
    index = build_user_index(sample_users)
    u = get_user_by_id(sample_users, 2, index=index)
    assert u["name"] == "Jane Smith"

    u2 = get_user_by_id(sample_users, 999)
    assert u2 is None


def test_filter_users_single_and_multiple(sample_users):
    # Role filter
    res = filter_users(sample_users, {"role": "User"})
    assert all(r["role"] == "User" for r in res)

    # Name filter (case-insensitive)
    res = filter_users(sample_users, {"name": "john"})
    assert all("john" in r["name"].lower() for r in res)

    # Combined
    res = filter_users(sample_users, {"role": "Admin", "status": "Active"})
    assert all(r["role"] == "Admin" and r["status"] == "Active" for r in res)


def test_export_users_to_string_format(sample_users):
    out = export_users_to_string(sample_users)
    assert out.startswith("USER_EXPORT_START")
    assert out.strip().endswith("USER_EXPORT_END")
    assert "User ID: 1" in out


def test_performance_display_100(gen_users):
    users = gen_users(100)
    start = time.perf_counter()
    _ = display_users(users)
    elapsed = (time.perf_counter() - start) * 1000
    assert elapsed < 50, f"display_users(100) too slow: {elapsed:.2f}ms"


def test_performance_display_1000(gen_users):
    users = gen_users(1000)
    start = time.perf_counter()
    _ = display_users(users)
    elapsed = (time.perf_counter() - start) * 1000
    assert elapsed < 100, f"display_users(1000) too slow: {elapsed:.2f}ms"


def test_get_user_by_id_lookup_perf(gen_users):
    users = gen_users(1000)
    idx = build_user_index(users)
    start = time.perf_counter()
    u = get_user_by_id(users, 800, index=idx)
    elapsed = (time.perf_counter() - start) * 1000
    assert u is not None
    assert elapsed < 1.0, f"id lookup too slow: {elapsed:.4f}ms"


def test_filter_performance(gen_users):
    users = gen_users(100)
    start = time.perf_counter()
    _ = filter_users(users, {"status": "Active"})
    elapsed = (time.perf_counter() - start) * 1000
    assert elapsed < 10, f"filter_users(100) too slow: {elapsed:.2f}ms"


def test_display_invalid_input_raises(caplog):
    caplog.set_level(logging.ERROR)
    with pytest.raises(TypeError):
        display_users(None)  # type: ignore[arg-type]
    assert any('[MARKER][INVALID_INPUT]' in rec.message for rec in caplog.records)


def test_display_verbose_logging(sample_users, caplog):
    caplog.set_level(logging.INFO)
    display_users(sample_users, verbose=True)
    assert any('[MARKER][VERBOSE]' in rec.message for rec in caplog.records)


def test_get_user_by_id_no_index(sample_users):
    u = get_user_by_id(sample_users, 3)
    assert u is not None and u['id'] == 3


def test_filter_users_none_criteria_returns_list(sample_users):
    assert filter_users(sample_users, None) == sample_users


def test_build_user_index_and_lookup(gen_users):
    users = gen_users(10)
    idx = build_user_index(users)
    assert idx[5]['id'] == 5


def test_run_as_module_executes_main(monkeypatch, capsys):
    # Run module as __main__ to hit main code for coverage; capture prints
    import runpy

    runpy.run_module('user_display_optimized', run_name='__main__')
    # If it runs without raising errors, assume OK
    captured = capsys.readouterr()
    assert 'Elapsed display_users' in captured.out
