# Generated by Django 4.2.3 on 2023-11-02 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pesquisa_satisfacao', '1311_alter_feedback_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='timestamp',
            field=models.CharField(default='2023-11-02 20:15:10', max_length=19),
        ),
    ]
