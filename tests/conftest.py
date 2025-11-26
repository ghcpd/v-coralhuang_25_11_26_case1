"""Pytest configuration and shared fixtures."""

import pytest
from typing import List, Dict, Any


@pytest.fixture
def sample_users() -> List[Dict[str, Any]]:
    """Sample user data for testing."""
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
    ]


@pytest.fixture
def empty_users() -> List[Dict[str, Any]]:
    """Empty user list for edge case testing."""
    return []


@pytest.fixture
def users_with_missing_keys() -> List[Dict[str, Any]]:
    """User data with missing keys for error handling tests."""
    return [
        {'id': 1, 'name': 'Complete User'},
        {'id': 2},  # Missing most fields
        {'name': 'No ID User', 'email': 'test@example.com'},  # Missing ID
        {},  # Empty dictionary
    ]


@pytest.fixture
def large_user_dataset_100() -> List[Dict[str, Any]]:
    """Generate 100 users for performance testing."""
    return [
        {
            'id': i,
            'name': f'User {i}',
            'email': f'user{i}@example.com',
            'role': ['Admin', 'User', 'Moderator'][i % 3],
            'status': ['Active', 'Inactive'][i % 2],
            'join_date': '2024-01-01',
            'last_login': '2025-11-26'
        }
        for i in range(1, 101)
    ]


@pytest.fixture
def large_user_dataset_1000() -> List[Dict[str, Any]]:
    """Generate 1000 users for performance testing."""
    return [
        {
            'id': i,
            'name': f'User {i}',
            'email': f'user{i}@example.com',
            'role': ['Admin', 'User', 'Moderator'][i % 3],
            'status': ['Active', 'Inactive'][i % 2],
            'join_date': '2024-01-01',
            'last_login': '2025-11-26'
        }
        for i in range(1, 1001)
    ]
