# Generated by Django 4.2.1 on 2023-06-22 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pesquisa_satisfacao', '0004_feedback_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='timestamp',
            field=models.DateTimeField(default='2023-06-22T16:33:24'),
        ),
    ]
