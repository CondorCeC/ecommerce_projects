# Generated by Django 4.2.3 on 2023-11-01 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pesquisa_satisfacao', '0780_alter_feedback_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='timestamp',
            field=models.CharField(default='2023-11-01 18:30:29', max_length=19),
        ),
    ]
