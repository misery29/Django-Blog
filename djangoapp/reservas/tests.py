from django.test import TestCase
from django.utils import timezone
from reservas.models import Reserva
from campos.models import Campo
from django.contrib.auth.models import User
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.urls import reverse
from django import forms
from reservas.forms import ReservaForm

class ReservaModelTest(TestCase):
    def setUp(self):
        # Criação de dados de teste
        self.user = User.objects.create_user(username='user', password='pass')
        self.campo = Campo.objects.create(nome='Campo 1', preco_por_hora=100)

    def test_reserva_conflito(self):
        data_inicio_existente = timezone.now()
        data_fim_existente = data_inicio_existente + timedelta(hours=2)
        Reserva.objects.create(
            usuario=self.user,
            campo=self.campo,
            data_inicio=data_inicio_existente,
            data_fim=data_fim_existente,
            preco_total=200
        )

        # Tentar criar uma nova reserva que sobreponha a existente
        data_inicio_nova = data_inicio_existente + timedelta(hours=1)
        data_fim_nova = data_fim_existente + timedelta(hours=1)

        reserva = Reserva(
            usuario=self.user,
            campo=self.campo,
            data_inicio=data_inicio_nova,
            data_fim=data_fim_nova,
            preco_total=150
        )

        with self.assertRaises(ValidationError):
            reserva.clean()

    def test_reserva_sem_conflito(self):
        data_inicio_existente = timezone.now()
        data_fim_existente = data_inicio_existente + timedelta(hours=2)
        Reserva.objects.create(
            usuario=self.user,
            campo=self.campo,
            data_inicio=data_inicio_existente,
            data_fim=data_fim_existente,
            preco_total=200
        )

        data_inicio_nova = data_fim_existente + timedelta(hours=1)
        data_fim_nova = data_inicio_nova + timedelta(hours=2)

        reserva = Reserva(
            usuario=self.user,
            campo=self.campo,
            data_inicio=data_inicio_nova,
            data_fim=data_fim_nova,
            preco_total=150
        )

        try:
            reserva.clean()
        except ValidationError:
            self.fail('O método clean() levantou uma exceção de ValidationError inesperadamente.')

class ReservaAdminTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='admin', email='admin@example.com')
        self.client.login(username='admin', password='admin')
        self.campo = Campo.objects.create(nome='Campo Teste', preco_por_hora=50)

    def test_reserva_admin(self):
        # Verifica se o admin está configurado corretamente
        from reservas.admin import ReservaAdmin
        from django.contrib import admin
        admin_site = admin.sites.site
        model_admin = ReservaAdmin(Reserva, admin_site)
        self.assertTrue('data_inicio' in model_admin.list_display)
        self.assertTrue('data_fim' in model_admin.list_display)

class ReservaViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')
        self.campo = Campo.objects.create(nome='Campo Teste', preco_por_hora=100)
        self.client.login(username='user', password='pass')

    def test_reservar_view(self):
        response = self.client.post(reverse('reservas:reservar', args=[self.campo.pk]), {
            'data_inicio': timezone.now() + timedelta(hours=1),
            'data_fim': timezone.now() + timedelta(hours=2),
            'preco_total': 100
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Confirmar Reserva')

    def test_confirmar_reserva_view(self):
        response = self.client.post(reverse('reservas:confirmar_reserva'), {
            'campo_id': self.campo.pk,
            'data_inicio': timezone.now() + timedelta(hours=1),
            'data_fim': timezone.now() + timedelta(hours=2),
            'preco_total': 100
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reserva confirmada com sucesso!')

class ReservaFormTest(TestCase):
    def setUp(self):
        self.campo = Campo.objects.create(nome='Campo Teste', preco_por_hora=100)

    def test_reserva_form_valid(self):
        form_data = {
            'campo': self.campo.pk,
            'data_inicio': timezone.now() + timedelta(hours=1),
            'data_fim': timezone.now() + timedelta(hours=2),
            'preco_total': 100
        }
        form = ReservaForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_reserva_form_invalid(self):
        #'data_fim' antes de 'data_inicio'
        data_inicio = timezone.now() + timedelta(hours=2)
        data_fim = timezone.now() + timedelta(hours=1)  # Data de fim antes da data de início
        
        response = self.client.post('/reservas/reservar/%d/' % self.campo.pk, {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'preco_total': 100
        })
        
        # Verifica se a mensagem de erro está na resposta
        self.assertContains(response, "A data de início deve ser anterior à data de fim")