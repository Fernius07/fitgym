from django.shortcuts import render, get_object_or_404
from .models import GrupoMuscular, Equipamiento, Ejercicio


# Portada: el ejercicio más popular de cada grupo muscular
def index(request):
    destacados = []
    for grupo in GrupoMuscular.objects.order_by('nombre'):
        ejercicio = grupo.ejercicio_set.order_by('-popularidad').first()
        if ejercicio:
            destacados.append(ejercicio)
    context = {'destacados': destacados}
    return render(request, 'index.html', context)


def lista_ejercicios(request):
    ejercicios = Ejercicio.objects.select_related('grupo').order_by('nombre')
    context = {'lista_ejercicios': ejercicios}
    return render(request, 'lista_ejercicios.html', context)


def detalle_ejercicio(request, ejercicio_id):
    ejercicio = get_object_or_404(Ejercicio, pk=ejercicio_id)
    equipamientos = ejercicio.equipamiento.all()
    context = {'ejercicio': ejercicio, 'equipamientos': equipamientos}
    return render(request, 'detalle_ejercicio.html', context)


def lista_grupos(request):
    grupos = GrupoMuscular.objects.order_by('nombre')
    context = {'lista_grupos': grupos}
    return render(request, 'lista_grupos.html', context)


def detalle_grupo(request, grupo_id):
    grupo = get_object_or_404(GrupoMuscular, pk=grupo_id)
    ejercicios = grupo.ejercicio_set.order_by('nombre')
    context = {'grupo': grupo, 'ejercicios': ejercicios}
    return render(request, 'detalle_grupo.html', context)


def lista_equipamientos(request):
    equipamientos = Equipamiento.objects.order_by('nombre')
    context = {'lista_equipamientos': equipamientos}
    return render(request, 'lista_equipamientos.html', context)


def detalle_equipamiento(request, equipamiento_id):
    equipamiento = get_object_or_404(Equipamiento, pk=equipamiento_id)
    ejercicios = equipamiento.ejercicio_set.order_by('nombre')
    context = {'equipamiento': equipamiento, 'ejercicios': ejercicios}
    return render(request, 'detalle_equipamiento.html', context)
