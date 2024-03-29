# Generated by Django 4.2.1 on 2023-06-22 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.TextField(max_length=255)),
                ('rating', models.IntegerField()),
                ('selected_options', models.TextField()),
                ('indicacao', models.CharField(choices=[('sim', 'Sim'), ('nao', 'Não')], max_length=3)),
            ],
        ),
    ]
