from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, LoginSerializer, CustomerSerializer
from core.elasticsearch.client import es_client
from core.elasticsearch.indices import CustomerIndex
from asgiref.sync import async_to_sync

Customer = get_user_model()

class AuthViewSet(viewsets.GenericViewSet):
  serializer_class = CustomerSerializer
  permission_classes = [AllowAny]
  
  @action(detail=False, methods=['post'])
  def register(self, request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    customer = serializer.save()
    
    # Remove direct ES indexing since it's handled by signals
    return Response(
      CustomerSerializer(customer).data, 
      status=status.HTTP_201_CREATED
    )

  @action(detail=False, methods=['post'])
  def login(self, request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = serializer.validated_data['user']
    refresh = RefreshToken.for_user(user)
    
    return Response({
      'access': str(refresh.access_token),
      'refresh': str(refresh),
      'user': CustomerSerializer(user).data
    })