from django.apps import AppConfig
import json

def on_user_delete(user):
  print(f"User {user.Login} was deleted")

def on_deal_add(deal):
  deal_info = {
    'Ticket': deal.Ticket,
    'Order': deal.Order,
    'Time': deal.Time,
    'Login': deal.Login,
    'Symbol': deal.Symbol,
    'Action': deal.Action,
    'Volume': deal.Volume,
    'Price': deal.Price,
    'Commission': deal.Commission,
    'Profit': deal.Profit,
    'Comment': deal.Comment,
    'Dealer': deal.Dealer,
    'Entry': deal.Entry
  }
  print("New Deal Details:")
  print(json.dumps(deal_info, indent=2, default=str))

class MT5Config(AppConfig):
  name = 'core.mt5'
  verbose_name = 'MT5 Manager'
  
  def ready(self):
    from .pool import mt5_pools
    # Initialize connections when Django is ready
    connection_results = mt5_pools.connect_all()
    print("MT5 Connection Results:", connection_results)
    
    # Setup test callbacks
    mt5_pools.add_user_callback('user_delete', on_user_delete)
    mt5_pools.add_deal_callback('deal_add', on_deal_add)
    print("MT5 callbacks registered")

default_app_config = 'core.mt5.MT5Config'
