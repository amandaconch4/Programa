from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import PerfilUsuario, Usuario, Venta, Juego, DetalleVenta
from django.contrib.auth.hashers import check_password #verificar las contraseñas
from django.core.mail import send_mail  # Para enviar correos electrónicos
from django.conf import settings  # Configuración del correo
from django.contrib.auth.models import User  # Modelo de usuario predeterminado de Django
from core.models import Usuario
from .forms import UsuarioForm, PerfilUsuarioForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q 
from django.contrib.auth import logout
from django.http import JsonResponse

# Create your views here.

def sevengamer(request):
    if request.user.is_authenticated:
        messages.success(request, f'¡Bienvenid@ {request.user.username}!')
    return render(request, 'index.html')

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
    if request.method == 'POST':
        email = request.POST.get('email') 
        try:
           # Verifica si el correo pertenece a un usuario registrado
            email = email.strip()
            User = get_user_model()
            usuario = User.objects.get(email__iexact=email)
            
            # Si el correo existe, muestra un mensaje de éxito
            messages.success(request, 'Se ha enviado un enlace de recuperación a tu correo electrónico.')
        except User.DoesNotExist:
            # Si el correo no está registrado, muestra un mensaje de error
            messages.error(request, 'El correo ingresado no está registrado.')
    
    return render(request, 'recuperar_password.html')


@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    return redirect('sevengamer')

@login_required
def mi_cuenta(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'mi_cuenta.html')

def actualizar_perfil(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.nombre_completo = request.POST.get('nombre_completo')
        user.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        user.direccion = request.POST.get('direccion')
        user.save()
        messages.success(request, 'Perfil actualizado correctamente')
        return redirect('mi_cuenta')
    
    return redirect('mi_cuenta')

def actualizar_foto(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST' and request.FILES.get('profile_photo'):
        user = request.user
        user.profile_photo = request.FILES['profile_photo']
        user.save()
        messages.success(request, 'Foto de perfil actualizada correctamente')
    
    return redirect('mi_cuenta')

def registro(request):
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        if usuario_form.is_valid():
            usuario = usuario_form.save(commit=False)
            # Asigna el perfil de usuario normal (rol='usuario')
            perfil_usuario = PerfilUsuario.objects.get(rol='usuario')
            usuario.perfil = perfil_usuario
            usuario.save()
            messages.success(request, "¡Registro exitoso! Ya puedes iniciar sesión.")
            return redirect('login')
        else:
            # Limpia mensajes anteriores de error
            storage = messages.get_messages(request)
            storage.used = True
            messages.error(request, "Error en el formulario. Por favor, revisa los datos.")
    else:
        usuario_form = UsuarioForm()
    return render(request, 'registro.html', {
        'usuario_form': usuario_form
    })

def login(request):
    if request.user.is_authenticated:
        return redirect('sevengamer')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Verificar si el usuario existe
        try:
            user_obj = Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            messages.error(request, 'El usuario no existe')
            return render(request, 'login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            
            if request.POST.get('remember-me'):
                request.session.set_expiry(1209600)  # 2 semanas
            else:
                request.session.set_expiry(0) 
            
            return redirect('sevengamer')
        else:
            # Verificar si la contraseña es incorrecta
            from django.contrib.auth.hashers import check_password
            try:
                if check_password(password, user_obj.password):
                    messages.error(request, 'Error de autenticación. Contacte al administrador.')
                else:
                    messages.error(request, 'Contraseña incorrecta')
            except Exception as e:
                messages.error(request, 'Error al verificar contraseña')
    
    return render(request, 'login.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('admin-username')
        password = request.POST.get('admin-password')
        
        # Autenticar usando Django's authentication
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff and user.is_superuser:
            # Si es un administrador válido, iniciar sesión
            auth_login(request, user)
            return redirect('panel_admin')
        else:
            # Si las credenciales son inválidas
            messages.error(request, 'Credenciales de administrador incorrectas')
    
    return render(request, 'admin.html')

@login_required
def panel_admin(request):
    # Verificar si el usuario es un administrador
    if not request.user.is_staff or not request.user.is_superuser:
        messages.error(request, 'No tienes permiso para acceder al panel de administración.')
        return redirect('admin')  # Redirigir al login de admin

    # Usuarios admin y superusuarios (como ya tienes)
    usuarios = Usuario.objects.filter(
        Q(perfil__rol='admin') | Q(is_superuser=True)
    ).distinct()

    # SOLO clientes (perfil_id = 1)
    clientes = Usuario.objects.filter(perfil_id=1)

    return render(request, 'panel-admin.html', {
        'usuarios': usuarios,
        'clientes': clientes,
    })

@login_required
def agregar_admin(request):
    # Verifica si el usuario es un administrador
    if not request.user.is_staff or not request.user.is_superuser:
        messages.error(request, 'No tienes permiso para agregar administradores.')
        return redirect('admin')
    
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        if usuario_form.is_valid():
            usuario = usuario_form.save(commit=False)
            # Asigna el perfil de admin (rol='admin')
            perfil_admin = PerfilUsuario.objects.get(rol='admin')
            usuario.perfil = perfil_admin
            usuario.is_staff = True
            usuario.is_superuser = True
            usuario.save()
            messages.success(request, f"Administrador {usuario.username} creado exitosamente.")
            return redirect('panel_admin')
        else:
            messages.error(request, "Error en el formulario. Por favor, revisa los datos.")
    else:
        usuario_form = UsuarioForm()
    
    return render(request, 'agregar_admin.html', {
        'usuario_form': usuario_form
    })

@login_required
def eliminar_admin(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permiso para eliminar administradores.')
        return redirect('panel_admin')

    try:
        usuario = Usuario.objects.get(id=user_id)

        # Verifica que el usuario tenga perfil y que sea admin
        if usuario.perfil and usuario.perfil.rol == 'admin':
            usuario.delete()
            messages.success(request, f'Administrador {usuario.username} eliminado exitosamente.')
        else:
            messages.error(request, 'Solo puedes eliminar administradores con perfil asignado.')
    except Usuario.DoesNotExist:
        messages.error(request, 'El administrador no existe.')

    return redirect('panel_admin')

@login_required
def editar_admin(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id, perfil__rol='admin')
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Administrador actualizado correctamente.')
            return redirect('panel_admin')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'editar_admin.html', {'form': form, 'usuario': usuario})

@login_required
def confirmar_eliminacion(request):
    return render(request, 'confirmar_eliminacion_cta_usuario.html')

@login_required
def eliminar_cuenta(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
   
        return render(request, 'eliminar_cuenta.html')

    return redirect('mi_cuenta')

@login_required
def editar_cliente(request, user_id):
    cliente = get_object_or_404(Usuario, id=user_id, perfil_id=1)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('panel_admin')
    else:
        form = UsuarioForm(instance=cliente)
    return render(request, 'editar-cliente.html', {'form': form, 'cliente': cliente})

@login_required
def eliminar_cliente(request, user_id):
    cliente = get_object_or_404(Usuario, id=user_id, perfil_id=1)
    cliente.delete()
    messages.success(request, 'Cliente eliminado correctamente.')
    return redirect('panel_admin')