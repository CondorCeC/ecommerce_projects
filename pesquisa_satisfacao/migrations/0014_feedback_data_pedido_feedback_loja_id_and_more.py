# Generated by Django 4.2.3 on 2023-10-20 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pesquisa_satisfacao', '0013_alter_feedback_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='data_pedido',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='feedback',
            name='loja_id',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='timestamp',
            field=models.CharField(default='2023-10-20 14:40:57', max_length=19),
        ),
    ]
