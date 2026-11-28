from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormMixin

from .forms import ValoracionForm
from .models import Ejercicio, Equipamiento, GrupoMuscular


def es_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


# Portada: el ejercicio más popular de cada grupo muscular
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        destacados = []
        grupos_vistos = set()
        ejercicios = Ejercicio.objects.select_related('grupo').order_by(
            'grupo__nombre', '-popularidad', 'nombre'
        )
        for ejercicio in ejercicios:
            if ejercicio.grupo_id not in grupos_vistos:
                grupos_vistos.add(ejercicio.grupo_id)
                destacados.append(ejercicio)
        context['destacados'] = destacados
        return context


class EjercicioListView(ListView):
    template_name = 'lista_ejercicios.html'
    context_object_name = 'lista_ejercicios'
    queryset = Ejercicio.objects.select_related('grupo').order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Para los botones de filtro por grupo (JavaScript)
        context['grupos'] = GrupoMuscular.objects.order_by('nombre')
        return context


# Detalle de un ejercicio con formulario de valoraciones (normal o AJAX)
class EjercicioDetailView(FormMixin, DetailView):
    model = Ejercicio
    template_name = 'detalle_ejercicio.html'
    context_object_name = 'ejercicio'
    form_class = ValoracionForm

    def get_queryset(self):
        return Ejercicio.objects.select_related('grupo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipamientos'] = self.object.equipamiento.order_by('nombre')
        context['valoraciones'] = self.object.valoraciones.order_by('-fecha')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        valoracion = form.save(commit=False)
        valoracion.ejercicio = self.object
        valoracion.save()
        if es_ajax(self.request):
            html = render_to_string('fragmento_valoracion.html',
                                    {'v': valoracion}, request=self.request)
            return JsonResponse({
                'ok': True,
                'html': html,
                'total': self.object.valoraciones.count(),
                'mensaje': _('¡Gracias por tu valoración!'),
            })
        messages.success(self.request, _('¡Gracias por tu valoración!'))
        return redirect(self.object)

    def form_invalid(self, form):
        if es_ajax(self.request):
            return JsonResponse({'ok': False, 'errores': form.errors}, status=400)
        return self.render_to_response(self.get_context_data(form=form))


class GrupoListView(ListView):
    template_name = 'lista_grupos.html'
    context_object_name = 'lista_grupos'
    queryset = GrupoMuscular.objects.order_by('nombre')


class GrupoDetailView(DetailView):
    model = GrupoMuscular
    template_name = 'detalle_grupo.html'
    context_object_name = 'grupo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ejercicios'] = self.object.ejercicio_set.order_by('nombre')
        return context


class EquipamientoListView(ListView):
    template_name = 'lista_equipamientos.html'
    context_object_name = 'lista_equipamientos'
    queryset = Equipamiento.objects.order_by('nombre')


class EquipamientoDetailView(DetailView):
    model = Equipamiento
    template_name = 'detalle_equipamiento.html'
    context_object_name = 'equipamiento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ejercicios'] = (self.object.ejercicio_set
                                 .select_related('grupo').order_by('nombre'))
        return context
