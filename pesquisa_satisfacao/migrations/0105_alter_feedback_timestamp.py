# Generated by Django 4.2.3 on 2023-10-31 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pesquisa_satisfacao', '0104_alter_feedback_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='timestamp',
            field=models.CharField(default='2023-10-31 17:56:15', max_length=19),
        ),
    ]
