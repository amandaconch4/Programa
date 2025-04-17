from django import forms
from .models import Usuario, PerfilUsuario, Juego, Venta, DetalleVenta
from django.contrib.auth.hashers import make_password

# Formulario para crear un Usuario
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre_completo', 'nombre_usuario', 'correo', 'contraseña', 'fecha_nacimiento', 'direccion', 'perfil']

    # Método para encriptar la contraseña
    def save(self, commit=True):
        usuario = super().save(commit=False)
        if usuario.contraseña:
            usuario.contraseña = make_password(usuario.contraseña)
        if commit:
            usuario.save()
        return usuario

# Formulario para crear un perfil de usuario (rol)
class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['rol']

# Formulario para crear una Venta
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente']

# Formulario para crear los detalles de la venta (productos)
class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['venta', 'juego', 'cantidad']

    # Calcular el subtotal automáticamente al guardar
    def save(self, *args, **kwargs):
        detalle_venta = super().save(commit=False)
        detalle_venta.subtotal = detalle_venta.juego.precio * detalle_venta.cantidad
        detalle_venta.save()
        return detalle_venta