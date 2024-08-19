from django.contrib import admin
from .models import Reserva

class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'campo', 'data_inicio', 'data_fim', 'preco_total')
    # Permitir ao admin bloquear horários sem associar a um usuário específico
    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = request.user
        obj.save()
        
admin.site.register(Reserva, ReservaAdmin)