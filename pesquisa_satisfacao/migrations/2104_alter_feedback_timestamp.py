# Generated by Django 4.2.3 on 2023-11-03 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pesquisa_satisfacao', '2103_alter_feedback_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='timestamp',
            field=models.CharField(default='2023-11-03 13:42:23', max_length=19),
        ),
    ]
