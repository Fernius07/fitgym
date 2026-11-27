from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class GrupoMuscular(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('grupo', args=[self.pk])


class Equipamiento(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('equipamiento', args=[self.pk])


class Ejercicio(models.Model):
    # Un ejercicio pertenece a un grupo muscular
    grupo = models.ForeignKey(GrupoMuscular, on_delete=models.CASCADE)
    # Un ejercicio puede necesitar varios equipamientos
    equipamiento = models.ManyToManyField(Equipamiento)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    popularidad = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('ejercicio', args=[self.pk])


class Valoracion(models.Model):
    # Opinión que deja un visitante sobre un ejercicio (formulario público)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE,
                                  related_name='valoraciones')
    autor = models.CharField(max_length=50)
    puntuacion = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(max_length=500)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'valoración'
        verbose_name_plural = 'valoraciones'

    def __str__(self):
        return f'{self.autor} - {self.ejercicio} ({self.puntuacion}/5)'
