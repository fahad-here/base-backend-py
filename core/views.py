from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'status': 'ok',
        'version': '1.0.0',
        'endpoints': {
            'cp': '/api/v1/cp/',
            'admin': '/admin/'
        }
    }) 