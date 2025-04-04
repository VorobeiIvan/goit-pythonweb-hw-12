import pytest
import redis


@pytest.fixture
def redis_client():
    """
    Фікстура для створення клієнта Redis.
    """
    client = redis.Redis(host="localhost", port=6379, db=0)
    try:
        yield client
    finally:
        client.flushdb()  # Очищення бази даних після тестів
        client.close()


def test_redis_set_and_get(redis_client):
    """
    Тест для перевірки збереження і отримання даних у Redis.
    """
    key = "test_key"
    value = "test_value"

    # Зберігаємо значення
    redis_client.set(key, value)

    # Отримуємо значення
    cached_value = redis_client.get(key)
    assert cached_value is not None, "Value was not found in Redis"
    assert (
        cached_value.decode("utf-8") == value
    ), "Cached value does not match the original"


def test_redis_expiration(redis_client):
    """
    Тест для перевірки часу життя ключа у Redis.
    """
    key = "test_key"
    value = "test_value"

    # Зберігаємо значення з часом життя 1 секунда
    redis_client.set(key, value, ex=1)

    # Перевіряємо, що значення доступне
    cached_value = redis_client.get(key)
    assert cached_value is not None, "Value expired too early"

    # Чекаємо 2 секунди
    import time

    time.sleep(2)

    # Перевіряємо, що значення більше недоступне
    cached_value = redis_client.get(key)
    assert cached_value is None, "Value did not expire as expected"


def test_redis_delete(redis_client):
    """
    Тест для перевірки видалення ключа у Redis.
    """
    key = "test_key"
    value = "test_value"

    # Зберігаємо значення
    redis_client.set(key, value)

    # Видаляємо ключ
    redis_client.delete(key)

    # Перевіряємо, що ключ видалено
    cached_value = redis_client.get(key)
    assert cached_value is None, "Key was not deleted from Redis"
