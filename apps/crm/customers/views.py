from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import CustomerSerializer, CustomerUpdateSerializer
from .filters import CustomerFilter
from shared.services.elasticsearch import es_client
from models.customers.elasticsearch import CustomerIndex

Customer = get_user_model()

class CustomerViewSet(viewsets.ModelViewSet):
  queryset = Customer.objects.all()
  serializer_class = CustomerSerializer
  filterset_class = CustomerFilter
  
  def get_serializer_class(self):
    if self.action == 'update':
      return CustomerUpdateSerializer
    return CustomerSerializer
  
  @action(detail=True, methods=['post'])
  def block(self, request, pk=None):
    customer = self.get_object()
    customer.status = 'blocked'
    customer.save()
    
    # Update Elasticsearch
    es_client.update(
      index=CustomerIndex.get_index_name(),
      id=str(customer.id),
      doc={'status': 'blocked'}
    )
    
    return Response({'status': 'blocked'})