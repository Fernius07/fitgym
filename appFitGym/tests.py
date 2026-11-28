from django.test import TestCase
from django.urls import reverse
from django.utils import translation

from .models import Ejercicio, Valoracion


class FitGymTests(TestCase):
    fixtures = ['datos']

    def test_paginas_publicas_responden(self):
        ejercicio = Ejercicio.objects.first()
        for idioma in ('es', 'en'):
            with translation.override(idioma):
                urls = [
                    reverse('index'), reverse('ejercicios'), reverse('grupos'),
                    reverse('equipamientos'), ejercicio.get_absolute_url(),
                    ejercicio.grupo.get_absolute_url(),
                    ejercicio.equipamiento.first().get_absolute_url(),
                ]
            for url in urls:
                with self.subTest(url=url):
                    self.assertTrue(url.startswith(f'/{idioma}/'))
                    self.assertEqual(self.client.get(url).status_code, 200)

    def test_traduccion_ingles(self):
        respuesta = self.client.get('/en/')
        self.assertContains(respuesta, 'Featured exercises')
        self.assertContains(respuesta, '<html lang="en">')
        self.assertContains(self.client.get('/es/'), 'Ejercicios destacados')

    def test_valoracion_por_ajax(self):
        ejercicio = Ejercicio.objects.get(pk=2)
        respuesta = self.client.post(
            ejercicio.get_absolute_url(),
            {'autor': 'Test', 'puntuacion': 4, 'comentario': 'Muy bueno'},
            headers={'x-requested-with': 'XMLHttpRequest'},
        )
        self.assertEqual(respuesta.status_code, 200)
        datos = respuesta.json()
        self.assertTrue(datos['ok'])
        self.assertIn('Muy bueno', datos['html'])
        self.assertEqual(ejercicio.valoraciones.count(), 1)

    def test_valoracion_ajax_con_errores(self):
        ejercicio = Ejercicio.objects.get(pk=2)
        respuesta = self.client.post(
            ejercicio.get_absolute_url(),
            {'autor': '', 'puntuacion': 9, 'comentario': ''},
            headers={'x-requested-with': 'XMLHttpRequest'},
        )
        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(set(respuesta.json()['errores']),
                         {'autor', 'puntuacion', 'comentario'})
        self.assertEqual(ejercicio.valoraciones.count(), 0)

    def test_valoracion_sin_javascript(self):
        ejercicio = Ejercicio.objects.get(pk=2)
        respuesta = self.client.post(
            ejercicio.get_absolute_url(),
            {'autor': 'Test', 'puntuacion': 5, 'comentario': 'Genial'},
            follow=True,
        )
        self.assertRedirects(respuesta, ejercicio.get_absolute_url())
        self.assertContains(respuesta, 'Genial')

    def test_datos_iniciales_todas_las_entidades(self):
        self.assertEqual(Ejercicio.objects.count(), 15)
        self.assertTrue(Valoracion.objects.exists())
