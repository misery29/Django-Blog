from django import forms

class CampoSearchForm(forms.Form):
    cidade = forms.CharField(required=False, label='Cidade')
    tipo_gramado = forms.ChoiceField(
        choices=[('Todos', 'Todos'), ('Sintética', 'Sintética'), ('Natural', 'Natural')],
        required=False,
        label='Tipo de Gramado'
    )
    iluminacao_noturna = forms.BooleanField(required=False, label='Iluminação Noturna')
    vestuario = forms.BooleanField(required=False, label='Vestiário')