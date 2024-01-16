from django.contrib import admin
from frota import models
from django.contrib.auth.models import User
import pytz
import openpyxl
from django.http import HttpResponse


class InsucessoInline(admin.TabularInline):
    model = models.Insucesso
    extra = 0 
    fields = ['img_insucesso', 'hora_ins', 'end_ins', 'description_ins', 'final_lat2', 'final_lng2'] 


@admin.register(models.Entrega)
class EntregaAdmin(admin.ModelAdmin):
    list_display = 'id', 'owner', 'show', 'status', 'endereco', 'data_ent', 'janela', 'picture', 'group',
    ordering = '-id',
    list_per_page = 50
    list_max_show_all = 200
    list_editable = 'status', 'show', 'endereco','data_ent','janela','group', 'owner'
    inlines = [InsucessoInline]
    def export_to_excel(self, request, queryset):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="entregas.xlsx"'
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        headers = ['id', 'Cliente', 'Pedido', 'Telefone', 'Email', 'Data Entrega', 'Janela Entrega',
                   'Descrição', 'Categoria', 'Usuario', 'Status', 'Pagamento', 'Endereço',
                   'Bairro','Horário Finalização', 'Latitude Insucesso', 'Longitude Insucesso', 
                   'Latitude Finalização', 'Longitude Finalização', 'Endereço Finalização',
                   'Obs Motorista' , 'Loja', 'Horário Insucesso', 'Endereço Insucesso', 'Observação Insucesso'
                   ]
        for col_num, header_title in enumerate(headers, 1):
            column_letter = openpyxl.utils.get_column_letter(col_num)
            worksheet[f'{column_letter}1'] = header_title
        next_row = 2  
        for entrega in queryset:
            insucessos = entrega.insucessos.all()
            horas_ins = [ins.hora_ins.astimezone(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S") for ins in insucessos if ins.hora_ins]
            worksheet[f'W{next_row}'] = ", ".join(horas_ins) if horas_ins else None
            enderecos_ins = [ins.end_ins for ins in insucessos if ins.end_ins]
            worksheet[f'X{next_row}'] = ", ".join(enderecos_ins) if enderecos_ins else None
            lat_ins = [str(ins.final_lat2) for ins in insucessos if ins.final_lat2]
            worksheet[f'P{next_row}'] = ", ".join(lat_ins) if lat_ins else None
            lng_ins = [str(ins.final_lng2) for ins in insucessos if ins.final_lng2]
            worksheet[f'Q{next_row}'] = ", ".join(lng_ins) if lng_ins else None
            descricoes_ins = [ins.description_ins for ins in insucessos if ins.description_ins]
            worksheet[f'Y{next_row}'] = ", ".join(descricoes_ins) if descricoes_ins else None
            worksheet[f'A{next_row}'] = entrega.id
            worksheet[f'B{next_row}'] = entrega.first_name
            worksheet[f'C{next_row}'] = entrega.numero_pedido
            worksheet[f'D{next_row}'] = entrega.phone
            worksheet[f'E{next_row}'] = entrega.email
            worksheet[f'F{next_row}'] = entrega.data_ent.astimezone(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S")
            worksheet[f'G{next_row}'] = entrega.janela
            worksheet[f'H{next_row}'] = entrega.description
            worksheet[f'I{next_row}'] = entrega.category.name if entrega.category else ''
            owner_name = entrega.owner.username if entrega.owner else ''
            worksheet[f'J{next_row}'] = owner_name
            worksheet[f'K{next_row}'] = entrega.status
            worksheet[f'L{next_row}'] = entrega.pagamento
            worksheet[f'M{next_row}'] = entrega.endereco
            worksheet[f'N{next_row}'] = entrega.bairro
            worksheet[f'O{next_row}'] = entrega.timestamp.astimezone(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S") if entrega.timestamp else None
            worksheet[f'R{next_row}'] = entrega.final_lat
            worksheet[f'S{next_row}'] = entrega.final_lng
            worksheet[f'T{next_row}'] = entrega.end_final
            worksheet[f'U{next_row}'] = entrega.description_store
            worksheet[f'V{next_row}'] = entrega.group.name if entrega.group else ''
            next_row += 1
        workbook.save(response)
        return response
    export_to_excel.short_description = 'Exportar para Excel'
    actions = [export_to_excel]
@admin.register(models.EntregaLog)
class EntregaLogAdmin(admin.ModelAdmin):
    list_display = 'user', 'entrega', 'action', 'timestamp', 

@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = 'id', 'user', 'role'

