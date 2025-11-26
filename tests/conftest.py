import pytest


@pytest.fixture
def sample_users():
    return [
        {
            'id': i,
            'name': f'User {i}',
            'email': f'user{i}@example.com',
            'role': 'User' if i % 2 else 'Admin',
            'status': 'Active' if i % 3 else 'Inactive',
            'join_date': '2024-01-01',
            'last_login': '2025-11-26'
        }
        for i in range(1, 11)
    ]


@pytest.fixture
def large_users():
    # produce a larger list for performance tests (1000 entries)
    return [
        {
            'id': i,
            'name': f'PerfUser {i}',
            'email': f'perf{i}@example.com',
            'role': 'User',
            'status': 'Active',
            'join_date': '2024-01-01',
            'last_login': '2025-11-26'
        }
        for i in range(1, 1001)
    ]
