from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['campo', 'data_inicio', 'data_fim', 'preco_total']
        widgets = {
            'data_inicio': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'data_fim': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'preco_total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }
