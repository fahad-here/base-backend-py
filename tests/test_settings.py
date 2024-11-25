from core.settings.base import *

# Test specific settings
DEBUG = False
SECRET_KEY = 'test-secret-key'

# Use SQLite for testing
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:',
  }
}

# Use in-memory cache for testing
CACHES = {
  'default': {
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
  }
}

# Test-specific Elasticsearch settings
ELASTICSEARCH_HOST = 'localhost'
ELASTICSEARCH_PORT = '9200'
ELASTICSEARCH_INDEX_PREFIX = 'test'

# Test-specific Redis settings
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'

# Disable CORS for testing
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = False

# Disable WebSocket for testing
CHANNEL_LAYERS = {
  "default": {
    "BACKEND": "channels.layers.InMemoryChannelLayer",
  },
}

# Disable logging during tests
LOGGING = {
  'version': 1,
  'disable_existing_loggers': True,
  'handlers': {
    'null': {
      'class': 'logging.NullHandler',
    },
  },
  'loggers': {
    '': {
      'handlers': ['null'],
      'level': 'CRITICAL',
    },
  },
}
