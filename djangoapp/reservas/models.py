from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from campos.models import *

class Reserva(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    campo = models.ForeignKey(Campo, on_delete=models.CASCADE)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    preco_total = models.DecimalField(max_digits=10, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Reserva de {self.usuario} no campo {self.campo} de {self.data_inicio} até {self.data_fim}"

    def clean(self):
        # Verificar se existe conflito de horário
        conflitos = Reserva.objects.filter(
            campo=self.campo,
            data_inicio__lt=self.data_fim,
            data_fim__gt=self.data_inicio
        ).exclude(id=self.pk)
        
        if conflitos.exists():
            raise ValidationError("Este horário já está reservado ou bloqueado!")

    def save(self, *args, **kwargs):
        self.clean()  # Verifica a disponibilidade antes de salvar
        super().save(*args, **kwargs)