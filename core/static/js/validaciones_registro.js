// Selección de elementos

const form = document.getElementById('registroForm');

const nombreInput = document.getElementById('id_nombre_completo');
const usernameInput = document.getElementById('id_username');
const emailInput = document.getElementById('id_email');
const password1 = document.getElementById('id_password1');
const fechaNacimiento = document.getElementById('id_fecha_nacimiento');
const direccionInput = document.getElementById('id_direccion');

// Errores

const nombreError = document.getElementById('nombre_completo-error');
const usernameError = document.getElementById('username-error');
const emailError = document.getElementById('email-error');
const password1Error = document.getElementById('password1-error');
const fechaError = document.getElementById('fecha_nacimiento-error');
const direccionError = document.getElementById('direccion-error');

// Requisitos visuales

const reqLength = document.getElementById('req-length');
const reqNumber = document.getElementById('req-number');
const reqSpecial = document.getElementById('req-special');
const reqFormato = document.getElementById('req-email-formato');
const reqSinEspacios = document.getElementById('req-email-sin-espacios');
const reqDominio = document.getElementById('req-email-dominio');
const reqUpper = document.getElementById('req-uppercase');



// VALIDACIÓN VISUAL DE CONTRASEÑA
function validarContraseña(contraseña) {
    const longitud = contraseña.length >= 6 && contraseña.length <= 18;
    const mayuscula = /[A-Z]/.test(contraseña);
    const numero = /\d/.test(contraseña);
    const especial = /[.,!@#$%^&*]/.test(contraseña);

    reqLength.className = longitud ? 'valid' : 'invalid';
    reqUpper.className = mayuscula ? 'valid' : 'invalid';
    reqNumber.className = numero ? 'valid' : 'invalid';
    reqSpecial.className = especial ? 'valid' : 'invalid';

    return longitud && mayuscula && numero && especial;
}


// VALIDACIÓN VISUAL DE EMAIL 
function validarEmailVisual(email) {
    const formatoValido = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    const sinEspacios = !/\s/.test(email);
    const dominioValido = email.endsWith('@') && /^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email.split('@')[1] || '');

    reqFormato.className = formatoValido ? 'valid' : 'invalid';
    reqSinEspacios.className = sinEspacios ? 'valid' : 'invalid';
    reqDominio.className = dominioValido ? 'valid' : 'invalid';

    return formatoValido && sinEspacios && dominioValido;
}

function validarEdad(fecha) {
    const hoy = new Date();
    const cumple = new Date(fecha);
    let edad = hoy.getFullYear() - cumple.getFullYear();
    const m = hoy.getMonth() - cumple.getMonth();
    if (m < 0 || (m === 0 && hoy.getDate() < cumple.getDate())) edad--;
    return edad >= 13;
}

passwordInput.addEventListener('input', () => {
    validarContraseña(passwordInput.value);
    passwordError.textContent = '';
});

emailInput.addEventListener('input', () => {
    validarEmail(emailInput.value);
    emailError.textContent = '';
});

[nombreInput, usernameInput, fechaNacimiento, direccionInput, confirmarPassword].forEach(input => {
    input?.addEventListener('input', () => {
        const span = document.getElementById(input.id.replace('id_', '') + '-error');
        if (span) span.style.display = 'none';
    });
});

form.addEventListener('submit', (e) => {
    let valido = true;

    if (!nombreInput.value.trim()) {
        nombreError.textContent = 'Ingrese su nombre completo';
        nombreError.style.display = 'block';
        valido = false;
    }

    if (!usernameInput.value.trim()) {
        usernameError.textContent = 'Ingrese un nombre de usuario';
        usernameError.style.display = 'block';
        valido = false;
    }

    if (!emailInput.value.trim() || !validarEmail(emailInput.value)) {
        emailError.textContent = 'Revise los requisitos del correo electrónico';
        emailError.style.display = 'block';
        valido = false;
    }

    if (!passwordInput.value.trim() || !validarContraseña(passwordInput.value)) {
        passwordError.textContent = 'Revise los requisitos de la contraseña';
        passwordError.style.display = 'block';
        valido = false;
    }

    if (confirmarPassword.value !== passwordInput.value) {
        confirmarPasswordError.textContent = 'Las contraseñas no coinciden';
        confirmarPasswordError.style.display = 'block';
        valido = false;
    }

    if (!fechaNacimiento.value || !validarEdad(fechaNacimiento.value)) {
        fechaError.textContent = 'Debe tener al menos 13 años';
        fechaError.style.display = 'block';
        valido = false;
    }

    if (!valido) e.preventDefault();
});


