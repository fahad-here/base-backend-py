from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .pool import mt5_pools
from .constants import MT5_SERVERS

@api_view(['GET'])
@permission_classes([AllowAny])
def check_mt5_connections(request):
  status = {
    'demo': {
      'connected': mt5_pools.demo._connected,
      'server_name': next(s.name for s in MT5_SERVERS if s.type == 'demo')
    },
    'live': {
      'connected': mt5_pools.live._connected,
      'server_name': next(s.name for s in MT5_SERVERS if s.type == 'live')
    }
  }
  return Response(status)
