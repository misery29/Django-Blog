# Generated by Django 4.2.15 on 2024-08-22 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campo',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='campo',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
