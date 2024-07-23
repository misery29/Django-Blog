from django.contrib import admin
from .models import Campo

class CampoAdmin(admin.ModelAdmin):
   list_display = ('nome', 'cidade', 'endereco', 'dimensao', 'preco_por_hora', 'tipo_gramado', 'iluminacao_noturna', 'vestiarios', 'foto')
   list_filter = ('cidade', 'tipo_gramado', 'iluminacao_noturna', 'vestiarios')
   search_fields = ('nome', 'cidade', 'endereco')

admin.site.register(Campo, CampoAdmin)