# Generated by Django 4.2.3 on 2023-11-03 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pesquisa_satisfacao', '1359_alter_feedback_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='timestamp',
            field=models.CharField(default='2023-11-02 21:08:29', max_length=19),
        ),
    ]
