from rest_framework import serializers
from .models import Venta, DetalleVenta, Juego

class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ('juego', 'cantidad', 'subtotal')

class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True)

    class Meta:
        model = Venta
        fields = ('cliente', 'detalles', 'total')