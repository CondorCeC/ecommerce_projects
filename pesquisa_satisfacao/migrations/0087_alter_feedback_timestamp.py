# Generated by Django 4.2.3 on 2023-10-31 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pesquisa_satisfacao', '0086_alter_feedback_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='timestamp',
            field=models.CharField(default='2023-10-31 17:36:02', max_length=19),
        ),
    ]
