document.addEventListener('DOMContentLoaded', () => {
    cargarResumenCarrito();
    configurarFormularioPago();
});

function formatearPrecio(precio) {
    return precio.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

function cargarResumenCarrito() {
    const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    const cartSummaryElement = document.getElementById('cartSummary');
    const totalAmountElement = document.getElementById('totalAmount');
    let total = 0;

    cartSummaryElement.innerHTML = '';
    carrito.forEach(item => {
        const subtotal  = item.precio * item.cantidad;
        total += subtotal;

        const itemElement = document.createElement('div');
        itemElement.className = 'cart-item';
        itemElement.innerHTML = `
            <img src="${item.imagen}" alt="${item.nombre}">
            <div class="cart-item-details">
                <h3>${item.nombre}</h3>
                <p>Cantidad: ${item.cantidad}</p>
                <p>Precio unitario: $${formatearPrecio(item.precio)}</p>
                <p>Subtotal: $${formatearPrecio(subtotal)}</p>
            </div>
        `;

        cartSummaryElement.appendChild(itemElement);
    });

    totalAmountElement.textContent = `Total a pagar: $${formatearPrecio(total)}`;
}

function crearMensajeError(input) {
    let errorDiv = input.parentNode.querySelector('.error-message');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        input.parentNode.appendChild(errorDiv);
    }
    return errorDiv;
}

function configurarFormularioPago() {
    const form = document.getElementById('paymentForm');
    
    const cardTypeSelect = document.getElementById('cardType');
    const cardTypeError = crearMensajeError(cardTypeSelect);
    const cardNameInput = document.getElementById('cardName');
    const cardNameError = crearMensajeError(cardNameInput);
    const cardNumberInput = document.getElementById('cardNumber');
    const cardNumberError = crearMensajeError(cardNumberInput);
    const expiryDateInput = document.getElementById('expiryDate');
    const expiryError = crearMensajeError(expiryDateInput);
    const cvvInput = document.getElementById('cvv');
    const cvvError = crearMensajeError(cvvInput);

    cardTypeSelect.addEventListener('change', () => {
        if (cardTypeSelect.value) cardTypeError.textContent = '';
    });

    cardNameInput.addEventListener('input', () => {
        if (cardNameInput.value.trim()) cardNameError.textContent = '';
    });

    cardNumberInput.addEventListener('input', (e) => {
        let value = e.target.value.replace(/\D/g, '').slice(0, 16);
        e.target.value = value.replace(/(.{4})/g, '$1 ').trim();
        cardNumberError.textContent = value.length === 16 ? '' : 'Debe tener 16 dígitos';
    });

    expiryDateInput.addEventListener('input', (e) => {
        let value = e.target.value.replace(/\D/g, '').slice(0, 4);
        if (value.length >= 2) value = value.slice(0, 2) + '/' + value.slice(2);
        e.target.value = value;

        expiryError.textContent = '';
        if (value.length === 5) {
            const [m, y] = value.split('/');
            const month = parseInt(m), year = parseInt(y);
            const date = new Date();
            const nowYear = date.getFullYear() % 100, nowMonth = date.getMonth() + 1;

            if (month < 1 || month > 12) expiryError.textContent = 'Mes inválido';
            else if (year < nowYear || (year === nowYear && month < nowMonth)) expiryError.textContent = 'Tarjeta vencida';
        }
    });

    cvvInput.addEventListener('input', (e) => {
        const value = e.target.value.replace(/\D/g, '').slice(0, 3);
        e.target.value = value;
        cvvError.textContent = value.length === 3 ? '' : 'Debe tener 3 dígitos';
    });

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const cardType = cardTypeSelect.value;
        const cardName = cardNameInput.value.trim();
        const cardNumber = cardNumberInput.value.replace(/\s/g, '');
        const expiryDate = expiryDateInput.value;
        const cvv = cvvInput.value;
        const carrito = JSON.parse(localStorage.getItem("carrito")) || [];

        let hasErrors = false;

        if (!cardType) {
            cardTypeError.textContent = 'Selecciona tipo de tarjeta';
            hasErrors = true;
        }
        if (!cardName) {
            cardNameError.textContent = 'Nombre obligatorio';
            hasErrors = true;
        }
        if (cardNumber.length !== 16) {
            cardNumberError.textContent = 'Número inválido';
            hasErrors = true;
        }
        if (expiryDate.length !== 5 || !expiryDate.includes('/')) {
            expiryError.textContent = 'Fecha inválida';
            hasErrors = true;
        }
        if (cvv.length !== 3) {
            cvvError.textContent = 'CVV inválido';
            hasErrors = true;
        }

        if (hasErrors) return;

        fetch("/procesar_pago/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                cardType,
                cardName,
                cardNumber,
                expiryDate,
                cvv,
                carrito
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                localStorage.removeItem("carrito");
            
                // Mostrar modal si existe
                const modal = document.getElementById('successModal');
                if (modal) {
                    modal.classList.add('show');
                } else {
                    // O redirigir si no hay modal
                    window.location.href = data.redirect_url;
                }
            }            
        })
        .catch(error => {
            console.error("Error en fetch:", error);
            alert("Ocurrió un error inesperado.");
        });
    });
}

function volverAlInicio() {
    window.location.href = "/";
}