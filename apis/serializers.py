from rest_framework import serializers
from core.models import Venta, DetalleVenta, Juego


class JuegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Juego
        fields = '__all__'


class DetalleVentaSerializer(serializers.ModelSerializer):
    juego = JuegoSerializer()

    class Meta:
        model = DetalleVenta
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True)

    class Meta:
        model = Venta
        fields = '__all__'