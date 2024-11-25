def setup_auth():
  from .views import AuthViewSet
  from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    CustomerSerializer
  )
  from .middleware import (
    CPAuthenticationMiddleware,
    RateLimitMiddleware
  )
  
  return {
    'AuthViewSet': AuthViewSet,
    'RegisterSerializer': RegisterSerializer,
    'LoginSerializer': LoginSerializer,
    'CustomerSerializer': CustomerSerializer,
    'CPAuthenticationMiddleware': CPAuthenticationMiddleware,
    'RateLimitMiddleware': RateLimitMiddleware
  }