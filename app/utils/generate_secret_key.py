import secrets


def generate_secret_key():
    """
    Generate a long, random, and unique secret key.

    This function uses Python's `secrets` module to generate a secure, URL-safe
    random string. The generated key is suitable for use as a SECRET_KEY in
    web applications, ensuring strong cryptographic security.

    Returns:
        str: A randomly generated secret key.

    How to use `generate_secret_key.py`:
    1. Open a terminal in the root directory of your project.
    2. Run the script using the command:
       python /path/to/generate_secret_key.py
    3. The script will output a generated secret key to the console. For example:
       Your generated SECRET_KEY:
       abc123... (randomly generated string)
    4. Copy the generated key and paste it into your `.env` file under the variable `SECRET_KEY`. For example:
       SECRET_KEY=abc123...
    5. Ensure your application uses this key for cryptographic operations, such as token encryption.

    Why is this important?
    - **Security**: The secret key is used for encrypting tokens (e.g., JWT) and ensuring the security of your application.
    - **Uniqueness**: Each application should have its own unique secret key to prevent compromise.
    """
    # Generate a secure, random, URL-safe string of 32 characters
    return secrets.token_urlsafe(32)


if __name__ == "__main__":
    # Print a message to indicate the purpose of the script
    print("Your generated SECRET_KEY:")

    # Generate and print the secret key to the console
    print(generate_secret_key())
