from django import forms
from .models import Usuario, PerfilUsuario, Venta, DetalleVenta, Categoria
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


# Formulario para crear un Usuario
Usuario = get_user_model()

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nombre_completo', 'password1', 'fecha_nacimiento', 'direccion']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'required': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hace los campos obligatorios excepto dirección
        campos_obligatorios = ['username', 'email', 'nombre_completo', 'fecha_nacimiento']
        # Si es para editar, la contraseña NO es obligatoria
        if self.instance and self.instance.pk:
            self.fields['password1'].required = False
        else:
            campos_obligatorios.append('password1')
        for field_name, field in self.fields.items():
            if field_name in campos_obligatorios:
                field.required = True
                field.error_messages = {'required': f'El campo {field.label} es obligatorio'}
            else:
                field.required = False

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            return username
        qs = Usuario.objects.filter(username=username)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("El nombre de usuario ya está en uso.")
        return username

    def clean_nombre_completo(self):
        nombre_completo = self.cleaned_data.get('nombre_completo')
        if not nombre_completo:
            return nombre_completo
        if len(nombre_completo.strip()) < 8:
            raise forms.ValidationError("El nombre completo debe tener al menos 8 caracteres.")
        return nombre_completo

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("El correo electrónico no puede estar vacío")
        if " " in email:
            raise forms.ValidationError("El correo electrónico no puede contener espacios.")
        import re
        dominio_valido = re.match(r'^[^\s@]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
        if not dominio_valido:
            raise forms.ValidationError("El correo electrónico debe tener un dominio válido.")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        # Si se quiere editar y no se ingresa una nueva contraseña, permite dejarlo vacío
        if self.instance and self.instance.pk and not password1:
            return None
        if not password1:
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

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')

        if password:
            user.set_password(password)
        else:
            # Recupera el hash original directamente desde la base de datos
            if user.pk:
                from core.models import Usuario
                original = Usuario.objects.get(pk=user.pk)
                user.password = original.password

        if commit:
            user.save()
        return user
    
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
    
# Formulario para crear y editar Categorías
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre_categoria', 'juegos']
        widgets = {
            'nombre_categoria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría', 'minlength': 3}),
            'juegos': forms.SelectMultiple(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['juegos'].required = False

    def clean_nombre_categoria(self):
        nombre_categoria = self.cleaned_data.get('nombre_categoria')
        if not nombre_categoria:
            raise forms.ValidationError("El nombre de la categoría no puede estar vacío")
        
        # Eliminar espacios al inicio y al final
        nombre_categoria = nombre_categoria.strip()
        
        if len(nombre_categoria) < 3:
            raise forms.ValidationError("El nombre de la categoría debe tener al menos 3 caracteres")
        
        # Verificar que solo contenga letras y espacios
        if not all(char.isalpha() or char.isspace() for char in nombre_categoria):
            raise forms.ValidationError("El nombre de la categoría solo puede contener letras")
        
        # Verificar que no sean solo espacios
        if nombre_categoria.isspace():
            raise forms.ValidationError("El nombre de la categoría no puede ser solo espacios")
        
        # Convertir a título para mantener consistencia
        nombre_categoria = nombre_categoria.title()
        
        # Verificar si ya existe la categoría, excluyendo la categoría actual en caso de edición
        categoria_existente = Categoria.objects.filter(nombre_categoria=nombre_categoria)
        
        # Si estamos editando, excluir la categoría actual
        if self.instance and self.instance.pk:
            categoria_existente = categoria_existente.exclude(pk=self.instance.pk)
        
        if categoria_existente.exists():
            raise forms.ValidationError("Ya existe una categoría con este nombre")
        
        return nombre_categoria

