from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('ejercicios/', views.EjercicioListView.as_view(), name='ejercicios'),
    path('ejercicios/<int:pk>/', views.EjercicioDetailView.as_view(), name='ejercicio'),
    path('grupos/', views.GrupoListView.as_view(), name='grupos'),
    path('grupos/<int:pk>/', views.GrupoDetailView.as_view(), name='grupo'),
    path('equipamientos/', views.EquipamientoListView.as_view(), name='equipamientos'),
    path('equipamientos/<int:pk>/', views.EquipamientoDetailView.as_view(), name='equipamiento'),
]
