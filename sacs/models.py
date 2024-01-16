from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from PIL import Image
# Create your models here.

class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    name = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.name

class Contact(models.Model):
    STATUS_CHOICES = (
    ('Novo', 'Novo'),
    ('Em atendimento', 'Em atendimento'),
    ('Pendente', 'Pendente'),
    ('Concluído', 'Concluído'),
    
    )
    ORIGEM_CHOICES = (
        ('loja', 'Loja'),
        ('sap', 'Sap'),
        ('chat', 'Chat'),
        ('RA', 'Ra'),
        ('whats', 'Whats'),
        ('Ligação', 'Ligação'),
        
    )
    first_name = models.CharField(max_length=50, verbose_name='Nome Cliente')
    last_name = models.CharField(max_length=50, verbose_name='Número Pedido')
    phone = models.CharField(max_length=50, verbose_name='Telefone')
    email = models.EmailField(max_length=254, blank=True)
    created_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True, verbose_name='Descrição')
    show = models.BooleanField(default=True)
    picture = models.ImageField(blank=True, upload_to='pictures/%Y/%m')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Categoria')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Usuário')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Novo')
    timestamp = models.DateTimeField(null=True, blank=True)
    inicio_atendimento = models.DateTimeField(null=True, blank=True)
    origem = models.CharField(max_length=20, choices=ORIGEM_CHOICES, null=True, blank=True)
    description_store = models.TextField(blank=True, verbose_name='Obs Loja')
    group = models.ForeignKey(Group, on_delete=models.PROTECT, null=True, blank=False, verbose_name='Loja')
   
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.

        # Check if picture exists
        if self.picture:
            img = Image.open(self.picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (600, 600)
                img.thumbnail(output_size)
                img.save(self.picture.path)
    

class ContactLog(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # assuming you are using Django's default User model
    action = models.CharField(max_length=255)  # e.g., 'Iniciar atendimento', 'Concluído'
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} - {self.action} at {self.timestamp}"

