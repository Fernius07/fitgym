/* FitGym & Workout - interacción en el cliente (E4a, opción 1)
 *
 * 1. Selector de idioma: cambia de idioma al elegir una opción.
 * 2. Lista de ejercicios: filtro en vivo por nombre y por grupo muscular.
 * 3. Detalle de ejercicio: envío de valoraciones por AJAX (fetch) sin
 *    recargar la página. Si no hay JavaScript, el formulario funciona
 *    igualmente con un POST normal.
 * 4. Mensajes de Django: desaparecen solos con un efecto de fundido.
 */
document.documentElement.classList.add('js');

document.addEventListener('DOMContentLoaded', function () {
    iniciarSelectorIdioma();
    iniciarFiltroEjercicios();
    iniciarValoracionesAjax();
    ocultarMensajes();
});

function iniciarSelectorIdioma() {
    var selector = document.getElementById('selector-idioma');
    if (!selector) { return; }
    selector.addEventListener('change', function () {
        selector.form.submit();
    });
}

function iniciarFiltroEjercicios() {
    var lista = document.getElementById('lista-ejercicios');
    var buscador = document.getElementById('buscador');
    if (!lista || !buscador) { return; }

    var tarjetas = Array.prototype.slice.call(lista.children);
    var botones = document.querySelectorAll('#filtros .filtro');
    var contador = document.getElementById('contador');
    var sinResultados = document.getElementById('sin-resultados');
    var grupoActivo = '';

    function quitarTildes(texto) {
        return texto.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
    }

    function filtrar() {
        var texto = quitarTildes(buscador.value.trim());
        var visibles = 0;
        tarjetas.forEach(function (tarjeta) {
            var coincideTexto = quitarTildes(tarjeta.dataset.nombre).indexOf(texto) !== -1;
            var coincideGrupo = !grupoActivo || tarjeta.dataset.grupo === grupoActivo;
            var mostrar = coincideTexto && coincideGrupo;
            tarjeta.hidden = !mostrar;
            if (mostrar) { visibles++; }
        });
        contador.textContent = contador.dataset.plantilla
            .replace('{n}', visibles)
            .replace('{total}', tarjetas.length);
        sinResultados.hidden = visibles > 0;
    }

    buscador.addEventListener('input', filtrar);
    Array.prototype.forEach.call(botones, function (boton) {
        boton.addEventListener('click', function () {
            Array.prototype.forEach.call(botones, function (b) { b.classList.remove('activo'); });
            boton.classList.add('activo');
            grupoActivo = boton.dataset.grupo;
            filtrar();
        });
    });
    filtrar();
}

function iniciarValoracionesAjax() {
    var form = document.getElementById('form-valoracion');
    if (!form || !window.fetch) { return; }

    var lista = document.getElementById('lista-valoraciones');
    var total = document.getElementById('total-valoraciones');
    var vacio = document.getElementById('sin-valoraciones');
    var aviso = document.getElementById('aviso-valoracion');
    var boton = form.querySelector('button[type="submit"]');

    function limpiarErrores() {
        Array.prototype.forEach.call(form.querySelectorAll('.errores'), function (ul) {
            ul.innerHTML = '';
        });
    }

    function mostrarErrores(errores) {
        Object.keys(errores).forEach(function (campo) {
            var ul = form.querySelector('.errores[data-campo="' + campo + '"]');
            if (!ul) { return; }
            errores[campo].forEach(function (mensaje) {
                var li = document.createElement('li');
                li.textContent = mensaje;
                ul.appendChild(li);
            });
        });
    }

    form.addEventListener('submit', function (evento) {
        evento.preventDefault();
        limpiarErrores();
        aviso.textContent = '';
        aviso.className = 'aviso';
        boton.disabled = true;

        fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            credentials: 'same-origin'
        })
            .then(function (respuesta) { return respuesta.json(); })
            .then(function (datos) {
                if (datos.ok) {
                    lista.insertAdjacentHTML('afterbegin', datos.html);
                    var nueva = lista.firstElementChild;
                    nueva.classList.add('nueva');          // efecto de aparición
                    total.textContent = datos.total;
                    vacio.hidden = true;
                    form.reset();
                    aviso.textContent = datos.mensaje;
                    aviso.classList.add('aviso-ok');
                } else {
                    mostrarErrores(datos.errores || {});
                    aviso.textContent = form.dataset.error;
                    aviso.classList.add('aviso-error');
                }
            })
            .catch(function () {
                aviso.textContent = form.dataset.error;
                aviso.classList.add('aviso-error');
            })
            .then(function () { boton.disabled = false; });
    });
}

function ocultarMensajes() {
    var mensajes = document.querySelector('.mensajes');
    if (!mensajes) { return; }
    setTimeout(function () {
        mensajes.classList.add('desvanecer');
        setTimeout(function () { mensajes.remove(); }, 600);
    }, 4000);
}
