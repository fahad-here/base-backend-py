"""Redis-specific exceptions."""

class RedisError(Exception):
  """Base exception for Redis errors."""
  pass

class RedisConnectionError(RedisError):
  """Raised when Redis connection fails."""
  pass

class RedisOperationError(RedisError):
  """Raised when a Redis operation fails."""
  pass