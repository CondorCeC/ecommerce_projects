from django.db import models
from datetime import datetime
# Create your models here.  


class Feedback(models.Model):
    email = models.TextField(max_length=255, blank=False)
    rating = models.IntegerField()
    selected_options = models.TextField()
    indicacao = models.CharField(max_length=4, choices=[('sim', 'Sim'), ('nao', 'Não'), ('null', 'Null')])
    pedido = models.CharField(max_length=255, default='123456')
    timestamp = models.CharField(max_length=19, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    data_pedido = models.DateField(null=True, blank=True)  # Adicionado novo campo
    loja_id = models.CharField(max_length=4, null=True, blank=True)

    
    def __str__(self):
        return f"Rating: {self.rating}, Selected Options: {self.selected_options}, Feedback ID: {self.id}"
