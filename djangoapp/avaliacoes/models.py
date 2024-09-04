from django.db import models
from django.contrib.auth.models import User
from campos.models import Campo

class Avaliacao(models.Model):
    campo = models.ForeignKey(Campo, on_delete=models.CASCADE, related_name='avaliacoes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    estrelas = models.PositiveIntegerField()  # Número de estrelas, de 1 a 5
    comentario = models.TextField(blank=True, null=True)  # Comentário opcional
    data_criacao = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('usuario', 'campo')

    def __str__(self):
        return f'Avaliação de {self.usuario} para {self.campo}'