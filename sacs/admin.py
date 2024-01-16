from django.contrib import admin
from sacs import models
import openpyxl
from django.http import HttpResponse
import pandas as pd
from django.contrib.auth.models import User
import pytz



@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = 'id', 'owner','first_name', 'last_name', 'phone', 'show', 'status', 'created_date', 'timestamp', 'category', 'origem'
    ordering = '-id',
    # list_filter = 'created_date',
    search_fields = 'id', 'first_name', 'last_name',
    list_per_page = 10
    list_max_show_all = 200
    list_editable = 'first_name', 'last_name', 'show', 'status',
    list_display_links = 'id', 'phone',
    def export_to_excel(self, request, queryset):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="sacs.xlsx"'

        workbook = openpyxl.Workbook()
        worksheet = workbook.active

        # Defina os cabeçalhos das colunas
        headers = ['id', 'Cliente', 'Pedido', 'Telefone', 'Status', 'Data Criação', 'Data Finalização', 'Categoria', 'Loja', 'Origem', 'Início Atendimento', 'group']
        for col_num, header_title in enumerate(headers, 1):
            column_letter = openpyxl.utils.get_column_letter(col_num)
            worksheet[f'{column_letter}1'] = header_title

        # Adicione as informações do queryset nas células correspondentes
        next_row = 2  # Iniciar na linha 2

        for contact in queryset:
            worksheet[f'A{next_row}'] = contact.id
            worksheet[f'B{next_row}'] = contact.first_name
            worksheet[f'C{next_row}'] = contact.last_name
            worksheet[f'D{next_row}'] = contact.phone
            worksheet[f'E{next_row}'] = contact.status
            worksheet[f'F{next_row}'] = contact.created_date.astimezone(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S")
            worksheet[f'G{next_row}'] = contact.timestamp.astimezone(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S") if contact.timestamp else None
            worksheet[f'H{next_row}'] = contact.category.name if contact.category else ''
            owner_name = contact.owner.username if contact.owner else ''
            if owner_name == 'ahu_gourmet':
                owner_name = '17 - Ahú Gourmet'
            if owner_name == 'condor_cajuru':
                owner_name = '37 - Cajuru'
            worksheet[f'I{next_row}'] = owner_name
            worksheet[f'J{next_row}'] = contact.origem
            worksheet[f'K{next_row}'] = contact.inicio_atendimento.astimezone(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S") if contact.inicio_atendimento else None
            worksheet[f'L{next_row}'] = contact.group.name if contact.group else ''
            next_row += 1
        workbook.save(response)
        return response

    export_to_excel.short_description = 'Exportar para Excel'
    actions = [export_to_excel]
    
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name',
    ordering = '-id',
# @admin.register(models.AccessLog)
# class AccessLog(admin.ModelAdmin):
#     list_display = 'user', 'log_message', 'stamp'
@admin.register(models.ContactLog)
class ContactLogAdmin(admin.ModelAdmin):
    list_display = 'user', 'contact', 'action', 'timestamp', 