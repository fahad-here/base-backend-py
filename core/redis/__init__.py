"""Redis module initialization."""
from .client import RedisClient
from .exceptions import RedisError, RedisConnectionError, RedisOperationError
from .constants import (
  USER_PREFIX,
  CUSTOMER_PREFIX,
  SESSION_PREFIX,
  DEFAULT_EXPIRE
)

# Create singleton instance
redis_client = RedisClient()

__all__ = [
  "RedisClient",
  "redis_client",
  "RedisError",
  "RedisConnectionError",
  "RedisOperationError",
  "USER_PREFIX",
  "CUSTOMER_PREFIX",
  "SESSION_PREFIX",
  "DEFAULT_EXPIRE"
]