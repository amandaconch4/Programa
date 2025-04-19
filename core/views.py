
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UsuarioForm, PerfilUsuarioForm
from .models import PerfilUsuario, Usuario
from django.contrib.auth.hashers import make_password #encriptar las contraseñas 
from django.contrib.auth.hashers import check_password #verificar las contraseñas
from django.core.mail import send_mail  # Para enviar correos electrónicos
from django.conf import settings  # Configuración del correo
from django.contrib.auth.models import User  # Modelo de usuario predeterminado de Django


# Create your views here.

def sevengamer(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def terror(request):
    return render(request, 'terror.html')

def mundoabierto(request):
    return render(request, 'mundo-abierto.html')

def accion(request):
    return render(request, 'accion.html')

def carreras(request):
    return render(request, 'carreras.html')

def deportes(request):
    return render(request, 'deportes.html')

def rol(request):
    return render(request, 'rol.html')

def residentevil(request):
    return render(request, 'resident-evil-village.html')

def outlast(request):
    return render(request, 'outlast.html')

def deadspace(request):
    return render(request, 'dead-space.html')

def witcher3(request):
    return render(request, 'witcher3.html')

def gta5(request):
    return render(request, 'gta5.html')

def zelda(request):
    return render(request, 'zelda.html')

def assassinscreed(request):
    return render(request, 'assassins-creed.html')

def payday3(request):
    return render(request, 'payday3.html')

def forzahorizon5(request):
    return render(request, 'forza-horizon5.html')

def needforspeed(request):
    return render(request, 'nfs-heat.html')

def granturismo7(request):
    return render(request, 'gran-turismo7.html')

def fifa24(request):
    return render(request, 'fifa24.html')

def nba2k24(request):
    return render(request, 'nba2k24.html')

def efootball(request):
    return render(request, 'efootball2024.html')

def finalfantasy(request):
    return render(request, 'final-fantasy.html')

def baldursgate3(request):
    return render(request, 'baldurs-gate3.html')

def persona5(request):
    return render(request, 'persona5.html')

def admin(request):
    return render(request, 'admin.html')

def panel_admin(request):
    return render(request, 'panel-admin.html')

def panel_usuario(request):
    return render(request, 'panel-usuario.html')

def pago(request):
    return render(request, 'pago.html')

def recuperar_password(request):
    return render(request, 'recuperar_password.html')


def registro(request):
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        if usuario_form.is_valid():
            usuario = usuario_form.save(commit=False)
            
            # Asignar automáticamente el perfil "usuario"
            perfil_usuario, created = PerfilUsuario.objects.get_or_create(rol='usuario')
            usuario.perfil = perfil_usuario
            usuario.save()
            messages.success(request, "¡Registro exitoso! Ya puedes iniciar sesión.")
            return redirect('login')
        else:
            messages.error(request, "Error en el formulario. Por favor, revisa los datos.")
    else:
        usuario_form = UsuarioForm()
    return render(request, 'registro.html', {
        'usuario_form': usuario_form
    })

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            usuario = Usuario.objects.get(nombre_usuario=username)
            if check_password(password, usuario.contraseña):
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nombre'] = usuario.nombre_usuario
                return redirect('home') 
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html')

def recuperar_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Obtén el correo ingresado
        try:
           # Verifica si el correo pertenece a un usuario registrado
            email = email.strip()
            usuario = User.objects.get(email__iexact=email)
            
            # Si el correo existe, muestra un mensaje de éxito
            messages.success(request, 'Se ha enviado un enlace de recuperación a tu correo electrónico.')
        except User.DoesNotExist:
            # Si el correo no está registrado, muestra un mensaje de error
            messages.error(request, 'El correo ingresado no está registrado.')
    
    return render(request, 'recuperar-password.html')