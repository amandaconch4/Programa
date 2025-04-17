from django.contrib import admin
from .models import GestionUsuario
from .models import Usuario, PerfilUsuario, Juego, Categoria, Venta, DetalleVenta


admin.site.register(Usuario)
admin.site.register(PerfilUsuario)
admin.site.register(Juego)
admin.site.register(Categoria)
admin.site.register(Venta)
admin.site.register(DetalleVenta)

