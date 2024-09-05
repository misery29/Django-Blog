from django.contrib import admin
from .models import Reserva

class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'campo', 'data_inicio', 'data_fim', 'preco_total', 'is_active')
    readonly_fields = ('preco_total', 'criado_em', 'is_active')
    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = request.user
        obj.save()
        
admin.site.register(Reserva, ReservaAdmin)