// Toggle del ojito
function togglePassword(inputId) {
const input = document.getElementById(inputId);
const icon = document.getElementById(`toggleIcon-${inputId}`);
if (input.type === 'password') {
    input.type = 'text';
    icon.classList.remove('fa-eye');
    icon.classList.add('fa-eye-slash');
} else {
    input.type = 'password';
    icon.classList.remove('fa-eye-slash');
    icon.classList.add('fa-eye');
}
}

/*  // EVENTOS EN TIEMPO REAL

// Mostrar/ocultar contraseña con ícono FontAwesome
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(`toggleIcon-${inputId}`);
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// Validación en tiempo real
const password = document.getElementById('id_password1');
const passwordError = document.getElementById('password1-error');


password.addEventListener('input', function () {
    const value = password.value;


    reqLength.classList.toggle('valid', value.length >= 6 && value.length <= 18);
    reqLength.classList.toggle('invalid', !(value.length >= 6 && value.length <= 18));

    reqUpper.classList.toggle('valid', /[A-Z]/.test(value));
    reqUpper.classList.toggle('invalid', !/[A-Z]/.test(value));

    reqNumber.classList.toggle('valid', /\d/.test(value));
    reqNumber.classList.toggle('invalid', !/\d/.test(value));

    reqSpecial.classList.toggle('valid', /[.,!@#$%^&*]/.test(value));
    reqSpecial.classList.toggle('invalid', !/[.,!@#$%^&*]/.test(value));

    passwordError.textContent = '';
    passwordError.style.display = 'none';
});

 // Limpieza de errores en tiempo real para los demás campos
[nombreInput, usernameInput, fechaNacimiento, direccionInput].forEach(input => {
    if (input) {
        input.addEventListener('input', function() {
            const errorSpan = document.getElementById(input.id.replace('id_', '') + '-error');
            if (errorSpan) {
                errorSpan.textContent = '';
                errorSpan.style.display = 'none';
            }
        });
    }
});

// VALIDACIÓN AL ENVIAR EL FORMULARIO 
-form.addEventListener('submit', function(e) {
    let valido = true;

    // Nombre completo
    if (!nombreInput.value.trim()) {
        nombreError.textContent = 'Por favor, ingrese su nombre completo';
        nombreError.style.display = 'block';
        valido = false;
    }

    // Nombre de usuario
    if (!usernameInput.value.trim()) {
        usernameError.textContent = 'Por favor, ingrese un nombre de usuario';
        usernameError.style.display = 'block';
        valido = false;
    }

    // Email
    if (!emailInput.value.trim()) {
        emailError.textContent = 'Por favor, ingrese un correo electrónico';
        emailError.style.display = 'block';
        valido = false;
    } else if (!validarEmailVisual(emailInput.value)) {
        emailError.textContent = 'Por favor, cumple todos los requisitos del correo electrónico';
        emailError.style.display = 'block';
        valido = false;
    }

    // Contraseña
    if (!password.value.trim()) {
        passwordError.textContent = 'Por favor, ingrese una contraseña';
        passwordError.style.display = 'block';
        valido = false;
    } else if (!validarContraseña(password.value)) {
        passwordError.textContent = 'La contraseña debe cumplir todos los requisitos visuales.';
        passwordError.style.display = 'block';
        valido = false;
    }

    // Fecha de nacimiento
    if (!fechaNacimiento.value.trim()) {
        fechaError.textContent = 'Por favor, seleccione su fecha de nacimiento';
        fechaError.style.display = 'block';
        valido = false;
    } else if (!validarFechaNacimiento(fechaNacimiento.value)) {
        fechaError.textContent = 'Debes tener al menos 13 años y no ser una fecha futura';
        fechaError.style.display = 'block';
        valido = false;
    }

    // Dirección: opcional
    if (direccionInput) {
        direccionError.textContent = '';
        direccionError.style.display = 'none';
    }

    if (!valido) {
        e.preventDefault();
    }
});*/