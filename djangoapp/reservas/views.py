from django.shortcuts import render, get_object_or_404, redirect
from .models import Campo, Reserva
from django.contrib.auth.models import User
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
                data_fim__gt=data_inicio,
                is_active=True
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
            preco_total=preco_total,
            is_active = True
        )


        reserva.clean()
        reserva.save()

        # Notificação para usuários
        assunto_usuario = 'Confirmação de Reserva'
        mensagem_usuario = f"Olá {request.user.username}, sua reserva no campo {campo.nome} foi confirmada para {data_inicio} até {data_fim}."
        email_usuario = request.user.email
        send_mail(assunto_usuario, mensagem_usuario, settings.EMAIL_HOST_USER, [email_usuario])

        # Notificação para os administradores
        assunto_admin = 'Nova Reserva Feita'
        mensagem_admin = f"O usuário {request.user.username} fez uma nova reserva no campo {campo.nome} para o período de {data_inicio} até {data_fim}."
        admins = User.objects.filter(is_staff=True).values_list('email', flat=True)
        send_mail(assunto_admin, mensagem_admin, settings.EMAIL_HOST_USER, list(admins))


        return redirect('usuarios:index')
    return redirect('reservas:reservar', campo_id=campo_id)

@login_required
def historico_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user, is_active=True).order_by('-data_inicio')
    now = timezone.now()
    return render(request, 'historico_reservas.html', {
        'reservas': reservas,
        'now' : now, })

@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
    reserva.is_active = False
    reserva.save()
    return redirect('reservas:historico_reservas')