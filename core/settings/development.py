from datetime import timedelta
from .base import *

DEBUG = True
SECRET_KEY = env('SECRET_KEY')

# Development-specific settings
ALLOWED_HOSTS = ['*']
INTERNAL_IPS = ['127.0.0.1']

# Development middleware
MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'corsheaders.middleware.CorsMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
] 

# Elasticsearch settings
ELASTICSEARCH_HOST = 'localhost'
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_INDEX_PREFIX = 'dev'
ELASTICSEARCH_USER = 'elastic'
ELASTICSEARCH_PASSWORD = 'elastic123'