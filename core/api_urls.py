from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router= DefaultRouter()
router.register(r'juegos', views.JuegoViewSet , basename='juegos')
router.register(r'ventas', views.VentaViewSet, basename='ventas')
router.register(r'detalle_ventas', views.DetalleVentaViewSet, basename='detalle_ventas')


urlpatterns = [
    path('', include(router.urls)) 
]