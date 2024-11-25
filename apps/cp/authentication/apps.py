from django.apps import AppConfig

class AuthConfig(AppConfig):
  default_auto_field = 'django.db.models.BigAutoField'
  name = 'apps.cp.authentication'
  label = 'cp_auth'  # This ensures a unique app label
  verbose_name = 'CP Authentication'