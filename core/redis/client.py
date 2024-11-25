"""Redis client implementation."""
from typing import Optional, Any, Union, List, Tuple
import json
from redis import asyncio as aioredis
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from shared.utils.logger import logger
from .exceptions import RedisConnectionError, RedisOperationError
from .constants import (
  DEFAULT_EXPIRE,
  MAX_CONNECTIONS,
  SOCKET_TIMEOUT,
  SCAN_COUNT
)

class RedisClient:
  def __init__(self):
    """Initialize Redis client."""
    self.connection: Optional[aioredis.Redis] = None
    self._initialized = False
    self.LOG_TAG = "Redis"

  async def initialize(self) -> None:
    """Initialize Redis connection if not already initialized."""
    if self._initialized:
      return

    if not hasattr(settings, 'REDIS_HOST') or not hasattr(settings, 'REDIS_PORT'):
      raise ImproperlyConfigured("Redis settings not configured")

    await self.connect()
    self._initialized = True

  async def ensure_connection(self) -> None:
    """Ensure Redis connection is established."""
    if not self._initialized:
      await self.initialize()
    elif not self.connection:
      await self.connect()

  async def connect(self) -> None:
    """Establish connection to Redis."""
    try:
      logger.info(f"Connecting to Redis at {settings.REDIS_HOST}")
      
      self.connection = await aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        password=settings.REDIS_PASSWORD,
        decode_responses=True,
        max_connections=MAX_CONNECTIONS,
        socket_timeout=SOCKET_TIMEOUT,
        retry_on_timeout=True
      )
      
      # Test connection
      await self.connection.ping()
      logger.info("Redis connection established successfully")
        
    except Exception as e:
      logger.error(f"Failed to connect to Redis: {str(e)}")
      raise RedisConnectionError(f"Redis connection failed: {str(e)}")

  async def get(self, key: str) -> Any:
    """Get value from Redis with automatic JSON deserialization."""
    try:
      value = await self.connection.get(key)
      if value is None:
        return None
      
      try:
        return json.loads(value)
      except json.JSONDecodeError:
        return value
            
    except Exception as e:
      logger.error(f"Error getting key {key}: {str(e)}")
      raise RedisOperationError(f"Failed to get key: {str(e)}")

  async def set(
    self, 
    key: str, 
    value: Any, 
    expire: Optional[int] = DEFAULT_EXPIRE,
    nx: bool = False
  ) -> bool:
    """Set value in Redis with automatic JSON serialization."""
    try:
      if isinstance(value, (dict, list)):
        value = json.dumps(value)
          
      options = {}
      if nx:
        options['nx'] = True
      if expire:
        options['ex'] = expire
          
      return await self.connection.set(key, value, **options)
        
    except Exception as e:
      logger.error(f"Error setting key {key}: {str(e)}")
      raise RedisOperationError(f"Failed to set key: {str(e)}")

  async def delete(self, key: str) -> bool:
    """Delete a key from Redis."""
    try:
      return bool(await self.connection.delete(key))
    except Exception as e:
      logger.error(f"Error deleting key {key}: {str(e)}")
      raise RedisOperationError(f"Failed to delete key: {str(e)}")

  async def delete_pattern(self, pattern: str) -> int:
    """Delete all keys matching pattern."""
    try:
      cursor = 0
      deleted_count = 0
      
      while True:
        cursor, keys = await self.connection.scan(
          cursor=cursor,
          match=pattern,
          count=SCAN_COUNT
        )
        
        if keys:
          deleted_count += await self.connection.delete(*keys)
        
        if cursor == 0:
          break
              
      logger.info(f"Deleted {deleted_count} keys matching pattern: {pattern}")
      return deleted_count
        
    except Exception as e:
      logger.error(f"Error deleting pattern {pattern}: {str(e)}")
      raise RedisOperationError(f"Failed to delete pattern: {str(e)}")

  async def increment(
    self, 
    key: str, 
    expire: Optional[int] = None
  ) -> int:
    """Increment a counter and optionally set expiry."""
    try:
      pipe = self.connection.pipeline()
      pipe.incr(key)
      if expire:
        pipe.expire(key, expire)
      
      results = await pipe.execute()
      return results[0]  # Return the increment result
        
    except Exception as e:
      logger.error(f"Error incrementing key {key}: {str(e)}")
      raise RedisOperationError(f"Failed to increment key: {str(e)}")

  async def health_check(self) -> dict:
    """Check Redis connection health."""
    try:
      await self.connection.ping()
      return {
        "status": "healthy",
        "connected": True
      }
    except Exception as e:
      return {
        "status": "unhealthy",
        "connected": False,
        "error": str(e)
      }

  async def close(self) -> None:
    """Close Redis connection."""
    if self.connection:
      await self.connection.close()
      self.connection = None

  async def __aenter__(self):
    await self.ensure_connection()
    return self

  async def __aexit__(self, exc_type, exc_val, exc_tb):
    await self.close()

  async def get_many(self, keys: List[str]) -> dict:
    """Get multiple values at once."""
    try:
      pipe = self.connection.pipeline()
      for key in keys:
        pipe.get(key)
      values = await pipe.execute()
      return {k: v for k, v in zip(keys, values) if v is not None}
    except Exception as e:
      logger.error(f"Error getting multiple keys: {str(e)}")
      raise RedisOperationError(f"Failed to get multiple keys: {str(e)}")

  async def set_many(
    self,
    mapping: dict,
    expire: Optional[int] = DEFAULT_EXPIRE
  ) -> bool:
    """Set multiple key-value pairs."""
    try:
      pipe = self.connection.pipeline()
      for key, value in mapping.items():
        if isinstance(value, (dict, list)):
          value = json.dumps(value)
        pipe.set(key, value, ex=expire)
      results = await pipe.execute()
      return all(results)
    except Exception as e:
      logger.error(f"Error setting multiple keys: {str(e)}")
      raise RedisOperationError(f"Failed to set multiple keys: {str(e)}")