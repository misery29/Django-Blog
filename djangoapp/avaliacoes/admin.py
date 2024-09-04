from django.contrib import admin
from .models import Avaliacao

class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('campo', 'usuario', 'estrelas', 'comentario', 'data_criacao', 'is_active')
    list_filter = ('is_active', 'campo', 'usuario')
    search_fields = ('campo__nome', 'usuario__username', 'comentario')
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Avaliações selecionadas foram marcadas como ativas.")

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Avaliações selecionadas foram marcadas como inativas.")

    make_active.short_description = "Marcar como Ativa"
    make_inactive.short_description = "Marcar como Inativa"

admin.site.register(Avaliacao, AvaliacaoAdmin)