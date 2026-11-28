from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Valoracion


class ValoracionForm(forms.ModelForm):
    """Formulario público basado en el modelo Valoracion."""

    class Meta:
        model = Valoracion
        fields = ['autor', 'puntuacion', 'comentario']
        labels = {
            'autor': _('Tu nombre'),
            'puntuacion': _('Puntuación'),
            'comentario': _('Comentario'),
        }
        widgets = {
            'puntuacion': forms.Select(choices=[(i, '★' * i) for i in range(5, 0, -1)]),
            'comentario': forms.Textarea(attrs={'rows': 3}),
        }
