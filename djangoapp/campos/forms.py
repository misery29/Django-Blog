from django import forms

class CampoSearchForm(forms.Form):
    cidade = forms.CharField(required=False, label='Cidade')
    tipo_gramado = forms.ChoiceField(
        choices=[('sintetico', 'sintetico'), ('natural', 'natural')],
        required=False,
        label='Tipo de Gramado'
    )
    iluminacao_noturna = forms.ChoiceField(
        choices=[('', ''), ('false', '0'), ('true', '1')],
        required=False,
        label='iluminacao_noturna'
    )
    vestiarios = forms.ChoiceField(
        choices=[('', ''), ('false', '0'), ('true', '1')],
        required=False,
        label='vestiarios'
        )