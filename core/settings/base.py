from pathlib import Path
import environ

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
environ.Env.read_env(BASE_DIR / '.env')

INSTALLED_APPS = [
  # Local apps first to ensure models are loaded
  'models.apps.ModelsConfig',

  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  
  # Third party apps
  'rest_framework',
  'django_filters',
  'corsheaders',
  
  # Local apps
  'core.mt5',
  'shared',
  'apps.cp.authentication.apps.AuthConfig',
  # 'apps.cp.profiles',
  # 'apps.cp.transactions',
  # 'apps.crm.customers',
  # 'apps.crm.operations',
  # 'apps.crm.reports',
  # 'channels',
]

AUTH_USER_MODEL = 'models.Customer'

REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework_simplejwt.authentication.JWTAuthentication',
  ],
  'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.IsAuthenticated',
  ],
  'DEFAULT_FILTER_BACKENDS': [
    'django_filters.rest_framework.DjangoFilterBackend',
  ],
}

# Database settings
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': env('DB_NAME'),
    'USER': env('DB_USER'),
    'PASSWORD': env('DB_PASSWORD'),
    'HOST': env('DB_HOST'),
    'PORT': env('DB_PORT', default='5432'),
  }
}

# Redis settings
REDIS_HOST = env('REDIS_HOST')
REDIS_PORT = env('REDIS_PORT', default='6379')
SOCKET_TIMEOUT = 5
MAX_CONNECTIONS = 20

# Elasticsearch settings
ELASTICSEARCH_HOST = env('ELASTICSEARCH_HOST')
ELASTICSEARCH_PORT = env('ELASTICSEARCH_PORT', default='9200')

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True



# Redis Cache Configuration
CACHES = {
  'default': {
    'BACKEND': 'core.redis.cache.CustomRedisCache',
    'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}/0',
    'OPTIONS': {
      'CLIENT_CLASS': 'django_redis.client.DefaultClient',
      'SOCKET_CONNECT_TIMEOUT': SOCKET_TIMEOUT,
      'SOCKET_TIMEOUT': SOCKET_TIMEOUT,
      'RETRY_ON_TIMEOUT': True,
      'MAX_CONNECTIONS': MAX_CONNECTIONS,
    }
  }
}

# Elasticsearch settings
ELASTICSEARCH_SETTINGS = {
  'default': {
    'hosts': [f"{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}"],
    'indices': {
      'customer': 'core.elasticsearch.indices.customer.CustomerIndex',
      'transaction': 'core.elasticsearch.indices.transaction.TransactionIndex'
    }
  }
}

# Channel layer settings
CHANNEL_LAYERS = {
  "default": {
    "BACKEND": "channels_redis.core.RedisChannelLayer",
    "CONFIG": {
      "hosts": [(REDIS_HOST, REDIS_PORT)],
    },
  },
}

# ASGI application
ASGI_APPLICATION = "core.asgi.application"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'app': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'elasticsearch': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.request': {
          'handlers': ['console'],
          'level': 'DEBUG',
          'propagate': True,
        },
        'django.urls': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
  BASE_DIR / 'static'
]

# Templates configuration
TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
      'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
      ],
    },
  },
]

# URL Configuration
ROOT_URLCONF = 'core.urls'
APPEND_SLASH = False

# Add after DATABASES config
ELASTICSEARCH_INDEX_PREFIX = env('ELASTICSEARCH_INDEX_PREFIX', default='dev')
