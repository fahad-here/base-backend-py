from django.urls import re_path
from apps.cp.consumers import CustomerConsumer
from apps.crm.consumers import StaffConsumer, NotificationConsumer

websocket_urlpatterns = [
  re_path(r"ws/customer/(?P<customer_id>\w+)/$", CustomerConsumer.as_asgi()),
  re_path(r"ws/staff/(?P<staff_id>\w+)/$", StaffConsumer.as_asgi()),
  re_path(r"ws/notifications/$", NotificationConsumer.as_asgi()),
] 