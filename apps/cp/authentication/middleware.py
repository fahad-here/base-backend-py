from django.utils.functional import SimpleLazyObject
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponseForbidden
from django.core.cache import cache

class CPAuthenticationMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    if not request.path.startswith('/api/v1/cp/auth/'):
      auth = JWTAuthentication()
      try:
        validated_token = auth.get_validated_token(
            auth.get_raw_token(request)
        )
        request.user = auth.get_user(validated_token)
      except:
        return HttpResponseForbidden('Invalid token')

    return self.get_response(request)

class RateLimitMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    if request.path.startswith('/api/v1/cp/'):
      ip = request.META.get('REMOTE_ADDR')
      key = f'ratelimit:{ip}'
      
      if cache.get(key, 0) >= 100:  # 100 requests per minute
        return HttpResponse('Too many requests', status=429)
          
      cache.get_or_set(key, 0, 60)
      cache.incr(key)
    
    return self.get_response(request)