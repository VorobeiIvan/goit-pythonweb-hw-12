from app.utils.dependencies import get_current_user


def test_get_current_user():
    """
    Test the get_current_user dependency.
    """
    # Приклад токена або даних для тесту
    token = "test_token"
    user = get_current_user(token)
    assert user is not None, "User should not be None"
    assert user.email == "test@example.com", "Email does not match"
