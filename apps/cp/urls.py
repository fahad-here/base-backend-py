from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet

app_name = 'cp'

profile = CustomerViewSet.as_view({
  'get': 'profile'
})

urlpatterns = [
  path('auth/', include('apps.cp.authentication.urls', namespace='auth')),
  path('profile', profile, name='profile')

  # path('profile/', CustomerViewSet.as_view({'get': 'profile'}), name='profile'),
  # path('transactions/', include('apps.cp.transactions.urls')),
]