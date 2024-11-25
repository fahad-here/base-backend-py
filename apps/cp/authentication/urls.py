from django.urls import path
from .views import AuthViewSet

app_name = 'auth'

auth_register = AuthViewSet.as_view({
  'post': 'register'
})

auth_login = AuthViewSet.as_view({
  'post': 'login'
})

urlpatterns = [
  path('register', auth_register, name='register'),
  path('login', auth_login, name='login')
]