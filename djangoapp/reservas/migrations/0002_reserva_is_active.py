# Generated by Django 4.2.16 on 2024-09-05 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
