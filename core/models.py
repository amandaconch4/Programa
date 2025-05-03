from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings




class PerfilUsuario(models.Model):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('usuario', 'Usuario')
    ]
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)

    def __str__(self):
        return self.rol
    
class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    nombre_completo = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField(null=True)
    direccion = models.CharField(max_length=300, blank=True)
    perfil = models.ForeignKey('PerfilUsuario', on_delete=models.CASCADE, related_name='usuarios', null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'nombre_completo']
    
    def __str__(self):
        return f"{self.username} ({self.get_rol_display() if self.perfil else 'No role'})"
    
    def get_rol_display(self):
        return self.perfil.get_rol_display() if self.perfil else 'No role'
    

class Juego (models.Model):
    nombre_juego = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.nombre_juego

class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=100, unique=True)
    juegos = models.ManyToManyField(Juego, related_name='categorias')

    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='activo') 

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.juego.precio * self.cantidad


class Venta(models.Model):
    cliente = models.ForeignKey( settings.AUTH_USER_MODEL,  # <- esta es la forma correcta
        on_delete=models.CASCADE,
        related_name='ventas',
        null=True,
        blank=True
    )
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='ventas', null=True, blank=True)  # Agregamos la relación con Carrito
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def actualizar_total(self):
        self.total = sum(detalle.subtotal for detalle in self.detalles.all())
        self.save()


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.juego.nombre} x {self.cantidad}"

    def save(self, *args, **kwargs):
        # Calcula el subtotal automáticamente
        self.subtotal = self.juego.precio * self.cantidad
        super().save(*args, **kwargs)
    
