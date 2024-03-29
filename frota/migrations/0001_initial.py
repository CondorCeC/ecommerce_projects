# Generated by Django 4.2.3 on 2023-10-20 18:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import frota.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sacs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entrega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='Nome Cliente')),
                ('numero_pedido', models.CharField(max_length=50, verbose_name='Número Pedido')),
                ('phone', models.CharField(max_length=50, verbose_name='Telefone')),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('data_ent', models.DateTimeField(blank=True, null=True, verbose_name='Data Entrega')),
                ('janela', models.CharField(choices=[('09:00 às 13:00', '09:00 às 13:00'), ('09:00 às 14:00', '09:00 às 14:00'), ('12:00 às 17:00', '12:00 às 17:00'), ('13:00 às 17:00', '13:00 às 17:00'), ('14:00 às 20:00', '14:00 às 20:00'), ('17:00 às 20:00', '17:00 às 20:00')], default='09:00 às 13:00', max_length=20, verbose_name='Janela de Entrega')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='Descrição')),
                ('show', models.BooleanField(default=True)),
                ('picture', models.ImageField(blank=True, upload_to=frota.models.custom_upload_to, verbose_name='Canhoto')),
                ('status', models.CharField(choices=[('Emitido', 'Emitido'), ('Exportado', 'Exportado'), ('Em Rota', 'Em Rota'), ('Concluído', 'Concluído'), ('Tentativa', 'Tentativa'), ('Reentrega', 'Reentrega')], default='Aguardando', max_length=20)),
                ('pagamento', models.CharField(choices=[('Online', 'Online'), ('Offline', 'Offline')], default='Offline', max_length=20)),
                ('timestamp', models.DateTimeField(blank=True, null=True, verbose_name='Horário Finalização')),
                ('endereco', models.CharField(blank=True, max_length=255, null=True, verbose_name='Endereço')),
                ('bairro', models.CharField(blank=True, max_length=40, null=True, verbose_name='Bairro')),
                ('final_lat', models.FloatField(blank=True, null=True, verbose_name='Latitude')),
                ('final_lng', models.FloatField(blank=True, null=True, verbose_name='Longitude')),
                ('end_final', models.CharField(blank=True, max_length=255, null=True, verbose_name='Endereço Finalização')),
                ('description_store', models.TextField(blank=True, verbose_name='Obs Motorista')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sacs.category', verbose_name='Categoria')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='auth.group', verbose_name='Loja')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('M', 'Motorista'), ('S', 'Supervisor')], default='M', max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Insucesso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_insucesso', models.ImageField(blank=True, null=True, upload_to='pictures/%Y/%m', verbose_name='Imagem Insucesso')),
                ('hora_ins', models.DateTimeField(blank=True, null=True, verbose_name='Horário Insucesso')),
                ('end_ins', models.CharField(blank=True, max_length=255, null=True, verbose_name='Endereço Insucesso')),
                ('description_ins', models.CharField(blank=True, max_length=255, null=True, verbose_name='Obs Insucesso')),
                ('final_lat2', models.FloatField(blank=True, null=True, verbose_name='Latitude Insucesso')),
                ('final_lng2', models.FloatField(blank=True, null=True, verbose_name='Longitude Insucesso')),
                ('entrega', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='insucessos', to='frota.entrega')),
            ],
        ),
        migrations.CreateModel(
            name='EntregaLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=255, verbose_name='Ação')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Horário Finalização')),
                ('entrega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frota.entrega')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
