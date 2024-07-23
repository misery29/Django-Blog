from django.shortcuts import render
from .models import Campo
from .forms import CampoSearchForm

def index(request):
    form = CampoSearchForm(request.GET or None)
    campos = Campo.objects.all()

    if form.is_valid():
        cidade = form.cleaned_data.get('cidade')
        tipo_gramado = form.cleaned_data.get('tipo_gramado')
        iluminacao_noturna = form.cleaned_data.get('iluminacao_noturna')
        vestuario = form.cleaned_data.get('vestuario')

        if cidade:
            campos = campos.filter(localizacao__icontains=cidade)
        if tipo_gramado and tipo_gramado != 'Todos':
            campos = campos.filter(tipo_gramado=tipo_gramado)
        if iluminacao_noturna:
            campos = campos.filter(iluminacao_noturna=iluminacao_noturna)
        if vestuario:
            campos = campos.filter(vestuario=vestuario)

    return render(request, 'index.html', {'campos': campos, 'form': form})
