// Selección de elementos
const form = document.getElementById('registroForm');

const nombreInput = document.getElementById('id_nombre_completo');
const usernameInput = document.getElementById('id_username');
const emailInput = document.getElementById('id_email');
const passwordInput = document.getElementById('id_password1');
const fechaNacimiento = document.getElementById('id_fecha_nacimiento');
const direccionInput = document.getElementById('id_direccion');

// Errores
const nombreError = document.getElementById('nombre_completo-error');
const usernameError = document.getElementById('nombre_usuario-error');
const emailError = document.getElementById('correo-error');
const passwordError = document.getElementById('password1-error');
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
const reqNombreLongitud = document.getElementById('req-nombre-length');
const reqUsernameLongitud = document.getElementById('req-username-length');
const reqUsernameSinEspacios = document.getElementById('req-username-sin-espacios');


// VALIDACIÓN VISUAL DE NOMBRE COMPLETO
function validarNombreCompleto(nombre) {
    // Trim para quitar espacios al inicio y final
    nombre = nombre.trim();
    
    // Validaciones individuales
    const longitud = nombre.length >= 8

    // Actualizar clases visuales
    reqNombreLongitud.className = nombre ? (longitud ? 'valido' : 'invalid') : '';

    // Retornar validación completa
    return nombre && longitud;
}

// VALIDACIÓN VISUAL DE USERNAME
function validarUsername(username) {
    // Trim para quitar espacios al inicio y final
    username = username.trim();
    
    // Validaciones individuales
    const longitud = username.length >= 5 && username.length <= 15;
    const sinEspacios = username.indexOf(' ') === -1;

    // Actualizar clases visuales
    reqUsernameLongitud.className = username ? (longitud ? 'valido' : 'invalid') : '';
    reqUsernameSinEspacios.className = username ? (sinEspacios ? 'valido' : 'invalid') : '';

    // Retornar validación completa
    return username && longitud && sinEspacios;
}

// VALIDACIÓN VISUAL DE CONTRASEÑA
function validarContraseña(contraseña) {
    // Validaciones individuales
    const longitud = contraseña.length >= 6 && contraseña.length <= 18;
    const mayuscula = /[A-Z]/.test(contraseña);
    const numero = /\d/.test(contraseña);
    const especial = /[.,!@#$%^&*]/.test(contraseña);

    // Actualizar clases visuales
    reqLength.className = contraseña ? (longitud ? 'valido' : 'invalid') : '';
    reqUpper.className = contraseña ? (mayuscula ? 'valido' : 'invalid') : '';
    reqNumber.className = contraseña ? (numero ? 'valido' : 'invalid') : '';
    reqSpecial.className = contraseña ? (especial ? 'valido' : 'invalid') : '';

    // Retornar validación completa
    return contraseña && longitud && mayuscula && numero && especial;
}

// VALIDACIÓN VISUAL DE EMAIL 
function validarEmail(email) {
    // Trim para quitar espacios al inicio y final
    email = email.trim();
    
    // Validaciones individuales
    const formatoValido = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    const sinEspacios = email.indexOf(' ') === -1;
    const dominioValido = email.includes('@') && /^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email.split('@')[1] || '');

    // Actualizar clases visuales
    reqFormato.className = email ? (formatoValido ? 'valido' : 'invalid') : '';
    reqSinEspacios.className = email ? (sinEspacios ? 'valido' : 'invalid') : '';
    reqDominio.className = email ? (dominioValido ? 'valido' : 'invalid') : '';

    // Retornar validación completa
    return email && formatoValido && sinEspacios && dominioValido;
}

function validarEdad(fecha) {
    const hoy = new Date();
    const cumple = new Date(fecha);
    let edad = hoy.getFullYear() - cumple.getFullYear();
    const m = hoy.getMonth() - cumple.getMonth();
    if (m < 0 || (m === 0 && hoy.getDate() < cumple.getDate())) edad--;
    return edad >= 13;
}

// Eventos de validación en tiempo real

nombreInput.addEventListener('input', () => {
    validarNombreCompleto(nombreInput.value);
    nombreError.textContent = '';
});

usernameInput.addEventListener('input', () => {
    validarUsername(usernameInput.value);
    usernameError.textContent = '';
});

passwordInput.addEventListener('input', () => {
    validarContraseña(passwordInput.value);
    passwordError.textContent = '';
});

emailInput.addEventListener('input', () => {
    validarEmail(emailInput.value);
    emailError.textContent = '';
});

[nombreInput, usernameInput, fechaNacimiento, direccionInput].forEach(input => {
    input?.addEventListener('input', () => {
        const span = document.getElementById(input.id.replace('id_', '') + '-error');
        if (span) span.style.display = 'none';
    });
});

// Validación al enviar el formulario
form.addEventListener('submit', (e) => {
    let valido = true;

    if (!nombreInput.value.trim() || !validarNombreCompleto(nombreInput.value)) {
        nombreError.textContent = 'Ingrese un nombre completo válido';
        nombreError.style.display = 'block';
        valido = false;
    }

    if (!nombreInput.value.trim()) {
        nombreError.textContent = 'Ingrese su nombre completo';
        nombreError.style.display = 'block';
        valido = false;
    }

    if (!usernameInput.value.trim() || !validarUsername(usernameInput.value)) {
        usernameError.textContent = 'Ingrese un nombre de usuario válido';
        usernameError.style.display = 'block';
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

    if (!fechaNacimiento.value || !validarEdad(fechaNacimiento.value)) {
        fechaError.textContent = 'Debe tener al menos 13 años';
        fechaError.style.display = 'block';
        valido = false;
    }

    if (!valido) e.preventDefault();
});

// Toggle del ojo
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