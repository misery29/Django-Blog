# Generated by Django 4.2.14 on 2024-07-22 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cidade', models.CharField(max_length=100)),
                ('endereco', models.CharField(max_length=255)),
                ('dimensao', models.CharField(max_length=50)),
                ('preco_por_hora', models.DecimalField(decimal_places=2, max_digits=6)),
                ('tipo_gramado', models.CharField(choices=[('natural', 'Natural'), ('sintetico', 'Sintético')], max_length=10)),
                ('iluminacao_noturna', models.BooleanField(default=False)),
                ('vestiarios', models.BooleanField(default=False)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='fotos_campos/')),
            ],
        ),
    ]
