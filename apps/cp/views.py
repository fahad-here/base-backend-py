from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

Customer = get_user_model()

class CustomerViewSet(GenericViewSet):
  permission_classes = [IsAuthenticated]
  
  @action(detail=False, methods=['get'])
  def profile(self, request):
    return Response({
      'id': str(request.user.id),
      'email': request.user.email,
      'first_name': request.user.first_name,
      'last_name': request.user.last_name,
      'phone': request.user.phone,
      'country': request.user.country,
      'status': request.user.status
    })