# Generated by Django 4.2.3 on 2023-11-03 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pesquisa_satisfacao', '1765_alter_feedback_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='timestamp',
            field=models.CharField(default='2023-11-03 09:31:34', max_length=19),
        ),
    ]
