from django.shortcuts import render, get_object_or_404, redirect
from .models import Campo, Reserva
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

def reservar(request, campo_id):
    campo = get_object_or_404(Campo, id=campo_id)
    erro_mensagem = None

    if request.method == 'POST':
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        preco_total = request.POST.get('preco_total')

        try:
            # Validações
            if data_inicio >= data_fim:
                raise ValidationError("A data de início deve ser anterior à data de fim")

            reservas_conflitantes = Reserva.objects.filter(
                campo=campo,
                data_inicio__lt=data_fim,
                data_fim__gt=data_inicio
            )
            if reservas_conflitantes.exists():
                raise ValidationError("Conflito com outra reserva existente")

            return render(request, 'confirmacao_pagamento.html', {
                'campo': campo,
                'data_inicio': data_inicio,
                'data_fim': data_fim,
                'preco_total': preco_total
            })

        except ValidationError as e:
            erro_mensagem = e.message

    return render(request, 'campo_detail.html', {'campo': campo, 'erro_mensagem': erro_mensagem})


def confirmar_reserva(request):
    campo_id = request.POST.get('campo_id')
    if request.method == 'POST':
        campo_id = request.POST.get('campo_id')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        preco_total = request.POST.get('preco_total')

        campo = get_object_or_404(Campo, id=campo_id)

        reserva = Reserva(
            usuario=request.user,
            campo=campo,
            data_inicio=data_inicio,
            data_fim=data_fim,
            preco_total=preco_total
        )


        reserva.clean()
        reserva.save()

        return redirect('usuarios:index')
    return redirect('reservas:reservar', campo_id=campo_id)

@login_required
def historico_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user).order_by('-data_inicio')
    now = timezone.now()
    return render(request, 'historico_reservas.html', {
        'reservas': reservas,
        'now' : now, })

def test_email_view(request):
    subject = 'Test Email'
    message = 'This is a test email sent from Django.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['juaumtest29@gmail.com']
    try:
        send_mail(subject, message, from_email, recipient_list)
        return HttpResponse("Test email sent successfully!")
    except Exception as e:
        return HttpResponse(f"Error sending email: {str(e)}")