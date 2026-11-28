// Interacción en el cliente para FitGym & Workout
document.documentElement.classList.add('js');

document.addEventListener('DOMContentLoaded', function () {
    iniciarSelectorIdioma();
    iniciarFiltroEjercicios();
    iniciarValoracionesAjax();
    ocultarMensajes();
});

function iniciarSelectorIdioma() {
    const selector = document.getElementById('selector-idioma');
    if (!selector) { return; }
    selector.addEventListener('change', function () {
        selector.form.submit();
    });
}

function iniciarFiltroEjercicios() {
    const lista = document.getElementById('lista-ejercicios');
    const buscador = document.getElementById('buscador');
    const contador = document.getElementById('contador');
    const sinResultados = document.getElementById('sin-resultados');
    if (!lista || !buscador || !contador || !sinResultados) { return; }

    const tarjetas = Array.from(lista.children);
    const botones = document.querySelectorAll('#filtros .filtro');
    let grupoActivo = '';

    function quitarTildes(texto) {
        return texto.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
    }

    function filtrar() {
        const texto = quitarTildes(buscador.value.trim());
        let visibles = 0;
        tarjetas.forEach(function (tarjeta) {
            const coincideTexto = quitarTildes(tarjeta.dataset.nombre).indexOf(texto) !== -1;
            const coincideGrupo = !grupoActivo || tarjeta.dataset.grupo === grupoActivo;
            const mostrar = coincideTexto && coincideGrupo;
            tarjeta.hidden = !mostrar;
            if (mostrar) { visibles++; }
        });
        contador.textContent = contador.dataset.plantilla
            .replace('{n}', visibles)
            .replace('{total}', tarjetas.length);
        sinResultados.hidden = visibles > 0;
    }

    buscador.addEventListener('input', filtrar);
    botones.forEach(function (boton) {
        boton.addEventListener('click', function () {
            botones.forEach(function (b) {
                b.classList.remove('activo');
                b.setAttribute('aria-pressed', 'false');
            });
            boton.classList.add('activo');
            boton.setAttribute('aria-pressed', 'true');
            grupoActivo = boton.dataset.grupo;
            filtrar();
        });
    });
    filtrar();
}

function iniciarValoracionesAjax() {
    const form = document.getElementById('form-valoracion');
    if (!form || !window.fetch) { return; }

    const lista = document.getElementById('lista-valoraciones');
    const total = document.getElementById('total-valoraciones');
    const vacio = document.getElementById('sin-valoraciones');
    const aviso = document.getElementById('aviso-valoracion');
    const boton = form.querySelector('button[type="submit"]');
    if (!lista || !total || !vacio || !aviso || !boton) { return; }

    function limpiarErrores() {
        form.querySelectorAll('.errores').forEach(function (ul) {
            ul.innerHTML = '';
        });
    }

    function mostrarErrores(errores) {
        Object.keys(errores).forEach(function (campo) {
            const ul = form.querySelector('.errores[data-campo="' + campo + '"]');
            if (!ul) { return; }
            errores[campo].forEach(function (mensaje) {
                const li = document.createElement('li');
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
            .then(function (respuesta) {
                if (!respuesta.ok && respuesta.status !== 400) {
                    throw new Error('Error ' + respuesta.status);
                }
                return respuesta.json();
            })
            .then(function (datos) {
                if (datos.ok) {
                    lista.insertAdjacentHTML('afterbegin', datos.html);
                    const nueva = lista.firstElementChild;
                    nueva.classList.add('nueva');
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
    const mensajes = document.querySelector('.mensajes');
    if (!mensajes) { return; }
    setTimeout(function () {
        mensajes.classList.add('desvanecer');
        setTimeout(function () { mensajes.remove(); }, 600);
    }, 4000);
}
