from django.contrib import admin
from .models import UserPosto, TipoAvaliacao, Questao, Resposta, Subtopico, MediaAvaliacao, Avaliacao
import pandas as pd
from django.http import HttpResponse


class RespostaInline(admin.TabularInline):  
    model = Resposta
    extra = 0

# @admin.register(Avaliacao)
# class AvaliacaoAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user_posto', 'data_ava', 'medias_subtopicos', 'media_geral', 'Loja', 'cargo', 'avaliador')
#     inlines = [RespostaInline]
@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_posto', 'data_ava', 'medias_subtopicos', 'media_geral', 'Loja', 'cargo', 'avaliador')
    inlines = [RespostaInline]
    actions = ['exportar_avaliacoes_para_excel']  # Adicionando a ação personalizada

    def exportar_avaliacoes_para_excel(self, request, queryset):
        avaliacoes_data = []
        for avaliacao in queryset.prefetch_related('resposta_set'):
            for resposta in avaliacao.resposta_set.all():
                avaliacoes_data.append({
                'ID da Avaliação': avaliacao.id,
                'Usuário': avaliacao.user_posto.user.username,
                'Loja': avaliacao.Loja,
                'Cargo': avaliacao.cargo,
                'Avaliador': avaliacao.avaliador,
                'Data da Avaliação': avaliacao.data_ava,
                'Subtópico': resposta.questao.subtopico.nome if resposta.questao.subtopico else '',
                'Questão': resposta.questao.texto,
                'Resposta': resposta.resposta,
                'Médias por Subtópico': avaliacao.medias_subtopicos.get(resposta.questao.subtopico.nome, ''),
                'Média Geral': avaliacao.media_geral,
                'Observação': avaliacao.observacao,
            })

        avaliacoes_df = pd.DataFrame(avaliacoes_data)
        avaliacoes_df['Data da Avaliação'] = pd.to_datetime(avaliacoes_df['Data da Avaliação']).dt.strftime('%Y-%m-%d %H:%M:%S')
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=avaliacoes.xlsx'

        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            avaliacoes_df.to_excel(writer, index=False, sheet_name='Avaliações')

        return response

    exportar_avaliacoes_para_excel.short_description = "Exportar avaliações selecionadas para Excel"

@admin.register(UserPosto)
class UserPostoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'cargo', 'pode_avaliar', 'foto', 'get_grupos')
    list_editable = ('pode_avaliar', 'foto', 'cargo')
    def get_grupos(self, obj):
        return ", ".join([grupo.name for grupo in obj.grupos.all()])
    get_grupos.short_description = 'Grupos' 
@admin.register(Resposta)
class RespostaAdmin(admin.ModelAdmin):
    list_display = ('id', 'avaliacao', 'questao', 'get_resposta_display')
    list_filter = ('avaliacao', 'questao')
    search_fields = ('avaliacao__user_posto__user__username', 'questao__texto')

@admin.register(MediaAvaliacao)
class MediaAvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'avaliacao', 'subtopico', 'media')
    list_filter = ('avaliacao', 'subtopico')

class QuestaoInline(admin.StackedInline): 
    model = Questao
    extra = 10

@admin.register(Subtopico)
class SubtopicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_avaliacao')
    list_editable = ('tipo_avaliacao',)
    inlines = [QuestaoInline]  

class SubtopicoInline(admin.StackedInline):
    model = Subtopico
    extra = 1

@admin.register(TipoAvaliacao)
class TipoAvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'titulo')
    list_editable = ('titulo',)
    inlines = [SubtopicoInline]
