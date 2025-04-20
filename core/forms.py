from django import forms
from .models import Usuario, PerfilUsuario, Venta, DetalleVenta
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


# Formulario para crear un Usuario
Usuario = get_user_model()

class UsuarioForm(UserCreationForm):  # Usamos UserCreationForm para manejar contraseñas
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nombre_completo', 'password1', 'password2', 'fecha_nacimiento', 'direccion']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),  # Para el campo de fecha
        }
        # Validación para el correo electrónico
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if " " in email:
            raise forms.ValidationError("El correo electrónico no puede contener espacios.")
        if not email.endswith('@dominio.com'):
            raise forms.ValidationError("El correo electrónico debe tener un dominio válido.")
        return email

    # Validación para la contraseña
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6 or len(password1) > 18:
            raise forms.ValidationError("La contraseña debe tener entre 6 y 18 caracteres.")
        if not any(char.isupper() for char in password1):
            raise forms.ValidationError("La contraseña debe contener al menos una mayúscula.")
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError("La contraseña debe contener al menos un número.")
        if not any(char in "!@#$%^&*(),." for char in password1):
            raise forms.ValidationError("La contraseña debe contener al menos un carácter especial.")
        return password1

    # Validación para la confirmación de la contraseña
    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        password1 = self.cleaned_data.get('password1')
        if password2 != password1:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    
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
    
UserModel = get_user_model()

class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        active_users = UserModel._default_manager.filter(
            correo__iexact=email, is_active=True
        )
        return (u for u in active_users if u.has_usable_password())
    


