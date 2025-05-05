from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import PerfilUsuario, Usuario, Venta, Juego, DetalleVenta,Carrito, CarritoItem, Categoria
from django.contrib.auth.hashers import check_password 
from django.core.mail import send_mail  
from django.conf import settings 
from django.contrib.auth.models import User  
from .forms import UsuarioForm, PerfilUsuarioForm, CategoriaForm
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q 
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import VentaSerializer, DetalleVentaSerializer
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.urls import reverse 
from django.db.models.deletion import ProtectedError


# Create your views here.

def sevengamer(request):
    if request.user.is_authenticated:
        messages.success(request, f'¡Bienvenid@ {request.user.username}!')
    
    # Muestra las categorías creadas en la base de datos
    categorias_dinamicas = Categoria.objects.all()
    
    return render(request, 'index.html', {'categorias_dinamicas': categorias_dinamicas})

def index(request):
    # Muestra las categorías creadas en la base de datos
    categorias_dinamicas = Categoria.objects.all()
    
    return render(request, 'index.html', {'categorias_dinamicas': categorias_dinamicas})

def terror(request):
    # Muestra las categorías creadas en la base de datos
    categorias_dinamicas = Categoria.objects.all()
    return render(request, 'terror.html', {'categorias_dinamicas': categorias_dinamicas})

def mundoabierto(request):
    # Muestra las categorías creadas en la base de datos
    categorias_dinamicas = Categoria.objects.all()
    return render(request, 'mundo-abierto.html', {'categorias_dinamicas': categorias_dinamicas})

def accion(request):
    # Muestra las categorías creadas en la base de datos
    categorias_dinamicas = Categoria.objects.all()
    return render(request, 'accion.html', {'categorias_dinamicas': categorias_dinamicas})

def carreras(request):
    # Muestra las categorías creadas en la base de datos
    categorias_dinamicas = Categoria.objects.all()
    return render(request, 'carreras.html', {'categorias_dinamicas': categorias_dinamicas})

def deportes(request):
    # Muestra las categorías creadas en la base de datos
    categorias_dinamicas = Categoria.objects.all()
    return render(request, 'deportes.html', {'categorias_dinamicas': categorias_dinamicas})

def rol(request):
    # Muestra las categorías creadas en la base de datos
    categorias_dinamicas = Categoria.objects.all()
    return render(request, 'rol.html', {'categorias_dinamicas': categorias_dinamicas})

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


@login_required
def pago(request):
    return render(request, 'pago.html')

