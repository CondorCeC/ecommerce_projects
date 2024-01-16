from django.shortcuts import render, redirect, get_object_or_404
from .models import TipoAvaliacao, Questao, UserPosto, Resposta, Subtopico, MediaAvaliacao, Avaliacao
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from posto_condor.forms import RespostaForm
from django.utils import timezone
import requests
import json
from datetime import datetime
from rest_framework import generics
from .serializers import  AutoPostoAvSerializer
import openpyxl
from django.http import HttpResponse
import pandas as pd

def index_posto(request):
    tipos_avaliacao = TipoAvaliacao.objects.all()
    context = {
            'tipos_avaliacao': tipos_avaliacao
        }
    return render(request, 'posto_condor/pesquisas.html', context)

def iniciar_avaliacao(request):
    try:
        user_posto_logado = UserPosto.objects.get(user=request.user)
        cargos_avaliaveis = cargos_que_pode_avaliar(user_posto_logado.cargo)
        context = {'cargos': cargos_avaliaveis}
    except UserPosto.DoesNotExist:

        context = {'error_message': 'UserPosto não encontrado.'}
    return render(request, 'posto_condor/iniciar_avaliacao.html', context)

def listar_usuarios_por_cargo(request, cargo):
    usuarios = UserPosto.objects.filter(cargo=cargo)
    user_posto_logado = UserPosto.objects.get(user=request.user)

    usuarios = usuarios.filter(grupos__in=user_posto_logado.grupos.all())

    return render(request, 'posto_condor/listar_usuarios.html', {'usuarios': usuarios})

def calcular_media_subtopico(respostas):
    total = sum([resposta.resposta for resposta in respostas])
    return total / len(respostas) if respostas else 0

def cargos_que_pode_avaliar(cargo):
    HIERARQUIA = {
        'Coordenador': ['Frentista', 'Operador de Caixa', 'Lubrificador', 'Atendente de Loja', 'Gerente','Líder de Pista', 'Líder de Loja'],
        'Supervisor': ['Frentista', 'Operador de Caixa', 'Lubrificador', 'Atendente de Loja', 'Gerente','Líder de Pista', 'Líder de Loja'],
        'Gerente': ['Líder de Pista', 'Líder de Loja','Frentista', 'Operador de Caixa', 'Lubrificador', 'Atendente de Loja'],
        'Líder de Pista': ['Frentista', 'Operador de Caixa', 'Lubrificador', 'Atendente de Loja'],
        'Líder de Loja': ['Operador de Caixa', 'Atendente de Loja'],
    }
    return HIERARQUIA.get(cargo, [])

def filtrar_por_grupo(queryset, user):
    return queryset.filter(user_posto__grupos__in=user.groups.all())

def filtrar_por_hierarquia(queryset, cargo_usuario):
    cargos_avaliaveis = cargos_que_pode_avaliar(cargo_usuario)
    return queryset.filter(user_posto__cargo__in=cargos_avaliaveis)

