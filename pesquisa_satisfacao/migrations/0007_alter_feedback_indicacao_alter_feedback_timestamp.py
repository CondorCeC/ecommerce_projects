# Generated by Django 4.2.1 on 2023-06-23 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pesquisa_satisfacao', '0006_alter_feedback_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='indicacao',
            field=models.CharField(choices=[('sim', 'Sim'), ('nao', 'Não'), ('null', 'Null')], max_length=4),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='timestamp',
            field=models.CharField(default='2023-06-23 09:54:00', max_length=19),
        ),
    ]
