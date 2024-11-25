from django.apps import AppConfig

class MT5Config(AppConfig):
  name = 'core.mt5'
  verbose_name = 'MT5 Manager'
  
  def ready(self):
    from .pool import mt5_pools
    # Initialize connections when Django is ready
    connection_results = mt5_pools.connect_all()
    print("MT5 Connection Results:", connection_results)

default_app_config = 'core.mt5.MT5Config'
