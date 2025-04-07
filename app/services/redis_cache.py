import redis
import os
import json
from datetime import timedelta

import redis

redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)


def cache_user(user_id, user_data):
    redis_client.set(f"user:{user_id}", user_data)


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
