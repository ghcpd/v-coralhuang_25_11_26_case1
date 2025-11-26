import re
import time
from typing import Any, Dict

import pytest

import user_display_optimized as udf


def test_display_users_empty(caplog):
    caplog.set_level("INFO")
    output = udf.display_users([])
    assert "Processed 0 users" in output
    assert output.endswith("\n")
    # No warnings expected
    assert not [rec for rec in caplog.records if rec.levelname == "WARNING"]


def test_display_users_missing_keys(caplog):
    user = {"id": 1, "name": "No Email"}  # missing many fields
    caplog.set_level("WARNING")
    output = udf.display_users([user], show_all=False)
    assert "N/A" in output
    warnings = [rec for rec in caplog.records if rec.levelname == "WARNING"]
    # Expect warnings for each missing default field except id & name
    missing_fields = set(udf.DEFAULT_FIELDS) - {"id", "name"}
    warned_fields = set()
    for rec in warnings:
        m = re.search(r"missing key '([^']+)'", rec.message)
        if m:
            warned_fields.add(m.group(1))
    assert missing_fields.issubset(warned_fields)
    assert all(udf.MARKER in rec.message for rec in warnings)


def test_get_user_by_id_with_and_without_index(sample_users):
    index = udf.build_user_index(sample_users)
    assert udf.get_user_by_id(index, sample_users[0]["id"]) == sample_users[0]
    assert udf.get_user_by_id(sample_users, sample_users[1]["id"], prebuilt_index=index) == sample_users[1]
    assert udf.get_user_by_id(sample_users, 9999) is None


def test_build_user_index_duplicate_and_missing(caplog):
    users = [
        {"id": 1, "name": "A"},
        {"id": 1, "name": "B"},  # duplicate id
        {"name": "No ID"},
    ]
    caplog.set_level("WARNING")
    idx = udf.build_user_index(users)
    assert idx[1]["name"] == "A"  # first wins
    messages = " ".join(rec.message for rec in caplog.records)
    assert "duplicate" in messages
    assert "missing key 'id'" in messages


def test_filter_users(sample_users):
    users = sample_users + [
        {
            "id": 99,
            "name": "alice wonder",
            "email": "alice@example.com",
            "role": "User",
            "status": "Active",
            "join_date": "2024-01-01",
            "last_login": "2025-11-26",
        }
    ]
    filtered = udf.filter_users(users, {"role": "User", "status": "Active"})
    assert all(u["role"] == "User" and u["status"] == "Active" for u in filtered)
    name_filtered = udf.filter_users(users, {"name": "ALICE"})
    assert any(u["id"] == 99 for u in name_filtered)


def test_export_users_to_string(sample_users):
    output = udf.export_users_to_string(sample_users)
    assert output.startswith("USER_EXPORT_START")
    assert output.endswith("USER_EXPORT_END\n")
    assert "User ID: 1" in output
    # Ensure separator present
    assert "-" * 100 in output


def test_cli_json_output(capsys):
    # Should not raise and should return 0
    code = udf._cli(["--count", "2", "--json", "--no-summary"])
    captured = capsys.readouterr()
    assert code == 0
    # Output should be valid JSON
    import json

    data = json.loads(captured.out)
    assert len(data) == 2


# ----------------------- Performance Tests -----------------------


@pytest.mark.flaky(reruns=2, reruns_delay=0.05)
def test_performance_display_100():
    users = udf.generate_dummy_users(100)
    start = time.perf_counter()
    udf.display_users(users)
    duration = (time.perf_counter() - start) * 1000  # ms
    assert duration < 50, f"display 100 users took {duration:.2f} ms"


@pytest.mark.flaky(reruns=2, reruns_delay=0.05)
def test_performance_display_1000(many_users):
    start = time.perf_counter()
    udf.display_users(many_users)
    duration = (time.perf_counter() - start) * 1000  # ms
    assert duration < 100, f"display 1000 users took {duration:.2f} ms"


@pytest.mark.flaky(reruns=2, reruns_delay=0.05)
def test_performance_filter_100():
    users = udf.generate_dummy_users(100)
    start = time.perf_counter()
    udf.filter_users(users, {"role": "Admin"})
    duration = (time.perf_counter() - start) * 1000  # ms
    assert duration < 10, f"filter 100 users took {duration:.2f} ms"


@pytest.mark.flaky(reruns=2, reruns_delay=0.05)
def test_performance_get_user_by_id_index():
    users = udf.generate_dummy_users(1000)
    index = udf.build_user_index(users)
    # Warmup
    udf.get_user_by_id(index, 500)
    iterations = 5000
    start = time.perf_counter()
    for i in range(iterations):
        udf.get_user_by_id(index, i % 1000)
    total = (time.perf_counter() - start)
    avg = (total / iterations) * 1000  # ms per lookup
    assert avg < 1, f"avg lookup {avg:.4f} ms"
