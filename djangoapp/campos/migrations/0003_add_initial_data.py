from django.db import migrations
from django.contrib.auth.models import User

def criar_campos_e_superusuario(apps, schema_editor):
    Campo = apps.get_model('campos', 'Campo')
    campos = [
        {
            'nome': 'Campo A',
            'cidade': 'Maricá',
            'endereco': 'Rua das Acácias, 123, Centro',
            'dimensao': '100x60',
            'preco_por_hora': 150.00,
            'tipo_gramado': 'natural',
            'iluminacao_noturna': True,
            'vestiarios': True,
        },
        {
            'nome': 'Campo B',
            'cidade': 'Maricá',
            'endereco': 'Avenida Beira-Mar, 456, Barra de Maricá',
            'dimensao': '120x70',
            'preco_por_hora': 200.00,
            'tipo_gramado': 'sintetico',
            'iluminacao_noturna': True,
            'vestiarios': False,
        },
        {
            'nome': 'Campo C',
            'cidade': 'Maricá',
            'endereco': 'Rua dos Palmeirais, 789, Ponta Negra',
            'dimensao': '90x50',
            'preco_por_hora': 100.00,
            'tipo_gramado': 'natural',
            'iluminacao_noturna': False,
            'vestiarios': True,
        },
        {
            'nome': 'Campo D',
            'cidade': 'Maricá',
            'endereco': 'Rua do Limoeiro, 101, Itaipuaçu',
            'dimensao': '110x65',
            'preco_por_hora': 180.00,
            'tipo_gramado': 'sintetico',
            'iluminacao_noturna': True,
            'vestiarios': True,
        },
        {
            'nome': 'Campo E',
            'cidade': 'Maricá',
            'endereco': 'Rua das Flores, 202, São José do Imbassaí',
            'dimensao': '105x60',
            'preco_por_hora': 160.00,
            'tipo_gramado': 'natural',
            'iluminacao_noturna': False,
            'vestiarios': False,
        },
        {
            'nome': 'Campo F',
            'cidade': 'Maricá',
            'endereco': 'Avenida Mário Cova, 303, Recanto das Rosas',
            'dimensao': '115x70',
            'preco_por_hora': 190.00,
            'tipo_gramado': 'sintetico',
            'iluminacao_noturna': True,
            'vestiarios': True,
        },
        {
            'nome': 'Campo G',
            'cidade': 'Maricá',
            'endereco': 'Rua dos Eucaliptos, 404, Jardim Atlântico',
            'dimensao': '130x75',
            'preco_por_hora': 210.00,
            'tipo_gramado': 'natural',
            'iluminacao_noturna': False,
            'vestiarios': True,
        },
        {
            'nome': 'Campo H',
            'cidade': 'Maricá',
            'endereco': 'Rua das Palmeiras, 505, Nova Maricá',
            'dimensao': '95x55',
            'preco_por_hora': 140.00,
            'tipo_gramado': 'sintetico',
            'iluminacao_noturna': True,
            'vestiarios': False,
        },
    ]
    
    for campo in campos:
        Campo.objects.create(**campo)

    username = "selecaoengsoftware@universidadedevassouras.edu.br"
    password = "default123"
    email = username

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)

class Migration(migrations.Migration):

    dependencies = [
        ('campos', '0002_campo_latitude_campo_longitude'),
    ]

    operations = [
        migrations.RunPython(criar_campos_e_superusuario),
    ]
