import os
from pathlib import Path

# Default to development settings
DJANGO_ENV = os.getenv('DJANGO_ENV', 'development')

if DJANGO_ENV == 'production':
  from .production import *
elif DJANGO_ENV == 'staging':
  from .staging import *
else:
  from .development import *