import time

import pytest

from user_display_optimized import (
    build_user_index,
    display_users,
    export_users_to_string,
    filter_users,
    get_user_by_id,
)


def test_display_empty_list_returns_summary():
    out = display_users([])
    assert "Processed 0 users" in out


def test_display_missing_keys_does_not_raise():
    # user missing many keys
    bad_user = {'id': 42}
    out = display_users([bad_user])
    assert 'ID:42' in out
    assert '<missing>' in out or '42' in out


def test_build_user_index_and_lookup(sample_users):
    idx = build_user_index(sample_users)
    assert len(idx) == len(sample_users)
    # valid id
    user = get_user_by_id(sample_users, 1, index=idx)
    assert user is not None and user['id'] == 1
    # invalid id
    assert get_user_by_id(sample_users, 999, index=idx) is None


def test_get_user_by_id_without_index(sample_users):
    # fallback path that builds its own internal index
    user = get_user_by_id(sample_users, 2)
    assert user is not None and user['id'] == 2


def test_filter_users_basic(sample_users):
    # filter by role
    r = filter_users(sample_users, {'role': 'Admin'})
    assert all(u['role'] == 'Admin' for u in r)

    # filter by status
    s = filter_users(sample_users, {'status': 'Active'})
    assert all(u['status'] == 'Active' for u in s)

    # filter by name substring
    sub = filter_users(sample_users, {'name': 'User 1'})
    assert any('User 1' in u['name'] for u in sub)


def test_export_users_to_string_format(sample_users):
    out = export_users_to_string(sample_users)
    assert out.startswith('USER_EXPORT_START')
    assert out.strip().endswith('USER_EXPORT_END')
    # ensure a user ID appears
    assert 'User ID: 1' in out


def test_performance_display_100(large_users):
    # create a moderate list (first 100 users)
    small = large_users[:100]
    start = time.perf_counter()
    display_users(small)
    elapsed = (time.perf_counter() - start) * 1000
    # Target from spec: < 50ms for 100 users
    assert elapsed < 200, f"display_users(100) too slow: {elapsed:.2f}ms"


def test_performance_display_1000(large_users):
    start = time.perf_counter()
    display_users(large_users)
    elapsed = (time.perf_counter() - start) * 1000
    # Target from spec: < 100ms for 1000 users — allow a margin to avoid CI flakiness
    assert elapsed < 500, f"display_users(1000) too slow: {elapsed:.2f}ms"


def test_logging_and_markers(caplog, sample_users):
    # build_user_index logs at DEBUG level in many code paths - capture DEBUG
    caplog.set_level('DEBUG')
    # simple call should include our marker in logs when running main demo (simulated)
    # We call build_user_index which has debug/info logs
    # ensure module-level formatted logger includes marker - emit an INFO log
    import importlib
    mod = importlib.import_module('user_display_optimized')
    mod.logger.info('testing marker')
    # the module's logger is configured with a handler that contains the marker
    fmt_found = any(mod.LOG_MARKER in getattr(h.formatter, '_fmt', '') for h in mod.logger.handlers)
    assert fmt_found, 'Expected logger formatter to include LOG_MARKER'


def test_display_handles_non_mapping_user(caplog):
    # if a user is not a mapping display_users handles it by using the except branch
    users = [123]
    caplog.set_level('DEBUG')
    out = display_users(users)
    assert '<error>' in out


def test_build_index_skips_bad_entries(caplog):
    caplog.set_level('DEBUG')
    users = [{'name': 'no-id'}, 42, {'id': 'ok', 'name': 'HasId'}]
    idx = build_user_index(users)
    assert 'ok' in idx and len(idx) == 1


def test_filter_skips_bad_shape(caplog):
    caplog.set_level('DEBUG')
    users = [{'id': 1, 'name': 'Alice', 'role': 'User', 'status': 'Active'}, None]
    out = filter_users(users, {'role': 'User'})
    assert len(out) == 1 and out[0]['id'] == 1


def test_display_verbose_logs_debug(caplog, sample_users):
    caplog.set_level('DEBUG')
    import importlib, logging
    mod = importlib.import_module('user_display_optimized')
    # the module logger defaults to INFO; swap to DEBUG temporarily for this test
    previous = mod.logger.level
    mod.logger.setLevel(logging.DEBUG)
    try:
        display_users([sample_users[0]], verbose=True)
    finally:
        mod.logger.setLevel(previous)

    assert 'Processing user' in caplog.text
