import logging
from slowapi import Limiter
from slowapi.util import get_remote_address

# Налаштування логування
logger = logging.getLogger(__name__)

# Ініціалізація Limiter
limiter = Limiter(key_func=get_remote_address)

logger.info("Rate limiter initialized with key function: get_remote_address")
