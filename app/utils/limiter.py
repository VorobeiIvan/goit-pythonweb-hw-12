import logging
from slowapi import Limiter
from slowapi.util import get_remote_address

# Configure logging for the module
logger = logging.getLogger(__name__)

# Initialize the rate limiter
# The `key_func` determines how to identify clients (e.g., by their remote address)
limiter = Limiter(key_func=get_remote_address)

# Log the initialization of the rate limiter
logger.info("Rate limiter initialized with key function: get_remote_address")

"""
This module sets up a rate limiter using the `slowapi` library.

Classes and Variables:
- limiter: An instance of `Limiter` that uses the client's remote address as the key function.

Functions:
- get_remote_address: A utility function from `slowapi` to retrieve the client's IP address.

Usage:
Import this module and use the `limiter` instance to apply rate limiting to your Flask routes.
"""
