# Generated by Django 4.2.3 on 2023-11-01 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pesquisa_satisfacao', '0562_alter_feedback_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='timestamp',
            field=models.CharField(default='2023-11-01 14:28:17', max_length=19),
        ),
    ]
