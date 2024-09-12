from django import forms
from .models import Avaliacao

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['estrelas', 'comentario']
        widgets = {
            'estrelas': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comentario': forms.Textarea(attrs={'rows': 4}),
        }

def clean_estrelas(self):
        estrelas = self.cleaned_data.get('estrelas')
        if estrelas < 1 or estrelas > 5:
            raise forms.ValidationError("O número de estrelas deve estar entre 1 e 5.")
        return estrelas        