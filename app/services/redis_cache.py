import redis
import os
import json
from datetime import timedelta

# Redis configuration
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True,
)


def cache_user(email: str, user_data: dict, expiration_minutes: int = 30):
    """
    Cache user data in Redis.

    Args:
        email (str): The user's email address (used as the key).
        user_data (dict): The user data to cache.
        expiration_minutes (int): Expiration time in minutes (default is 30).
    """
    redis_client.setex(
        f"user:{email}", timedelta(minutes=expiration_minutes), json.dumps(user_data)
    )


def get_cached_user(email: str) -> dict:
    """
    Retrieve cached user data from Redis.

    Args:
        email (str): The user's email address (used as the key).

    Returns:
        dict: The cached user data, or None if not found.
    """
    cached_user = redis_client.get(f"user:{email}")
    if cached_user:
        return json.loads(cached_user)
    return None
