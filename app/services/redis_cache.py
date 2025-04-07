import redis
import os
import json
from datetime import timedelta

# Initialize a Redis client to interact with the Redis database.
redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)


def cache_user(user_id: str, user_data: dict) -> None:
    """
    Cache user data in Redis.

    Args:
        user_id (str): The unique identifier for the user.
        user_data (dict): The user data to be cached, serialized as JSON.

    Returns:
        None
    """
    # Serialize the user data to JSON and store it in Redis with the key "user:{user_id}".
    redis_client.set(f"user:{user_id}", json.dumps(user_data))


def get_cached_user(email: str) -> dict:
    """
    Retrieve cached user data from Redis.

    Args:
        email (str): The user's email address (used as the key).

    Returns:
        dict: The cached user data as a dictionary, or None if not found.
    """
    # Attempt to retrieve the cached user data from Redis using the key "user:{email}".
    cached_user = redis_client.get(f"user:{email}")
    if cached_user:
        # If data is found, deserialize it from JSON and return it.
        return json.loads(cached_user)
    # Return None if no data is found in the cache.
    return None
