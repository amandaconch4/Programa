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
        fields = ['username', 'email', 'nombre_completo', 'password1', 'fecha_nacimiento', 'direccion']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),  # Para el campo de fecha
            'direccion': forms.TextInput(attrs={'required': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hace los campos obligatorios excepto dirección
        campos_obligatorios = ['username', 'email', 'nombre_completo', 'password1', 'fecha_nacimiento']
        for field_name, field in self.fields.items():
            if field_name in campos_obligatorios:
                field.required = True
                field.error_messages = {'required': f'El campo {field.label} es obligatorio'}
            else:
                field.required = False

    def clean(self):
        cleaned_data = super().clean()
        print("Cleaned data:", cleaned_data)
        
        # Validaciones adicionales para campos obligatorios
        campos_obligatorios = ['username', 'email', 'nombre_completo', 'password1', 'fecha_nacimiento']
        for field in campos_obligatorios:
            value = cleaned_data.get(field)
            if value is None or value == '':
                print(f"Campo {field} está vacío o None")
                # Solo añade el error si no hay errores previos para este campo
                if not self.errors.get(field):
                    self.add_error(field, f'El campo {field} no puede estar vacío')
        
        return cleaned_data

    def clean_nombre_completo(self):
        nombre_completo = self.cleaned_data.get('nombre_completo')
        
        # Si el campo está vacío, no hace nada (para eso está el general)
        if not nombre_completo:
            return nombre_completo
        
        # Validar longitud mínima de 8 caracteres
        if len(nombre_completo.strip()) < 8:
            raise forms.ValidationError("El nombre completo debe tener al menos 8 caracteres.")
        
        return nombre_completo

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            print("Email está vacío")
            raise forms.ValidationError("El correo electrónico no puede estar vacío")
        
        if " " in email:
            raise forms.ValidationError("El correo electrónico no puede contener espacios.")
        
        # Validación de dominio más flexible
        import re
        dominio_valido = re.match(r'^[^\s@]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
        if not dominio_valido:
            raise forms.ValidationError("El correo electrónico debe tener un dominio válido.")
        
        return email

    # Validación para la contraseña
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if not password1:
            print("Contraseña está vacía")
            raise forms.ValidationError("La contraseña no puede estar vacía")
        
        if len(password1) < 6 or len(password1) > 18:
            raise forms.ValidationError("La contraseña debe tener entre 6 y 18 caracteres.")
        if not any(char.isupper() for char in password1):
            raise forms.ValidationError("La contraseña debe contener al menos una mayúscula.")
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError("La contraseña debe contener al menos un número.")
        if not any(char in "!@#$%^&*(),." for char in password1):
            raise forms.ValidationError("La contraseña debe contener al menos un carácter especial.")
        return password1

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion', '')
        return direccion  # Permitir que sea opcional y vacío
    
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
    


