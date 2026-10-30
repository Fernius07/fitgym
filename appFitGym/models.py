from django.db import models


class GrupoMuscular(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Equipamiento(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


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
