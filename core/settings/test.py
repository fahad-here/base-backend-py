from .base import *

# Test specific settings
DEBUG = False
ELASTICSEARCH_INDEX_PREFIX = 'test'
SECRET_KEY = 'django-insecure-test-key-do-not-use-in-production'

# Test Database
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'test_db',
    'USER': env('DB_USER'),
    'PASSWORD': env('DB_PASSWORD'),
    'HOST': env('DB_HOST'),
    'PORT': env('DB_PORT', default='5432'),
  }
}

# Test Redis
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'

# Test Elasticsearch
ELASTICSEARCH_HOST = 'localhost'
ELASTICSEARCH_PORT = '9200'
ELASTICSEARCH_INDEX_PREFIX = 'test'
ELASTICSEARCH_USER = 'elastic'
ELASTICSEARCH_PASSWORD = 'elastic123'

# Keep the Redis cache for integration tests
CACHES = {
    'default': {
        'BACKEND': 'core.redis.cache.CustomRedisCache',
        'LOCATION': f'redis://localhost:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'RETRY_ON_TIMEOUT': True,
            'MAX_CONNECTIONS': 20,
        }
    }
}

# Keep channel layers for WebSocket tests
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}

# Disable logging during tests
LOGGING = {
  'version': 1,
  'disable_existing_loggers': True,
}