from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Avaliacao
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
        data_fim__lt=timezone.now()
    ).exists()

    if not reserva:
        return redirect('campos:detalhes', campo_id=campo_id)
    
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.campo = campo
            avaliacao.usuario = request.user
            avaliacao.save()
            return redirect('campos:detail_fields', pk=campo_id)
    else:
        form = AvaliacaoForm()
    
    return render(request, 'adicionar_avaliacao.html', {'form': form, 'campo': campo})
