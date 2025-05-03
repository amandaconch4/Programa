from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DetalleVenta, Venta

@receiver(post_save, sender=DetalleVenta)
def actualizar_total_venta(sender, instance, **kwargs):
    """
    Esta función se ejecuta cuando se guarda un DetalleVenta.
    Se asegura de que el total de la venta se actualice.
    """
    venta = instance.venta
    venta.actualizar_total()