# FitGym & Workout

Proyecto del grupo IW-BI-09 para la asignatura de Ingeniería Web. Es una página web hecha con Django donde se pueden consultar ejercicios de fuerza y acondicionamiento, organizados por el músculo que trabajan y por el material que hace falta para hacerlos.

## Qué se puede hacer en la web

- **Portada:** muestra un ejercicio destacado de cada grupo muscular (el más popular de cada uno) y tiene botones para ir directamente a la lista de ejercicios o a la de grupos musculares.
- **Menú:** está en la parte de arriba de todas las páginas y permite moverse entre la portada, los ejercicios, los grupos musculares y el equipamiento. También tiene un selector de idioma (español / inglés).
- **Ejercicios:** una lista con todos los ejercicios. Cada uno indica a qué grupo muscular pertenece (con enlace al grupo) y tiene un botón para ver sus detalles. Se puede filtrar al momento por nombre y por grupo muscular.
- **Detalle de un ejercicio:** explica en qué consiste, dice qué grupo muscular trabaja y qué material se necesita. Además muestra las valoraciones de los usuarios y un formulario para dejar una nueva.
- **Grupos musculares:** una lista con los grupos (pecho, espalda, pierna, hombro, brazo y core). Al entrar en uno se ve una breve descripción y todos los ejercicios que lo trabajan.
- **Equipamiento:** una lista con el material. Al entrar en uno se ve para qué sirve y qué ejercicios se pueden hacer con él.
- **Panel de administración:** permite añadir, modificar y borrar ejercicios, grupos musculares, equipamiento y valoraciones sin tocar el código.

## Mejoras de la entrega E4a

| Opción | Qué hemos hecho | Dónde está |
|---|---|---|
| **1. JavaScript (eventos, efectos, AJAX)** | Filtro en vivo de la lista de ejercicios (buscador + botones por grupo, con contador). Envío de valoraciones por AJAX con `fetch`: la valoración aparece con una animación sin recargar la página y los errores se muestran bajo cada campo. Si no hay JavaScript, el formulario sigue funcionando con un POST normal. El selector de idioma cambia al elegir una opción y los mensajes desaparecen con un fundido. | `appFitGym/static/js/fitgym.js`, `EjercicioDetailView` en `views.py` (responde JSON si la petición es AJAX) |
| **2. Vistas basadas en clases** | Todas las vistas son clases: `TemplateView` (portada), `ListView` (listas) y `DetailView` (detalles). El detalle de ejercicio combina `DetailView` con `FormMixin` para el formulario. | `appFitGym/views.py`, `appFitGym/urls.py` |
| **3. Formularios** | Nueva entidad `Valoracion` (autor, puntuación de 1 a 5, comentario y fecha) ligada a `Ejercicio`, con un `ModelForm` en la parte pública. | `appFitGym/models.py`, `appFitGym/forms.py`, `templates/detalle_ejercicio.html` |
| **5. Datos iniciales** | El fixture `datos.json` incluye todas las entidades: 6 grupos, 6 equipamientos, 15 ejercicios y 6 valoraciones. | `appFitGym/fixtures/datos.json` |
| **6. Multilingüismo (i18n)** | Español e inglés. Las URLs llevan el prefijo del idioma (`/es/...`, `/en/...`) con `i18n_patterns`, `LocaleMiddleware` detecta el idioma y las partes estáticas de las plantillas y el formulario están traducidas. | `fitgym/settings.py`, `fitgym/urls.py`, `locale/en/LC_MESSAGES/django.po` |

También hay tests automáticos (`py manage.py test`) que comprueban las páginas en los dos idiomas, la traducción, el envío de valoraciones (con y sin AJAX) y los datos iniciales.

## Pasos para probar el proyecto

1. Abrir un cmd y activar el entorno virtual: `workon [nombre entorno virtual]`. Si no sabéis el nombre, escribid `workon` y os sale la lista.
2. Ir a la carpeta del proyecto (la que contiene `manage.py`).
3. La base de datos `db.sqlite3` ya viene con los datos. Para crearla desde cero:
   ```
   py manage.py migrate
   py manage.py loaddata datos
   ```
4. Ejecutar el servidor: `py manage.py runserver`
5. Abrir el navegador en http://127.0.0.1:8000/ (redirige a `/es/`; la versión en inglés está en http://127.0.0.1:8000/en/).
6. Para el panel de admin: http://127.0.0.1:8000/admin

   Usuario: adminDjango

   Contraseña: adminDjango

Las traducciones ya están compiladas (`django.mo`). Si se cambia el `.po`, hay que volver a compilarlas con `py manage.py compilemessages` (necesita GNU gettext).
