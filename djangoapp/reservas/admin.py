from django.contrib import admin
from .models import Reserva
from django.http import HttpResponse
import csv
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph


def exportar_reservas_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reservas.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Campo', 'Data de Início', 'Data de Fim', 'Preço Total (R$)', 'Receita (R$)'])
    
    total_lucro = 0
    campo_contagem = {}
    
    for reserva in queryset:
        data_inicio_formatada = reserva.data_inicio.strftime('%Y-%m-%d %H:%M')
        data_fim_formatada = reserva.data_fim.strftime('%Y-%m-%d %H:%M')
        writer.writerow([reserva.campo.nome, data_inicio_formatada, data_fim_formatada, f"{reserva.preco_total:.2f}", f"{reserva.preco_total:.2f}"])
        total_lucro += reserva.preco_total
        campo_contagem[reserva.campo.nome] = campo_contagem.get(reserva.campo.nome, 0) + 1

    # Resumo financeiro no final
    writer.writerow([])
    writer.writerow(['Resumo Financeiro'])
    writer.writerow(['Total de Reservas', queryset.count()])
    writer.writerow(['Lucro Total (R$)', f"{total_lucro:.2f}"])

    # Contagem por campo
    writer.writerow(['Reservas por Campo'])
    for campo, contagem in campo_contagem.items():
        writer.writerow([campo, f"{contagem} reserva(s)"])
    
    return response

exportar_reservas_csv.short_description = 'Exportar dados das reservas como CSV'

def exportar_reservas_pdf(modeladmin, request, queryset):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # Título
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Relatório de Reservas", styles['Title']))
    
    # Dados das reservas
    data = [['Campo', 'Data de Início', 'Data de Fim', 'Preço Total (R$)']]
    total_lucro = 0
    campo_contagem = {}
    
    for reserva in queryset:
        data_inicio_formatada = reserva.data_inicio.strftime('%Y-%m-%d %H:%M')
        data_fim_formatada = reserva.data_fim.strftime('%Y-%m-%d %H:%M')
        data.append([reserva.campo.nome, data_inicio_formatada, data_fim_formatada, f"{reserva.preco_total:.2f}"])
        total_lucro += reserva.preco_total
        campo_contagem[reserva.campo.nome] = campo_contagem.get(reserva.campo.nome, 0) + 1
    
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
    
    # Resumo financeiro
    elements.append(Paragraph(f"Total de Reservas: {queryset.count()}", styles['Heading2']))
    elements.append(Paragraph(f"Lucro Total (R$): {total_lucro:.2f}", styles['Heading2']))
    
    
    doc.build(elements)
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
exportar_reservas_pdf.short_description = 'Exportar dados das reservas como PDF'

class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'campo', 'data_inicio', 'data_fim', 'preco_total', 'is_active')
    readonly_fields = ('preco_total', 'criado_em', 'is_active')
    
    actions = [exportar_reservas_csv, exportar_reservas_pdf]

    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = request.user
        obj.save()

admin.site.register(Reserva, ReservaAdmin)
