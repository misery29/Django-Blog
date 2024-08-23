from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Campo
from django.conf import settings
from .forms import CampoSearchForm
import json
import requests

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

def geocode_address(cidade, endereco):
    api_key = 'AIzaSyCnyOD_c4KKH7mSvQP_3QObDjg5cyawnC8'
    
    def fetch_geocode(url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
            return response.json()
        except requests.RequestException as e:
            print(f"Erro ao fazer requisição: {e}")
            return None

    # Construindo a URL de geocodificação principal
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={endereco},{cidade}&key={api_key}"
    
    # Realiza a requisição para a URL principal
    geocode_data = fetch_geocode(geocode_url)

    if geocode_data and geocode_data['status'] == 'OK' and geocode_data['results']:
        location = geocode_data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        # Tentativa de fallback, adicionando a cidade ao endereço
        endereco_com_cidade = f"{cidade},{endereco}"
        fallback_geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={endereco_com_cidade}&key={api_key}"
        
        # Realiza a requisição para a URL de fallback
        fallback_data = fetch_geocode(fallback_geocode_url)
        
        if fallback_data and fallback_data['status'] == 'OK' and fallback_data['results']:
            location = fallback_data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        
        # Coordenadas padrão em caso de falha
        print("Geocodificação falhou, retornando coordenadas padrão.")
        return None, None  # Coordenadas padrão (Brasília)


@login_required
def detail_fields(request, pk):
    campo = get_object_or_404(Campo, pk=pk)
    
    # Realiza a geocodificação se latitude e longitude ainda não estiverem definidas
    if not campo.latitude or not campo.longitude:
        lat, lon = geocode_address(campo.endereco, campo.cidade)
        if lat and lon:
            campo.latitude = lat
            campo.longitude = lon
            campo.save()  # Salva as coordenadas no banco de dados
    latitude_str = f"{campo.latitude:.6f}" if campo.latitude else None
    longitude_str = f"{campo.longitude:.6f}" if campo.longitude else None

    return render(request, 'campo_detail.html', {
        'campo': campo,
        'latitude': latitude_str,
        'longitude': longitude_str,
    })

def map_view(request):
    campos = list(Campo.objects.values('id','nome', 'endereco', 'latitude', 'longitude'))
    campos_json = json.dumps(campos)
    return render(request, 'map_view.html', {'campos_json': campos_json})