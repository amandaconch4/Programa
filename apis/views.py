from rest_framework import viewsets
from .serializers import JuegoSerializer, DetalleVentaSerializer, VentaSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from core.models import Juego, DetalleVenta, Venta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# Create your views here.

class JuegoViewSet(viewsets.ModelViewSet):
    queryset = Juego.objects.all()
    serializer_class = JuegoSerializer
    permission_classes = [IsAuthenticated]
   

class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer
    permission_classes = [IsAuthenticated]


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtrar las ventas por el usuario autenticado
        return self.queryset.filter(cliente=self.request.user)  


@api_view(['POST'])
@permission_classes([AllowAny])
def api_token_auth(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Por favor ingrese usuario y contraseña'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response(
            {'error': 'Credenciales inválidas'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_200_OK)
