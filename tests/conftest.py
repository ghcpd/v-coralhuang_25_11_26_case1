import pytest

from user_display_optimized import SAMPLE_USERS, generate_dummy_users


@pytest.fixture()
def sample_users():
    # Return a copy to avoid test mutation issues
    return [user.copy() for user in SAMPLE_USERS]


@pytest.fixture()
def many_users():
    return generate_dummy_users(1000)
