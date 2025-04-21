document.addEventListener('DOMContentLoaded', () => {
    const passwordInput = document.getElementById('id_new_password1');
    const passwordError = document.getElementById('passwordError');
    const reqLength = document.getElementById('req-length');
    const reqUpper = document.getElementById('req-uppercase');
    const reqNumber = document.getElementById('req-number');
    const reqSpecial = document.getElementById('req-special');

    if (passwordInput) {
        passwordInput.addEventListener('input', function () {
            const value = passwordInput.value;

            validarRequisito(value.length >= 6 && value.length <= 18, reqLength);
            validarRequisito(/[A-Z]/.test(value), reqUpper);
            validarRequisito(/\d/.test(value), reqNumber);
            validarRequisito(/[.,!@#$%^&*]/.test(value), reqSpecial);
        });

        function validarRequisito(condicion, elemento) {
            if (condicion) {
                elemento.classList.remove('invalid');
                elemento.classList.add('valid');
            } else {
                elemento.classList.remove('valid');
                elemento.classList.add('invalid');
            }
        }

        document.getElementById('passwordForm').addEventListener('submit', function (e) {
            const value = passwordInput.value;
            let esValido = true;

            if (!(value.length >= 6 && value.length <= 18) ||
                !/[A-Z]/.test(value) ||
                !/\d/.test(value) ||
                !/[.,!@#$%^&*]/.test(value)) {
                passwordError.textContent = 'La contraseña no cumple con los requisitos.';
                passwordError.style.display = 'block';
                esValido = false;
            }

            if (!esValido) {
                e.preventDefault();
            }
        });
    }

    // Mostrar/ocultar contraseñas
    const toggles = document.querySelectorAll('.toggle-password');
    toggles.forEach(toggle => {
        toggle.addEventListener('click', function () {
            const inputId = this.getAttribute('data-input');
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
        });
    });
});