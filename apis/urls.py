from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import api_token_auth 
from rest_framework.routers import DefaultRouter
from . import views


router= DefaultRouter()
router.register(r'juegos', views.JuegoViewSet , basename='juegos')
router.register(r'ventas', views.VentaViewSet, basename='ventas')
router.register(r'detalle_ventas', views.DetalleVentaViewSet, basename='detalle_ventas')


urlpatterns = [
    path('', include(router.urls)), 
    path('api-token-auth/', api_token_auth, name='api_token_auth'),
]