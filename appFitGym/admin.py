from django.contrib import admin
from .models import GrupoMuscular, Equipamiento, Ejercicio, Valoracion

admin.site.register(GrupoMuscular)
admin.site.register(Equipamiento)
admin.site.register(Ejercicio)


class ValoracionAdmin(admin.ModelAdmin):
    list_display = ('ejercicio', 'autor', 'puntuacion', 'fecha')
    list_filter = ('puntuacion', 'ejercicio__grupo')


admin.site.register(Valoracion, ValoracionAdmin)
