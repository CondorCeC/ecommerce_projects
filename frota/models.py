from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from PIL import Image
from sacs.models import Category
def custom_upload_to(instance, filename):
    # Obter a extensão do arquivo
    ext = filename.split('.')[-1]
    
    # Formate o nome do arquivo como desejado
    new_filename = f"{instance.numero_pedido}_{instance.group}.{ext}"
    
    # Retorne o caminho onde o arquivo deve ser armazenado
    return f'pictures/{new_filename}'
class Entrega(models.Model):
    STATUS_CHOICES = (
    ('Emitido', 'Emitido'),  
    ('Exportado', 'Exportado'),
    ('Em Rota', 'Em Rota'),
    ('Concluído', 'Concluído'),
    ('Tentativa', 'Tentativa'),
    ('Reentrega', 'Reentrega'),
    
    )
    PAG_CHOICES = (
    ('Online', 'Online'),
    ('Offline', 'Offline'),
    )
    JANELA_ENT = (
    ('09:00 às 13:00', '09:00 às 13:00'),
    ('09:00 às 14:00', '09:00 às 14:00'),
    ('12:00 às 17:00', '12:00 às 17:00'),
    ('13:00 às 17:00', '13:00 às 17:00'),
    ('14:00 às 20:00', '14:00 às 20:00'),
    ('17:00 às 20:00', '17:00 às 20:00'),
    )
  
    first_name = models.CharField(max_length=50, verbose_name='Nome Cliente')
    numero_pedido = models.CharField(max_length=50, verbose_name='Número Pedido')
    phone = models.CharField(max_length=50, verbose_name='Telefone')
    email = models.EmailField(max_length=254, blank=True)
    #created_date = models.DateTimeField(null=True, blank=True, verbose_name='Data Criação')
    data_ent = models.DateTimeField(null=True, blank=True, verbose_name='Data Entrega')
    janela = models.CharField(max_length=20, choices=JANELA_ENT, default='09:00 às 13:00', verbose_name='Janela de Entrega')
    description = models.CharField(max_length=255, blank=True, verbose_name='Descrição')
    show = models.BooleanField(default=True)
    picture = models.ImageField(blank=True, upload_to=custom_upload_to, verbose_name='Canhoto')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Categoria')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Usuário')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Aguardando')
    pagamento = models.CharField(max_length=20, choices=PAG_CHOICES, default='Offline')
    timestamp = models.DateTimeField(null=True, blank=True, verbose_name='Horário Finalização')
    endereco = models.CharField(max_length=255, null=True, blank=True, verbose_name='Endereço')
    bairro = models.CharField(max_length=40, null=True, blank=True, verbose_name='Bairro')
    final_lat = models.FloatField(null=True, blank=True, verbose_name='Latitude')
    final_lng = models.FloatField(null=True, blank=True, verbose_name='Longitude')
    end_final = models.CharField(max_length=255, null=True, blank=True, verbose_name='Endereço Finalização')
    description_store = models.TextField(blank=True, verbose_name='Obs Motorista')
    group = models.ForeignKey(Group, on_delete=models.PROTECT, null=True, blank=False, verbose_name='Loja')
   
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.numero_pedido}'
    


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 


        if self.picture:
            img = Image.open(self.picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (600, 600)
                img.thumbnail(output_size)
                img.save(self.picture.path)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLES = (
        ('M', 'Motorista'),
        ('S', 'Supervisor'),
    )
    role = models.CharField(max_length=1, choices=ROLES, default='M') 
    def __str__(self) -> str:
        return f'{self.user}'
class Insucesso(models.Model):
    entrega = models.ForeignKey(Entrega, on_delete=models.DO_NOTHING, related_name="insucessos")
    img_insucesso = models.ImageField(null=True, blank=True, upload_to='pictures/%Y/%m', verbose_name='Imagem Insucesso')
    hora_ins = models.DateTimeField(null=True, blank=True, verbose_name='Horário Insucesso')
    end_ins = models.CharField(max_length=255, null=True, blank=True, verbose_name='Endereço Insucesso')
    description_ins = models.CharField(max_length=255, null=True, blank=True, verbose_name='Obs Insucesso')
    final_lat2 = models.FloatField(null=True, blank=True, verbose_name='Latitude Insucesso')
    final_lng2 = models.FloatField(null=True, blank=True, verbose_name='Longitude Insucesso')
class EntregaLog(models.Model):
    entrega = models.ForeignKey(Entrega, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) 
    action = models.CharField(max_length=255, verbose_name='Ação')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Horário Finalização')
    
    def __str__(self):
        return f"{self.user} - {self.action} at {self.timestamp}"

