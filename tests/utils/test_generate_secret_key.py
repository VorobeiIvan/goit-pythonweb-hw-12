from app.utils.generate_secret_key import generate_secret_key


def test_generate_secret_key():
    """
    Test the generate_secret_key function.
    """
    key = generate_secret_key()
    assert isinstance(key, str), "Secret key should be a string"
    assert len(key) == 32, "Secret key should be 32 characters long"
