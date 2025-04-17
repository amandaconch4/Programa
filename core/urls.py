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
from .views import witcher3
from .views import gta5
from .views import zelda
from .views import assassinscreed
from .views import payday3
from .views import forzahorizon5
from .views import needforspeed
from .views import granturismo7
from .views import fifa24
from .views import nba2k24
from .views import efootball
from .views import finalfantasy
from .views import baldursgate3
from .views import persona5
from .views import registro
from .views import admin
from .views import panel_admin
from .views import panel_usuario
from .views import pago
from . import views

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
    path('sevengamer/witcher3', witcher3, name="witcher3"),
    path('sevengamer/gta5', gta5, name="gta5"),
    path('sevengamer/zelda', zelda, name="zelda"),
    path('sevengamer/assassinscreed', assassinscreed, name="assassinscreed"),
    path('sevengamer/payday3', payday3, name="payday3"),
    path('sevengamer/forzahorizon5', forzahorizon5, name="forzahorizon5"),
    path('sevengamer/needforspeed', needforspeed, name="needforspeed"),
    path('sevengamer/granturismo7', granturismo7, name="granturismo7"),
    path('sevengamer/fifa24', fifa24, name="fifa24"),
    path('sevengamer/nba2k24', nba2k24, name="nba2k24"),
    path('sevengamer/efootball', efootball, name="efootball"),
    path('sevengamer/finalfantasy', finalfantasy, name="finalfantasy"),
    path('sevengamer/baldursgate3', baldursgate3, name="baldursgate3"),
    path('sevengamer/persona5', persona5, name="persona5"),
    path('sevengamer/registro', registro, name="registro"),
    path('sevengamer/admin', admin, name="admin"),
    path('sevengamer/panel-admin', panel_admin, name="panel_admin"),
    path('sevengamer/panel-usuario', panel_usuario, name="panel_usuario"),
    path('sevengamer/pago', pago, name="pago"),
    path('', sevengamer, name="home"),
]