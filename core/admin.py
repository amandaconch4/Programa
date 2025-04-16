from django.contrib import admin
from .models import GestionUsuario
from .models import Usuario
from .models import Admin
from .models import Producto
from .models import Inventario
from .models import Ventas
from .models import Cliente

admin.site.register(GestionUsuario)
admin.site.register(Usuario)
admin.site.register(Admin)
admin.site.register(Producto)
admin.site.register(Inventario)
admin.site.register(Ventas)
admin.site.register(Cliente)
