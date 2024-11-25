"""Core package initialization."""
# Import constants first since they don't depend on Django
from .constants import (
  LOG_EVENTS,
  BACKEND_RESOURCES,
  RESOURCE_ACTIONS,
  ResponseMessages
)

# Lazy load clients to avoid circular imports
def get_redis_client():
  from .redis import redis_client
  return redis_client

def get_es_client():
  from .elasticsearch import es_client
  return es_client

def get_db():
  from .db.session import get_async_session
  return get_async_session()

__all__ = [
  "LOG_EVENTS",
  "BACKEND_RESOURCES",
  "RESOURCE_ACTIONS",
  "ResponseMessages",
  "get_redis_client",
  "get_es_client",
  "get_db"
]