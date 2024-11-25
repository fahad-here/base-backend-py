from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import api_root

urlpatterns = [
  path('', api_root, name='api-root'),
  path('admin/', admin.site.urls),
  path('api/v1/cp/', include('apps.cp.urls')),
  # path('api/v1/crm/', include('apps.crm.urls')),
]

if settings.DEBUG:
  from django.urls import get_resolver
  print("Available patterns:", get_resolver().url_patterns)