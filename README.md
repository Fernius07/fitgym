# FitGym & Workout

Proyecto del grupo IW-BI-09 para la asignatura de Ingeniería Web. Es una página web hecha con Django donde se pueden consultar ejercicios de fuerza y acondicionamiento, organizados por el músculo que trabajan y por el material que hace falta para hacerlos.

## Qué se puede hacer en la web

- **Portada:** muestra un ejercicio destacado de cada grupo muscular (el más popular de cada uno) y tiene botones para ir directamente a la lista de ejercicios o a la de grupos musculares.
- **Menú:** está en la parte de arriba de todas las páginas y permite moverse entre la portada, los ejercicios, los grupos musculares y el equipamiento.
- **Ejercicios:** una lista con todos los ejercicios (press de banca, dominadas, peso muerto, curl de bíceps...). Cada uno indica a qué grupo muscular pertenece y tiene un botón para ver sus detalles.
- **Detalle de un ejercicio:** explica en qué consiste, dice qué grupo muscular trabaja y qué material se necesita. Un mismo ejercicio puede hacerse con varios materiales, y desde aquí se puede entrar a la página de cada uno.
- **Grupos musculares:** una lista con los grupos (pecho, espalda, pierna, hombro, brazo y core). Al entrar en uno se ve una breve descripción y todos los ejercicios que lo trabajan.
- **Equipamiento:** una lista con el material (mancuernas, barra olímpica, poleas, peso corporal, bandas elásticas y máquinas guiadas). Al entrar en uno se ve para qué sirve y qué ejercicios se pueden hacer con él.
- **Panel de administración:** permite añadir, modificar y borrar ejercicios, grupos musculares y equipamiento sin tocar el código.

La base de datos ya incluye datos de ejemplo para poder probar todo desde el principio.

## Pasos para probar proyecto

1. Descomprimir carpeta y mover `fitgym_proj` a un sitio accesible.
2. En cmd escribir `workon [nombre entorno virtual]`. Si no sabéis el nombre, escribid `workon` y os sale la lista.
3. Ir a la carpeta de `fitgym_proj`: `cd fitgym_proj`
4. Ejecutar el servidor: `py manage.py runserver`
5. Abrir el navegador en http://127.0.0.1:8000/
6. Para el panel de admin: http://127.0.0.1:8000/admin

   Usuario: adminDjango

   Contraseña: adminDjango
