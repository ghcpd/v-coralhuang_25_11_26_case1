import pytest
from typing import List, Dict


@pytest.fixture
def sample_users() -> List[Dict]:
    return [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "role": "Admin",
            "status": "Active",
            "join_date": "2023-01-15",
            "last_login": "2025-11-26",
        },
        {
            "id": 2,
            "name": "Jane Smith",
            "email": "jane@example.com",
            "role": "User",
            "status": "Inactive",
            "join_date": "2023-06-20",
            "last_login": "2025-11-20",
        },
    ]


@pytest.fixture
def many_users() -> List[Dict]:
    return [
        {"id": i, "name": f"User{i}", "email": f"user{i}@example.com", "role": "User", "status": "Active", "join_date": "2024-01-01", "last_login": "2025-11-26"}
        for i in range(1, 1100)
    ]
