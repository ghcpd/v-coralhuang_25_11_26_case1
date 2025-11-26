"""Configuration and fixtures for user display tests."""

import pytest


@pytest.fixture
def sample_users():
    """Fixture providing sample user data for tests."""
    return [
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
        {
            'id': 3,
            'name': 'Bob Johnson',
            'email': 'bob@example.com',
            'role': 'Moderator',
            'status': 'Active',
            'join_date': '2024-02-10',
            'last_login': '2025-11-25'
        },
        {
            'id': 4,
            'name': 'Alice Williams',
            'email': 'alice@example.com',
            'role': 'User',
            'status': 'Active',
            'join_date': '2024-05-12',
            'last_login': '2025-11-26'
        },
        {
            'id': 5,
            'name': 'Charlie Brown',
            'email': 'charlie@example.com',
            'role': 'User',
            'status': 'Active',
            'join_date': '2024-08-03',
            'last_login': '2025-11-24'
        },
    ]


@pytest.fixture
def large_user_set():
    """Fixture providing 1000 users for performance testing."""
    return [
        {
            'id': i,
            'name': f'User {i}',
            'email': f'user{i}@example.com',
            'role': ['Admin', 'User', 'Moderator'][i % 3],
            'status': ['Active', 'Inactive'][i % 2],
            'join_date': f'2023-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}',
            'last_login': '2025-11-26'
        }
        for i in range(1, 1001)
    ]
