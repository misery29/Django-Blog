from django.shortcuts import render
from .models import Campo
from .forms import CampoSearchForm

def list_fields(request):
    form = CampoSearchForm(request.GET or None)
    campos = Campo.objects.all()


    print(form.errors)
    if form.is_valid():
        cidade = form.cleaned_data.get('cidade')
        tipo_gramado = form.cleaned_data.get('tipo_gramado')
        iluminacao_noturna = form.cleaned_data['iluminacao_noturna']
        vestiarios = form.cleaned_data.get('vestiarios')

        if cidade:
            campos = campos.filter(cidade__icontains=cidade)
        if tipo_gramado:
            campos = campos.filter(tipo_gramado=tipo_gramado)
        if iluminacao_noturna == 'true':
            campos = campos.exclude(iluminacao_noturna=False)
        if iluminacao_noturna == 'false':
            campos = campos.filter(iluminacao_noturna=False)
        if vestiarios == 'true':
            campos = campos.exclude(iluminacao_noturna=False)
        if vestiarios == 'false':
            campos = campos.filter(iluminacao_noturna=False)

    print(form.cleaned_data)
    return render(request, 'usuarios/index.html', {'campos': campos, 'form': form})
