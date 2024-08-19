from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_datetime
from .models import Campo, Reserva
from .forms import ReservaForm
import json
from django.utils import timezone
from django.db.models import Min, Max
from django.http import HttpResponse

def reservar(request, campo_id):
    campo = get_object_or_404(Campo, id=campo_id)
    if request.method == 'POST':
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        preco_total = request.POST.get('preco_total')
        return render(request, 'confirmacao_pagamento.html', {
            'campo': campo,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'preco_total': preco_total
        })
    return render(request, 'campos/detalhes_campo.html', {'campo': campo})

def confirmar_reserva(request):
    campo_id = request.POST.get('campo_id')
    if request.method == 'POST':
        campo_id = request.POST.get('campo_id')
        data_inicio = parse_datetime(request.POST.get('data_inicio'))
        data_fim = parse_datetime(request.POST.get('data_fim'))
        preco_total = request.POST.get('preco_total')

        campo = get_object_or_404(Campo, id=campo_id)

        reserva = Reserva(
            usuario=request.user,
            campo=campo,
            data_inicio=data_inicio,
            data_fim=data_fim,
            preco_total=preco_total
        )
        reserva.save()

        return HttpResponse('Reserva confirmada com sucesso!')
    return redirect('reservas:reservar', campo_id=campo_id)

def detalhes_campo(request, campo_id):
    campo = get_object_or_404(Campo, id=campo_id)
    reservas = Reserva.objects.filter(campo=campo)

    # Horários indisponíveis (reservas e bloqueios)
    horarios_indisponiveis = [
        {
            "from": reserva.data_inicio.strftime('%Y-%m-%dT%H:%M:%S'),
            "to": reserva.data_fim.strftime('%Y-%m-%dT%H:%M:%S')
        }
        for reserva in reservas
        if reserva.data_fim > timezone.now()  # Exclui reservas passadas
    ]

    # Ajuste para minTime e maxTime com base nas reservas
    min_time = '00:00'
    max_time = '23:59'
    
    if reservas.exists():
        min_time = reservas.aggregate(Min('data_inicio'))['data_inicio__min'].strftime('%H:%M')
        max_time = reservas.aggregate(Max('data_fim'))['data_fim__max'].strftime('%H:%M')

    context = {
        'campo': campo,
        'horarios_indisponiveis': json.dumps(horarios_indisponiveis),  # Passa os horários como JSON
        'min_time': min_time,
        'max_time': max_time,
    }
    return render(request, 'campos/detalhes_campo.html', context)