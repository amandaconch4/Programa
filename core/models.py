from django.db import models

# Create your models here.

class GestionUsuario (models.Model):
    id_usuario = models.CharField(max_length=200)
    rol = models.CharField(max_length=100)
    estado = models.BooleanField(default=True) 

    def __str__(self):
        return f"{self.id_usuario} - {self.rol}"
    
class Usuario (models.Model):
    nombre_completo_usuario = models.CharField(max_length=300, unique=True)
    nombre_usuario = models.CharField(max_length=200, unique=True)
    correo = models.EmailField(max_length=200, unique=True)
    contraseña = models.CharField(max_length=200)
    confir_contraseña = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    dirección = models.CharField(max_length=300)
    gestion = models.ForeignKey(GestionUsuario, on_delete=models.CASCADE, related_name='usuarios')


    def get_name_profile(self):
        return f" {self.nombre_usuario} - Usuario"
    
class Admin (models.Model):
    usuario_administrador = models.CharField(max_length=200, unique=True)
    contraseña = models.CharField(max_length=200)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='administradores')

    def __str__(self):
        return self.usuario_administrador

class Producto (models.Model):
    nombre_producto = models.CharField(max_length=200, unique=True)
    categoria = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre_producto

class Inventario (models.Model):
    producto= models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='inventario')
    stock_minimo = models.PositiveIntegerField()
    estado = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.producto.nombre_producto} - Stock: {self.producto.stock}"

class Ventas (models.Model):
    id_venta = models.CharField(max_length=200, unique=True)
    cliente = models.CharField(max_length=200)
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=100)

    def __str__(self):
        return f"Venta {self.id_venta} - {self.estado}"


class Cliente (models.Model):
    id_cliente = models.CharField(max_length=200, unique=True)
    nombre_cliente = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre_cliente

