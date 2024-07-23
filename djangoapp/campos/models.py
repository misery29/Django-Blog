from django.db import models

class Campo(models.Model):
    GRAMADO_CHOICES = [
        ('natural', 'Natural'),
        ('sintetico', 'Sintético'),
    ]

    nome = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    dimensao = models.CharField(max_length=50)
    preco_por_hora = models.DecimalField(max_digits=6, decimal_places=2)
    tipo_gramado = models.CharField(max_length=10, choices=GRAMADO_CHOICES)
    iluminacao_noturna = models.BooleanField(default=False)
    vestiarios = models.BooleanField(default=False)
    foto = models.ImageField(upload_to='fotos_campos/', null=True, blank=True)
    

    def __str__(self):
        return self.nome