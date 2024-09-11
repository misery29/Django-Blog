from django.contrib import admin
from .models import Campo
from reservas.models import Reserva
from django.http import HttpResponse
import csv
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from django.utils.dateparse import parse_datetime

class CampoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'endereco', 'dimensao', 'preco_por_hora', 'tipo_gramado', 'iluminacao_noturna', 'vestiarios', 'foto')
    list_filter = ('cidade', 'tipo_gramado', 'iluminacao_noturna', 'vestiarios')
    search_fields = ('nome', 'cidade', 'endereco')

    def get_actions(self, request):
        actions = super().get_actions(request)
        # Ensure actions are available for all
        return actions

    def exportar_campos_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="campos_reservas.csv"'

        writer = csv.writer(response)
        writer.writerow(['Campo', 'Cidade', 'Endereço', 'Total de Reservas', 'Lucro Total (R$)'])

        for campo in queryset:
            reservas = Reserva.objects.filter(campo=campo)
            total_reservas = reservas.count()
            lucro_total = sum([reserva.preco_total for reserva in reservas])

            writer.writerow([campo.nome, campo.cidade, campo.endereco, total_reservas, f'R$ {lucro_total:.2f}'])

        return response

    exportar_campos_csv.short_description = 'Exportar dados dos campos como CSV'

    def exportar_campos_pdf(self, request, queryset):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []

        styles = getSampleStyleSheet()
        elements.append(Paragraph("Relatório de Campos", styles['Title']))

        # Dados dos campos e reservas
        data = [['Campo', 'Cidade', 'Endereço', 'Total de Reservas', 'Lucro Total (R$)']]
        for campo in queryset:
            reservas = Reserva.objects.filter(campo=campo)
            total_reservas = reservas.count()
            lucro_total = sum([reserva.preco_total for reserva in reservas])
            data.append([campo.nome, campo.cidade, campo.endereco, str(total_reservas), f'R$ {lucro_total:.2f}'])
        
        # Estilos da tabela
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)

        doc.build(elements)
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

    exportar_campos_pdf.short_description = 'Exportar dados dos campos como PDF'

    actions = ['exportar_campos_csv', 'exportar_campos_pdf']

admin.site.register(Campo, CampoAdmin)