def avaliar_usuario(request, userposto_id):
    usuario = get_object_or_404(UserPosto, id=userposto_id)
    avaliador = UserPosto.objects.get(user=request.user)
    obs = request.POST.get('comentarios')
    grupo = usuario.grupos.first()  # Replace with your logic if needed
    grupo_name = grupo.name if grupo else None
    tipo_avaliacao = TipoAvaliacao.objects.get(cargo=usuario.cargo)
    subtopicos = Subtopico.objects.filter(tipo_avaliacao=tipo_avaliacao)
    medias_subtopicos = {}
   
    if request.method == 'POST':
        
        
        avaliacao = Avaliacao.objects.create(
        user_posto=usuario, 
        data_ava=timezone.now(),
        Loja=grupo_name,
        cargo=usuario.cargo,
        avaliador=avaliador.user.username,
        observacao=obs
    )
        for subtopico in subtopicos:
            questoes = Questao.objects.filter(subtopico=subtopico)
            for questao in questoes:
                resposta_valor = request.POST.get(f'resposta_{questao.id}')
                if resposta_valor:
                    resposta_valor = resposta_valor.replace(',', '.')
                    Resposta.objects.create(
                        avaliacao=avaliacao,
                        questao=questao,
                        resposta=float(resposta_valor)
                    )
            respostas = Resposta.objects.filter(avaliacao=avaliacao, questao__subtopico=subtopico)
            medias_subtopicos[subtopico.nome] = calcular_media_subtopico(respostas)
            media_subtopico = calcular_media_subtopico(respostas)
            medias_subtopicos[subtopico.nome] = round(media_subtopico, 2)  
            print(medias_subtopicos)
            data_ava = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            MediaAvaliacao.objects.create(
                avaliacao=avaliacao,
                subtopico=subtopico,
                media=medias_subtopicos[subtopico.nome],
            )
        media_geral = sum(medias_subtopicos.values()) / len(medias_subtopicos) if medias_subtopicos else 0
        avaliacao.data_ava = data_ava
        user_posto = avaliacao.user_posto.user.username
        
        avaliacao.media_geral = round(media_geral, 2)
        avaliacao.media_geral = media_geral
        avaliacao.medias_subtopicos = medias_subtopicos
        avaliacao.save()

        MediaAvaliacao.objects.create(
            avaliacao=avaliacao,
            media=media_geral
        )
        return redirect('posto:listar_avaliacoes')  
    subtopicos = Subtopico.objects.filter(tipo_avaliacao=tipo_avaliacao).order_by('id')  
    subtopicos_com_last = subtopicos.filter(last=True)

    #ultimo_subtopico = subtopicos.last() if subtopicos else None
    ultimo_subtopico = subtopicos_com_last.first() if subtopicos_com_last.exists() else None

    context = {
        'usuario': usuario,
        'subtopicos': subtopicos,
        'tipo_avaliacao': tipo_avaliacao,
        'ultimo_subtopico': ultimo_subtopico,
       
    }

    # Passe o contexto para o template
    return render(request, 'posto_condor/avaliacao.html', context)



class AutoPostoListAv(generics.ListCreateAPIView):
    queryset = Avaliacao.objects.all()
    serializer_class = AutoPostoAvSerializer


@login_required
def listar_avaliacoes(request):
    try:
        user_posto_logado = UserPosto.objects.get(user=request.user)
        avaliacoes = Avaliacao.objects.all()
        avaliacoes = filtrar_por_grupo(avaliacoes, request.user)
        avaliacoes = filtrar_por_hierarquia(avaliacoes, user_posto_logado.cargo)
        context = {
            'avaliacoes': avaliacoes,
            'cargo_usuario_logado': user_posto_logado.cargo, 
        }
    except:
        context = {'error_message': 'UserPosto não encontrado.'}
    

    return render(request, 'posto_condor/listar_avaliacoes.html', context)



@login_required
def ver_avaliacao(request, userposto_id):
    user_posto_logado = UserPosto.objects.get(user=request.user)
    avaliacao = get_object_or_404(Avaliacao, id=userposto_id)

    if avaliacao.user_posto.cargo not in cargos_que_pode_avaliar(user_posto_logado.cargo):
        messages.error(request, 'Você não tem permissão para ver essa avaliação.')
        return redirect('posto:listar_avaliacoes')

    respostas = Resposta.objects.filter(avaliacao=avaliacao).select_related('questao', 'questao__subtopico')

    respostas_por_subtopico = {}
    for resposta in respostas:
        subtopico = resposta.questao.subtopico
        if subtopico not in respostas_por_subtopico:
            respostas_por_subtopico[subtopico] = []
        respostas_por_subtopico[subtopico].append(resposta)
    medias = MediaAvaliacao.objects.filter(avaliacao=avaliacao)
    medias_subtopicos = {media.subtopico: media.media for media in medias if media.subtopico}
    media_geral = next((media.media for media in medias if not media.subtopico), 0)
    return render(request, 'posto_condor/ver_avaliacao.html', {
        'avaliacao': avaliacao, 
        'respostas_por_subtopico': respostas_por_subtopico,
        'medias_subtopicos': medias_subtopicos,
        'media_geral': media_geral
    })



def exportar_avaliacoes_para_excel(request):
    avaliacoes_queryset = Avaliacao.objects.all().prefetch_related('resposta_set')
    
   
    avaliacoes_data = []
    for avaliacao in avaliacoes_queryset:
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


# Defs que lidam com Login
def login_posto(request):
    form = AuthenticationForm(request)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, f'Logado com sucesso como {user}!')
            return redirect('posto:iniciar_avaliacao')
        messages.error(request, 'Login inválido')
    return render(
        request,
        'posto_condor/login_posto.html',
        {
            'form': form
        }
    )
@login_required(login_url='entrega:login_entrega')
def logout_posto(request):
    auth.logout(request)
    return redirect('posto:index_posto')



