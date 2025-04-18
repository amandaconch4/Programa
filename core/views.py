
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UsuarioForm, PerfilUsuarioForm
from django.contrib.auth.hashers import make_password #encriptar las contraseñas 

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

def registro(request):
    return render(request, 'registro.html')

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
        perfil_form = PerfilUsuarioForm(request.POST)

        if usuario_form.is_valid() and perfil_form.is_valid():
            # Guardar el usuario
            usuario = usuario_form.save(commit=False)
            # Encriptar la contraseña antes de guardar
            usuario.contraseña = make_password(usuario.contraseña)
            usuario.save()

             # Crear el perfil de usuario
            perfil = perfil_form.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

            messages.success(request, "¡Registro exitoso! Ya puedes iniciar sesión.")
            return redirect('login')  # Después del registro, redirige a la página de login
        else:
            messages.error(request, "Error en el formulario. Por favor, revisa los datos.")
            
    else:
        usuario_form = UsuarioForm()
        perfil_form = PerfilUsuarioForm()


    return render(request, 'registro.html')