def recuperar_password(request):
    if request.method == 'POST':
        email = request.POST.get('email') 
        try:
           
            email = email.strip()
            User = get_user_model()
            usuario = User.objects.get(email__iexact=email)
            
           
            messages.success(request, 'Se ha enviado un enlace de recuperación a tu correo electrónico.')
        except User.DoesNotExist:
            
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
            perfil_usuario = PerfilUsuario.objects.filter(rol='usuario').first()
            if perfil_usuario is None:
                perfil_usuario = PerfilUsuario.objects.create(rol='usuario')

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

    # Categorias
    categorias = Categoria.objects.all()

    return render(request, 'panel-admin.html', {
        'usuarios': usuarios,
        'clientes': clientes,
        'categorias': categorias
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

@login_required
def agregar_cliente(request):
    if not request.user.is_staff:
        messages.error(request, 'No tienes permiso para agregar clientes.')
        return redirect('panel_admin')

    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        if usuario_form.is_valid():
            usuario = usuario_form.save(commit=False)
            perfil_cliente = PerfilUsuario.objects.get(rol='usuario')
            usuario.perfil = perfil_cliente
            usuario.is_staff = False
            usuario.is_superuser = False
            usuario.save()
            messages.success(request, f"Cliente {usuario.username} creado exitosamente.")
            return redirect('panel_admin')
        else:
            messages.error(request, "Error en el formulario. Por favor, revisa los datos.")
    else:
        usuario_form = UsuarioForm()

    return render(request, 'agregar_cliente.html', {
        'usuario_form': usuario_form
    })



# Vistas para el carrito de compras  ********


# Obtener o crear el carrito del usuario
def get_carrito(usuario):
    carrito, creado = Carrito.objects.get_or_create(
        usuario=usuario,
        estado='activo'  # Especificamos explícitamente el estado
    )
    return carrito
# Agregar juego al carrito

@csrf_exempt
@login_required
def carrito_agregar(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            carrito_items = data.get('carrito', [])

            if not carrito_items:
                return JsonResponse({'success': False, 'error': 'Carrito vacío'})

            carrito, _ = Carrito.objects.get_or_create(usuario=request.user, estado='activo')
            carrito.items.all().delete()  # Limpiar carrito anterior

            for item in carrito_items:
                juego_id = item.get('id')
                cantidad = item.get('cantidad', 1)

                try:
                    juego = Juego.objects.get(id=juego_id)
                    CarritoItem.objects.create(
                        carrito=carrito,
                        juego=juego,
                        cantidad=cantidad
                    )
                except Juego.DoesNotExist:
                    continue

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

# Ver el contenido del carrito
@login_required
def ver_carrito(request):
    carrito = get_carrito(request.user)
    items = carrito.items.all()
    total = carrito.total()
    return render(request, 'ver_carrito.html', {
        'items': items,
        'total': total
    })

@csrf_exempt
@login_required
def carrito_agregar(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            carrito_items = data.get('carrito', [])

            if not carrito_items:
                return JsonResponse({'success': False, 'error': 'Carrito vacío'})

            carrito, _ = Carrito.objects.get_or_create(usuario=request.user, estado='activo')
            carrito.items.all().delete()  # Limpiar carrito anterior

            for item in carrito_items:
                juego_id = item.get('id')
                cantidad = item.get('cantidad', 1)

                try:
                    juego = Juego.objects.get(id=juego_id)
                    CarritoItem.objects.create(
                        carrito=carrito,
                        juego=juego,
                        cantidad=cantidad
                    )
                except Juego.DoesNotExist:
                    continue

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

@csrf_exempt
@login_required
def guardar_carrito_items(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("📦 Datos recibidos:", data)

            carrito_data = data.get('carrito', [])
            if not carrito_data:
                return JsonResponse({'error': 'Carrito vacío'}, status=400)

            carrito = get_carrito(request.user)

            for item in carrito_data:
                print("🎮 Procesando item:", item)
                juego_id = item.get('id')
                cantidad = item.get('cantidad', 1)

                juego = Juego.objects.get(id=juego_id)
                carrito_item, creado = CarritoItem.objects.get_or_create(
                    carrito=carrito,
                    juego=juego,
                    defaults={'cantidad': cantidad}
                )
                if not creado:
                    carrito_item.cantidad += cantidad
                    carrito_item.save()

            return JsonResponse({'success': True})

        except Exception as e:
            import traceback
            print("⛔ ERROR DETECTADO:")
            traceback.print_exc()
            print("🔧 Error:", str(e))
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)



# Vistas para realizar la compra  ********  

from django.http import HttpResponseBadRequest

@csrf_exempt
@login_required
def procesar_pago(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Datos JSON inválidos.")

        # Capturar los datos del cuerpo JSON
        card_type = data.get('cardType')
        card_name = data.get('cardName')
        card_number = data.get('cardNumber')
        expiry_date = data.get('expiryDate')
        cvv = data.get('cvv')

        # Validar los datos del formulario
        if not all([card_type, card_name, card_number, expiry_date, cvv]):
            return HttpResponseBadRequest("Faltan algunos campos obligatorios.")

        # Buscar el carrito activo del usuario
        carrito = Carrito.objects.filter(usuario=request.user, estado='activo').first()
        if not carrito:
            # Si no hay carrito, redirigir igual (por ejemplo, por segunda compra)
            return JsonResponse({
                'success': True,
                'redirect_url': reverse('index')  # Cambia 'index' si tu vista principal tiene otro nombre
            })

        # Crear la venta
        venta = Venta.objects.create(cliente=request.user, carrito=carrito)

        # Crear los detalles de la venta
        for item in carrito.items.all():
            DetalleVenta.objects.create(
                venta=venta,
                juego=item.juego,
                cantidad=item.cantidad,
                subtotal=item.subtotal()
            )

        # Actualizar el total
        venta.actualizar_total()

        # Finalizar el carrito y vaciarlo
        carrito.estado = 'finalizado'
        carrito.save()
        carrito.items.all().delete()

        return JsonResponse({
            'success': True,
            'redirect_url': reverse('index')  # Reemplaza 'index' si es necesario
        })

    return JsonResponse({'error': 'Método no permitido'}, status=405)

#**************

@login_required
def compra_exitosa(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id, cliente=request.user)
    return render(request, 'compra_exitosa', {'venta': venta})

#-----------------------------------

@login_required
def historial_compras(request):
     ventas = Venta.objects.filter(cliente=request.user).order_by('-fecha')
     return render(request, 'historial_compras.html', {'ventas': ventas})

@login_required
def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id, cliente=request.user)
    return render(request, 'detalle_venta.html', {'venta': venta})






# API rest ------------------------------------------
@api_view(['POST'])
@login_required
def procesar_pago_api(request):
    if request.method == 'POST':
        # Validar los datos recibidos en la API
        serializer = VentaSerializer(data=request.data)
        
        if serializer.is_valid():
            # Crear la venta
            venta = serializer.save(cliente=request.user)
            
            # Actualizar el total de la venta
            venta.actualizar_total()

            # Limpiar el carrito después de la compra
            request.session['carrito'] = []

            return Response({
                'message': 'Pago procesado con éxito',
                'venta_id': venta.id,
                'total': venta.total
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
@login_required
def historial_compras_api(request):
    ventas = Venta.objects.filter(cliente=request.user).order_by('-fecha')
    serializer = VentaSerializer(ventas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@login_required
def detalles_venta_api(request, venta_id):
    try:
        venta = Venta.objects.get(id=venta_id, cliente=request.user)
        detalles = DetalleVenta.objects.filter(venta=venta)
        serializer = DetalleVentaSerializer(detalles, many=True)
        return Response(serializer.data)
    except Venta.DoesNotExist:
        return Response({'error': 'Venta no encontrada'}, status=status.HTTP_404_NOT_FOUND)


# CRUD de Categorías
@login_required
def listar_categorias(request):
    if not request.user.is_staff:
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('sevengamer')
    
    categorias = Categoria.objects.all()
    return render(request, 'panel-admin.html', {'categorias': categorias})

@login_required
def agregar_categoria(request):
    if not request.user.is_staff:
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('sevengamer')
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría agregada exitosamente.')
            return redirect('listar_categorias')
    else:
        form = CategoriaForm()
    
    return render(request, 'agregar_categoria.html', {'form': form})

@login_required
def editar_categoria(request, categoria_id):
    if not request.user.is_staff:
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('sevengamer')
    
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría editada exitosamente.')
            return redirect('listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    
    return render(request, 'editar_categoria.html', {'form': form, 'categoria': categoria})

@login_required
def eliminar_categoria(request, categoria_id):
    # Verificar si el usuario tiene permisos de administrador
    if not request.user.is_staff:
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('sevengamer')
    
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    if request.method == 'POST':
        try:
            # Verificar si hay juegos asociados
            juegos_asociados = categoria.juegos.count()
            if juegos_asociados > 0:
                messages.error(request, f'No se puede eliminar la categoría. Hay {juegos_asociados} juego(s) asociados.')
                return redirect('listar_categorias')
            
            # Eliminar la categoría
            categoria.delete()
            messages.success(request, f'La categoría "{categoria.nombre_categoria}" ha sido eliminada exitosamente.')
        except ProtectedError:
            messages.error(request, 'No se puede eliminar la categoría debido a restricciones de integridad.')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar la categoría: {str(e)}')
        
        return redirect('listar_categorias')
    
    # Si no es POST, redirigir al panel de admin
    return redirect('listar_categorias')

@login_required
def verificar_categoria(request):
    nombre = request.GET.get('nombre', '').strip().title()
    
    if not nombre:
        return JsonResponse({'existe': False})
    
    existe = Categoria.objects.filter(nombre_categoria=nombre).exists()
    return JsonResponse({'existe': existe})

def categoria_dinamica(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    juegos = categoria.juegos.all()
    categorias_dinamicas = Categoria.objects.all()
    
    context = {
        'categoria': categoria,
        'juegos': juegos,
        'categorias_dinamicas': categorias_dinamicas
    }
    
    return render(request, 'categoria_dinamica.html', context)