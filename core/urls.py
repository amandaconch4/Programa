from django.urls import path
from .views import sevengamer
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm

urlpatterns = [
    # Auth URLs
    path('', sevengamer, name="home"),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('recuperar-password/', auth_views.PasswordResetView.as_view(template_name='recuperar_password.html',), name='password_reset'),
    path('recuperar-password/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='recuperar_password_enviado.html'), name='password_reset_done'),
    path('recuperar-password/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reestablecer_confirmar.html'), name='password_reset_confirm'),
    path('recuperar-password/completado/', auth_views.PasswordResetCompleteView.as_view(template_name='reestablecer_completado.html'), name='password_reset_complete'),
    path('mi-cuenta/', views.mi_cuenta, name='mi_cuenta'),
    path('mi-cuenta/actualizar-perfil/', views.actualizar_perfil, name='actualizar_perfil'),
    path('mi-cuenta/actualizar-foto/', views.actualizar_foto, name='actualizar_foto'),

    # Game URLs
    path('sevengamer', sevengamer, name="sevengamer"),
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
    path('sevengamer/admin', admin, name="admin"),
    path('sevengamer/panel-admin', panel_admin, name="panel_admin"),
    path('sevengamer/panel-usuario', panel_usuario, name="panel_usuario"),
    path('sevengamer/pago', pago, name="pago"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)