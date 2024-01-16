from rest_framework import serializers
from .models import  Avaliacao, Resposta


class RespostaSerializer(serializers.ModelSerializer):
    questao_texto = serializers.CharField(source='questao.texto')
    
    class Meta:
        model = Resposta
        fields = ['questao_id', 'questao_texto', 'resposta']

class AutoPostoAvSerializer(serializers.ModelSerializer):
    medias_subtopicos = serializers.SerializerMethodField()
    media_geral = serializers.FloatField()
    respostas = RespostaSerializer(many=True, source='resposta_set')
    user_posto = serializers.CharField(source='user_posto.user.username')
    data_ava = serializers.DateTimeField()
    
    class Meta:
        model = Avaliacao
        fields = ['id', 'user_posto', 'Loja', 'cargo', 'avaliador',  'data_ava', 'medias_subtopicos', 'media_geral', 'respostas', 'observacao']
    
    def get_medias_subtopicos(self, obj):
      
        return obj.medias_subtopicos
