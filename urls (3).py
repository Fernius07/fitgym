from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Vista de Django para cambiar de idioma (formulario del menú)
    path('i18n/', include('django.conf.urls.i18n')),
]

# Las URLs públicas llevan el prefijo del idioma: /es/... y /en/...
urlpatterns += i18n_patterns(
    path('', include('appFitGym.urls')),
    path('admin/', admin.site.urls),
)
