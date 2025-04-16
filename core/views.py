
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

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

def registro(request):
    if request.method == 'POST':
        nombre_completo_usuario = request.POST.get('nombre_completo_usuario')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmarPassword = request.POST.get('confirmarPassword')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        direccion = request.POST.get('direccion', '') 

        if password != confirmarPassword:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('registro') 
              
        try:
            user = User.objects.create_user(nombre_completo_usuario= nombre_completo_usuario,username=username,
                                             email=email, password=password, confirmarPassword = confirmarPassword,
                                             fecha_nacimiento = fecha_nacimiento, direccion = direccion)
           
            
            messages.success(request, "¡Registro exitoso! Ya puedes iniciar sesión.")
            return redirect('login')  # Después del registro, redirige a la página de login
        except Exception as e:
            messages.error(request, f"Error al crear el usuario: {e}")
            return redirect('registro')  # Si existee un error, redirige al formulario

    return render(request, 'registro.html')
