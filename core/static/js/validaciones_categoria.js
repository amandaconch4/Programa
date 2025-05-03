document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('categoriaForm');
    const nombreCategoriaInput = document.getElementById('id_nombre_categoria');
    const nombreCategoriaError = document.getElementById('nombre_categoria-error');
    const nombreRequisitos = document.getElementById('nombre-requisitos');
    const reqNombreLength = document.getElementById('req-nombre-length');

    function validarNombreCategoria(nombre) {
        // Trim para quitar espacios al inicio y final
        nombre = nombre.trim();
        
        // Validaciones individuales
        const longitud = nombre.length >= 3;
        const soloLetras = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/.test(nombre);

        // Actualizar clases visuales
        reqNombreLength.className = nombre ? (longitud ? 'valido' : 'invalid') : '';

        // Retornar validación completa
        return nombre && longitud && soloLetras;
    }

    // Función para verificar si la categoría ya existe
    function verificarCategoriaExistente(nombre) {
        return fetch(`/verificar-categoria/?nombre=${encodeURIComponent(nombre)}`)
            .then(response => response.json())
            .then(data => {
                if (data.existe) {
                    nombreCategoriaError.textContent = 'La categoría ya existe';
                    nombreCategoriaError.style.display = 'block';
                    nombreCategoriaInput.classList.add('error');
                    return false;
                }
                return true;
            })
            .catch(error => {
                console.error('Error:', error);
                return true;
            });
    }

    // Eventos de validación en tiempo real
    nombreCategoriaInput.addEventListener('input', function() {
        // Reemplazar cualquier carácter que no sea letra o espacio
        this.value = this.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]/g, '');
        validarNombreCategoria(this.value);
        nombreCategoriaError.textContent = '';
        nombreCategoriaError.style.display = 'none';
        nombreCategoriaInput.classList.remove('error');
    });

    // Validación al enviar el formulario
    form.addEventListener('submit', async function(e) {
        let valido = true;
        const nombreCategoria = nombreCategoriaInput.value.trim();

        if (!nombreCategoria || !validarNombreCategoria(nombreCategoria)) {
            nombreCategoriaError.textContent = 'Ingrese un nombre de categoría válido';
            nombreCategoriaError.style.display = 'block';
            valido = false;
        }

        // Verificar si la categoría ya existe antes de enviar
        if (valido) {
            const existeCategoria = await verificarCategoriaExistente(nombreCategoria);
            if (!existeCategoria) {
                valido = false;
            }
        }

        if (!valido) e.preventDefault();
    });
});