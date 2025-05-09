from rest_framework import viewsets
from .serializers import JuegoSerializer, DetalleVentaSerializer, VentaSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
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
    
       # Establecer permisos según la acción
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:  # Crear, actualizar o eliminar
            permission_classes = [IsAdminUser]  # Solo admin puede crear, actualizar o eliminar
        else:  # Listar o ver un detalle
            permission_classes = [IsAuthenticated]  # Cualquier usuario autenticado puede ver
        return [permission() for permission in permission_classes]

class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return DetalleVenta.objects.all()
        # Solo mostrar detalles de ventas propias
        return DetalleVenta.objects.filter(venta__cliente=self.request.user)


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        # Si es admin, puede ver todas las ventas
        if self.request.user.is_staff:
            return Venta.objects.all()
        # Si es usuario normal, solo sus ventas
        return Venta.objects.filter(cliente=self.request.user) 


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
