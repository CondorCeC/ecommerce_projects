# Generated by Django 4.2.3 on 2024-01-02 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pesquisa_satisfacao', '2543_alter_feedback_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='timestamp',
            field=models.CharField(default='2024-01-02 10:34:33', max_length=19),
        ),
    ]
