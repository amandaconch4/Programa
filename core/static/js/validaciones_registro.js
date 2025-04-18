// Selección de elementos
const form = document.getElementById('registroForm');
const nombreInput = document.getElementById('id_nombre_completo');
const nombreError = document.getElementById('nombre_completo-error');
const usernameInput = document.getElementById('id_nombre_usuario');
const usernameError = document.getElementById('nombre_usuario-error');
const emailInput = document.getElementById('id_correo');
const emailError = document.getElementById('correo-error');
const password = document.getElementById('id_contraseña');
const passwordError = document.getElementById('contraseña-error');
const fechaNacimiento = document.getElementById('id_fecha_nacimiento');
const fechaError = document.getElementById('fecha_nacimiento-error');
const direccionInput = document.getElementById('id_direccion');
const direccionError = document.getElementById('direccion-error');

// VALIDACIÓN VISUAL DE CONTRASEÑA
function validarContraseña(contraseña) {
    const tieneNumero = /[0-9]/.test(contraseña);
    const tieneMayuscula = /[A-Z]/.test(contraseña);
    const longitudCorrecta = contraseña.length >= 6 && contraseña.length <= 18;
    const tieneCaracterEspecial = /[.,!@#$%^&*]/.test(contraseña);

    const reqLength = document.getElementById('req-length');
    const reqNumber = document.getElementById('req-number');
    const reqMayus = document.getElementById('req-mayus');
    const reqSpecial = document.getElementById('req-special');

    if (reqLength) reqLength.classList.toggle('valido', longitudCorrecta);
    if (reqNumber) reqNumber.classList.toggle('valido', tieneNumero);
    if (reqMayus) reqMayus.classList.toggle('valido', tieneMayuscula);
    if (reqSpecial) reqSpecial.classList.toggle('valido', tieneCaracterEspecial);

    return longitudCorrecta && tieneNumero && tieneMayuscula && tieneCaracterEspecial;
}

// VALIDACIÓN VISUAL DE EMAIL 
function validarEmailVisual(email) {
    const formatoValido = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    const sinEspacios = !/\s/.test(email);
    const dominioValido = email.includes('@') && /^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email.split('@')[1] || '');

    const reqFormato = document.getElementById('req-email-formato');
    const reqSinEspacios = document.getElementById('req-email-sin-espacios');
    const reqDominio = document.getElementById('req-email-dominio');

    if (reqFormato) reqFormato.classList.toggle('valido', formatoValido);
    if (reqSinEspacios) reqSinEspacios.classList.toggle('valido', sinEspacios);
    if (reqDominio) reqDominio.classList.toggle('valido', dominioValido);

    return formatoValido && sinEspacios && dominioValido;
}

// VALIDACIÓN DE FECHA DE NACIMIENTO 
function validarFechaNacimiento(valor) {
    const hoy = new Date();
    const fecha = new Date(valor);
    let edad = hoy.getFullYear() - fecha.getFullYear();
    const m = hoy.getMonth() - fecha.getMonth();
    if (m < 0 || (m === 0 && hoy.getDate() < fecha.getDate())) {
        edad--;
    }
    if (fecha > hoy) return false;
    return edad >= 13;
}

// EVENTOS EN TIEMPO REAL
if (password) {
    password.addEventListener('input', function() {
        validarContraseña(password.value);
        passwordError.textContent = '';
        passwordError.style.display = 'none';
    });
}

if (emailInput) {
    emailInput.addEventListener('input', function() {
        validarEmailVisual(emailInput.value);
        emailError.textContent = '';
        emailError.style.display = 'none';
    });
}

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
form.addEventListener('submit', function(e) {
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
});