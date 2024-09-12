from django.test import TestCase
from django.urls import reverse
from django.contrib.admin.sites import AdminSite
from .admin import CampoAdmin
from .models import Campo
from reservas.models import Reserva
from django.contrib.auth import get_user_model
from django.utils import timezone
from campos.views import geocode_address
from django import forms

User = get_user_model()


class CampoAdminTests(TestCase):
    
    def setUp(self):
        self.site = AdminSite()
        self.campo = Campo.objects.create(
            nome="Campo Teste",
            cidade="Maricá",
            endereco="Rua Teste",
            dimensao="50x50",
            preco_por_hora=100.00,
            tipo_gramado="natural",
            iluminacao_noturna=True,
            vestiarios=True
        )
        self.usuario = User.objects.create_user(
            username='usuario_teste', 
            password='12345'
        )
        self.reserva = Reserva.objects.create(
            usuario=self.usuario,
            campo=self.campo,
            data_inicio=timezone.now(),
            data_fim=timezone.now() + timezone.timedelta(hours=2),
            preco_total=200.00
        )

    def test_exportar_campos_csv(self):
        request = self.client.get(reverse('admin:campos_campo_changelist'))  # Alterado para garantir uma requisição válida
        campo_admin = CampoAdmin(Campo, self.site)
        queryset = Campo.objects.all()
        response = campo_admin.exportar_campos_csv(request, queryset)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Campo Teste', str(response.content))

    def test_exportar_campos_pdf(self):
        request = self.client.get(reverse('admin:campos_campo_changelist'))  # Alterado para garantir uma requisição válida
        campo_admin = CampoAdmin(Campo, self.site)
        queryset = Campo.objects.all()
        response = campo_admin.exportar_campos_pdf(request, queryset)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
class GeocodeTests(TestCase):

    def setUp(self):
        self.campo = Campo.objects.create(
            nome="Campo Geocode",
            cidade="Maricá",
            endereco="Rua Qualquer",
            dimensao="30x50",
            preco_por_hora=150.00,
            tipo_gramado="sintetico",
            iluminacao_noturna=True,
            vestiarios=True
        )

    def test_geocode_address_success(self):
        lat, lon = geocode_address("Maricá", "Rua Abreu Sodré")
        self.assertIsNotNone(lat)
        self.assertIsNotNone(lon)

    def test_geocode_address_fail(self):
        # Teste para uma situação onde a geocodificação falha
        lat, lon = geocode_address("Cidade Inexistente", "Rua Inexistente")
        self.assertIsNone(lat)
        self.assertIsNone(lon)

class CampoDetailViewTests(TestCase):

    def setUp(self):
        self.campo = Campo.objects.create(
            nome="Campo Detalhe",
            cidade="Maricá",
            endereco="Av. Roberto Silveira",
            dimensao="60x40",
            preco_por_hora=120.00,
            tipo_gramado="natural",
            iluminacao_noturna=False,
            vestiarios=True
        )
        self.usuario = User.objects.create_user(username='user1', password='12345')

    def test_geocode_on_detail_view(self):
        self.client.login(username='user1', password='12345')
        url = reverse('campos:detail_fields', args=[self.campo.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.campo.refresh_from_db()
        self.assertIsNotNone(self.campo.latitude)
        self.assertIsNotNone(self.campo.longitude)

    def test_field_detail_view_no_geocode(self):
        # Cria um campo sem coordenadas para garantir que o geocode seja aplicado
        campo = Campo.objects.create(
            nome="Campo Sem Geocode",
            cidade="Maricá",
            endereco="Rua Sem Geocode",
            dimensao="40x40",
            preco_por_hora=100.00,
            tipo_gramado="natural",
            iluminacao_noturna=False,
            vestiarios=True
        )
        self.client.login(username='user1', password='12345')
        url = reverse('campos:detail_fields', args=[campo.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        campo.refresh_from_db()
        self.assertIsNotNone(campo.latitude)
        self.assertIsNotNone(campo.longitude)

    def test_field_detail_view_without_login(self):
        url = reverse('campos:detail_fields', args=[self.campo.pk])
        response = self.client.get(url)
        self.assertRedirects(response, f'/accounts/login/?next={url}')
