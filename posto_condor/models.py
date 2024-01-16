from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class UserPosto(models.Model):
    class Meta:
        verbose_name = 'Usuário Posto'
        verbose_name_plural = 'Usuários Postos'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grupos = models.ManyToManyField(Group, blank=True, related_name="usuarios_grupos")
    CARGOS = (
        ('Coordenador', 'Coordenador'),
        ('Supervisor', 'Supervisor'),
        ('Gerente', 'Gerente'),
        ('Líder de Pista', 'Líder de Pista'),
        ('Líder de Loja', 'Líder de Loja'),
        ('Frentista', 'Frentista'),
        ('Operador de Caixa', 'Operador de Caixa'),
        ('Lubrificador', 'Lubrificador'),
        ('Atendente de Loja', 'Atendente de Loja'),
    )
    cargo = models.CharField(max_length=20, choices=CARGOS, default='') 
    foto = models.ImageField(upload_to='fotos_usuarios/', null=True, blank=True)
    pode_avaliar = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.user}'
    
    
class TipoAvaliacao(models.Model):
    class Meta:
        verbose_name = 'Tipo Avaliação'
        verbose_name_plural = 'Tipo Avaliações'
    titulo = models.CharField(max_length=255)
    cargo = models.CharField(max_length=20, choices=UserPosto.CARGOS, null=True, blank=True)


    def __str__(self):
        return self.titulo
class Subtopico(models.Model):
    TOPICOS = (
        ('Atendimento ao Cliente', 'Atendimento ao Cliente'),
        ('Responsabilidade', 'Responsabilidade'),
        ('Orientação para Resultados', 'Orientação para Resultados'),
        ('Habilidades Interpessoais', 'Habilidades Interpessoais'),
        ('Comunicação', 'Comunicação'),
        ('Conhecimento Específico', 'Conhecimento Específico'),
        ('Organização e Planejamento', 'Organização e Planejamento'),
        ('Orientação para Qualidade', 'Orientação para Qualidade'),
        ('Orientação para Pessoas', 'Orientação para Pessoas'),
        ('Segurança', 'Segurança'),

    )
    tipo_avaliacao = models.ForeignKey(TipoAvaliacao, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255, choices=TOPICOS, null=True, blank=True)
    last = models.BooleanField(default=False, null=True, blank=True, verbose_name='Campo Observação')

    def __str__(self):
        return self.nome
class Questao(models.Model):
    subtopico = models.ForeignKey(Subtopico, on_delete=models.CASCADE, null=True, blank=True)
    texto = models.CharField(max_length=255, null=True, blank=True)
    peso = models.FloatField(default=1.0)


    def __str__(self):
        return self.texto
    
class Avaliacao(models.Model):
    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
    user_posto = models.ForeignKey(UserPosto, on_delete=models.CASCADE, null=True, blank=True)
    data_ava = models.DateTimeField(verbose_name='Data Avaliação', null=True, blank=True)
    medias_subtopicos = models.JSONField(default=dict, blank=True, null=True, verbose_name='Médias por Subtópico')
    media_geral = models.FloatField(null=True, blank=True, verbose_name='Média Geral')
    Loja = models.CharField(null=True, blank=True, verbose_name='Loja')
    cargo = models.CharField(max_length=20, null=True, blank=True, verbose_name='Cargo')
    avaliador = models.CharField(max_length=20, null=True, blank=True, verbose_name='Avaliador')
    observacao = models.CharField(max_length=800, null=True, blank=True, verbose_name='Observação')

    def __str__(self) -> str:
        return f"Avaliação de {self.user_posto} em {self.data_ava}"

class Resposta(models.Model):
    OPCOES_RESPOSTA = (
        (1.0, 'Atende'),
        (0.0, 'Não atende'),
    )
    
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, null=True, blank=True)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    resposta = models.FloatField(choices=OPCOES_RESPOSTA)
    
    def save(self, *args, **kwargs):
        if self.resposta == 1.0:
            self.resposta = self.questao.peso
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Resposta de {self.avaliacao.user_posto} para "{self.questao.texto}" - {self.get_resposta_display()}'
    
class MediaAvaliacao(models.Model):
    class Meta:
        verbose_name = 'Média Avaliação'
        verbose_name_plural = 'Média Avaliações'
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, null=True, blank=True)
    subtopico = models.ForeignKey(Subtopico, on_delete=models.CASCADE, null=True, blank=True)
    media = models.FloatField()

    def __str__(self):
        return f'Média de {self.avaliacao.user_posto} para sub-tópico "{self.subtopico}" na avaliação em {self.avaliacao.data_ava}'