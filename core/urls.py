from django.urls import path
from .views import sevengamer
from .views import login
from .views import terror
from .views import mundoabierto
from .views import accion
from .views import carreras
from .views import deportes
from .views import rol
from .views import residentevil
from .views import outlast
from .views import deadspace
from .views import registro
from .views import admin
from .views import panel_admin
from .views import panel_usuario


urlpatterns = [
    path('sevengamer', sevengamer, name="sevengamer"),
    path('sevengamer/login', login, name="login"),
    path('sevengamer/terror', terror, name="terror"),
    path('sevengamer/mundoabierto', mundoabierto, name="mundoabierto"),
    path('sevengamer/accion', accion, name="accion"),
    path('sevengamer/carreras', carreras, name="carreras"),
    path('sevengamer/deportes', deportes, name="deportes"),
    path('sevengamer/rol', rol, name="rol"),
    path('sevengamer/residentevil', residentevil, name="residentevil"),
    path('sevengamer/outlast', outlast, name="outlast"),
    path('sevengamer/deadspace', deadspace, name="deadspace"),
    path('sevengamer/registro', registro, name="registro"),
    path('sevengamer/admin', admin, name="admin"),
    path('sevengamer/panel-admin', panel_admin, name="panel_admin"),
    path('sevengamer/panel-usuario', panel_usuario, name="panel_usuario"),
]