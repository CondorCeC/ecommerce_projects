# Generated by Django 4.2.3 on 2024-01-02 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posto_condor', '0006_alter_subtopico_nome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avaliacao',
            name='observacao',
            field=models.CharField(blank=True, max_length=800, null=True, verbose_name='Observação'),
        ),
    ]
