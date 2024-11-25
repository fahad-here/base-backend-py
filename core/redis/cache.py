from django_redis.cache import RedisCache
from django.core.cache.backends.base import BaseCache
from redis import Redis
from django.conf import settings

class CustomRedisCache(RedisCache):
  def get_client(self, write=False):
    """Get a Redis client."""
    if self._client is None:
      self._client = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        socket_timeout=settings.SOCKET_TIMEOUT,
        retry_on_timeout=True,
        max_connections=settings.MAX_CONNECTIONS
      )
    return self._client 