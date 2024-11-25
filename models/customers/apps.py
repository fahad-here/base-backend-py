 from django.apps import AppConfig

class CustomersConfig(AppConfig):
  default_auto_field = 'django.db.models.BigAutoField'
  name = 'models.customers'
  label = 'models'  # Changed from 'customers' to 'models' to match AUTH_USER_MODEL

  def ready(self):
    from . import signals  # Import signals when the app is ready