# Generated by Django 4.2.3 on 2023-11-06 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posto_condor', '0004_avaliacao_avaliador'),
    ]

    operations = [
        migrations.AddField(
            model_name='avaliacao',
            name='observacao',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Observação'),
        ),
    ]
