"""Small helper to run module operations from shell scripts.
"""
from user_display_optimized import time_display, UserDisplay


def main() -> None:
    users = [
        {"id": i, "name": f"User{i}", "email": f"user{i}@example.com", "role": "User", "status": "Active", "join_date": "2024-01-01", "last_login": "2025-11-26"}
        for i in range(1, 101)
    ]
    users1k = [
        {"id": i, "name": f"User{i}", "email": f"user{i}@example.com", "role": "User", "status": "Active", "join_date": "2024-01-01", "last_login": "2025-11-26"}
        for i in range(1, 1001)
    ]
    t100 = time_display(users)
    t1000 = time_display(users1k)
    print(f"100 users: {t100:.3f} ms")
    print(f"1000 users: {t1000:.3f} ms")
    print(UserDisplay(users[:5]).display_users())


if __name__ == "__main__":
    main()
