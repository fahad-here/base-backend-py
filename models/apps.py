from django.apps import AppConfig

class ModelsConfig(AppConfig):
  default_auto_field = 'django.db.models.BigAutoField'
  name = 'models'
  verbose_name = 'Models'
  label = 'models'

  def ready(self):
    try:
      import models.customers.models
      import models.customers.signals
    except ImportError:
      pass