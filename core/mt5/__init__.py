from django.apps import AppConfig
import json

print("DEBUG: MT5 Module Loading")

def on_user_update(user):
  print(f"User {user.Login} was updated")

def on_user_delete(user):
  print(f"User {user.Login} was deleted")

def on_deal_add(deal):
  deal_info = {
    'Ticket': deal.Deal,
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
