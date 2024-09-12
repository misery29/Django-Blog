from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Avaliacao
from .models import User
from django.core.mail import send_mail
from django.conf import settings
from campos.models import Campo
from reservas.models import Reserva
from django.contrib.auth.decorators import login_required
from .forms import AvaliacaoForm

@login_required
def adicionar_avaliacao(request, campo_id):
    campo = get_object_or_404(Campo, id=campo_id)
    
    # Verifique se o usuário tem uma reserva concluída para este campo
    reserva = Reserva.objects.filter(
        campo=campo,
        usuario=request.user,
        data_fim__lt=timezone.now(),
        is_active=True
    ).exists()

    if not reserva:
        return redirect('campos:detail_fields', pk=campo_id)
    
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.campo = campo
            avaliacao.usuario = request.user
            avaliacao.save()

            assunto_admin="Nova avaliação para o campo {0}".format(campo.nome)
            mensagem_admin=f'O usuário {request.user.email} enviou uma avaliação para o campo {campo.nome}.'
            admins = User.objects.filter(is_staff=True).values_list('email', flat=True)               
            send_mail(assunto_admin, mensagem_admin, settings.EMAIL_HOST_USER, list(admins))
            return redirect('campos:detail_fields', pk=campo_id)
    else:
        form = AvaliacaoForm()
    
    return render(request, 'adicionar_avaliacao.html', {'form': form, 'campo': campo})
