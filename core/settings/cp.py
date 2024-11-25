from .base import *

# CP-specific settings
ALLOWED_HOSTS = env.list('CP_ALLOWED_HOSTS', default=['*'])

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'corsheaders.middleware.CorsMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'apps.cp.authentication.middleware.CPAuthenticationMiddleware',
  'apps.cp.authentication.middleware.RateLimitMiddleware',
]

# CP-specific JWT settings
SIMPLE_JWT = {
  'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
  'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
  'USER_ID_FIELD': 'id',
  'USER_ID_CLAIM': 'user_id',
}