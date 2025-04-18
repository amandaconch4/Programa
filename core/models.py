from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PerfilUsuario(models.Model):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('usuario', 'Usuario')
    ]
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)

    def __str__(self):
        return self.rol
    
class Usuario(models.Model):
    nombre_completo = models.CharField(max_length=200, unique=True)
    nombre_usuario = models.CharField(max_length=200, unique=True)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=300)

    perfil = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name='usuarios')

    def __str__(self):
        return f"{self.nombre_usuario} ({self.perfil.rol})"
    

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


class Venta(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='ventas')
    fecha = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente.nombre_usuario}"

    def actualizar_total(self):
        total = sum(detalle.subtotal for detalle in self.detalles.all())
        self.total = total
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
    


