from django.http import HttpResponseForbidden
from shared.utils.logger import logger

class StaffAuthenticationMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    if request.path.startswith('/api/v1/crm/'):
      if not request.user.is_staff:
        return HttpResponseForbidden()
    
    return self.get_response(request)

class AuditLogMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    response = self.get_response(request)
    
    if request.path.startswith('/api/v1/crm/'):
      logger.info(
        'Staff action',
        extra={
          'staff_id': request.user.id,
          'path': request.path,
          'method': request.method,
          'status_code': response.status_code
        }
      )
    
    return response