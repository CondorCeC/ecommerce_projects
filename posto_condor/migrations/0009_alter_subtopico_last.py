# Generated by Django 4.2.3 on 2024-01-02 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posto_condor', '0008_subtopico_last'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtopico',
            name='last',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Campo Observação'),
        ),
    ]
