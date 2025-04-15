from django.urls import path
from .views import sevengamer
from .views import login
from .views import terror
from .views import mundoabierto
from .views import accion
from .views import carreras
from .views import deportes
from .views import rol
from .views import registro
from .views import admin


urlpatterns = [
    path('sevengamer', sevengamer, name="sevengamer"),
    path('sevengamer/login', login, name="login"),
    path('sevengamer/terror', terror, name="terror"),
    path('sevengamer/mundoabierto', mundoabierto, name="mundoabierto"),
    path('sevengamer/accion', accion, name="accion"),
    path('sevengamer/carreras', carreras, name="carreras"),
    path('sevengamer/deportes', deportes, name="deportes"),
    path('sevengamer/rol', rol, name="rol"),
    path('sevengamer/registro', registro, name="registro"),
    path('sevengamer/admin', admin, name="admin"),

]