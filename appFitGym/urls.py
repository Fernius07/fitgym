from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ejercicios/', views.lista_ejercicios, name='ejercicios'),
    path('ejercicios/<int:ejercicio_id>/', views.detalle_ejercicio, name='ejercicio'),
    path('grupos/', views.lista_grupos, name='grupos'),
    path('grupos/<int:grupo_id>/', views.detalle_grupo, name='grupo'),
    path('equipamientos/', views.lista_equipamientos, name='equipamientos'),
    path('equipamientos/<int:equipamiento_id>/', views.detalle_equipamiento, name='equipamiento'),
]
