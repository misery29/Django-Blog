from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from .models import Avaliacao
from campos.models import Campo
from reservas.models import Reserva
from .forms import AvaliacaoForm

class AvaliacaoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')
        self.campo = Campo.objects.create(nome='Campo 1', preco_por_hora=100)
        self.avaliacao = Avaliacao.objects.create(
            campo=self.campo,
            usuario=self.user,
            estrelas=4,
            comentario='Boa experiência',
        )

    def test_avaliacao_str(self):
        self.assertEqual(str(self.avaliacao), f'Avaliação de {self.user} para {self.campo}')

    def test_unique_together_constraint(self):
        with self.assertRaises(Exception):
            Avaliacao.objects.create(
                campo=self.campo,
                usuario=self.user,
                estrelas=5,
                comentario='Outra avaliação'
            )

class AvaliacaoAdminTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='admin', email='admin@example.com')
        self.client.login(username='admin', password='admin')
        self.campo = Campo.objects.create(nome='Campo Teste', preco_por_hora=50)
        self.avaliacao = Avaliacao.objects.create(
            campo=self.campo,
            usuario=self.user,
            estrelas=4,
            comentario='Boa experiência'
        )

    def test_avaliacao_admin(self):
        from avaliacoes.admin import AvaliacaoAdmin
        from django.contrib import admin
        admin_site = admin.sites.site
        model_admin = AvaliacaoAdmin(Avaliacao, admin_site)
        self.assertTrue('campo' in model_admin.list_display)
        self.assertTrue('usuario' in model_admin.list_display)
        self.assertTrue('estrelas' in model_admin.list_display)
        self.assertTrue('comentario' in model_admin.list_display)
        self.assertTrue('data_criacao' in model_admin.list_display)
        self.assertTrue('is_active' in model_admin.list_display)

class AvaliacaoViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')
        self.campo = Campo.objects.create(nome='Campo Teste', preco_por_hora=100)
        self.reserva = Reserva.objects.create(
            usuario=self.user,
            campo=self.campo,
            data_inicio=timezone.now() - timezone.timedelta(days=2),
            data_fim=timezone.now() - timezone.timedelta(days=1),
            preco_total=100,
            is_active=True
        )
        self.client.login(username='user', password='pass')

    def test_adicionar_avaliacao_view(self):
        response = self.client.get(reverse('avaliacoes:adicionar_avaliacao', args=[self.campo.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adicionar_avaliacao.html')

    def test_adicionar_avaliacao_post(self):
        data = {
            'estrelas': 5,
            'comentario': 'Ótima experiência!'
        }
        response = self.client.post(reverse('avaliacoes:adicionar_avaliacao', args=[self.campo.pk]), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('campos:detail_fields', args=[self.campo.pk]))
        self.assertTrue(Avaliacao.objects.filter(campo=self.campo, usuario=self.user, estrelas=5).exists())

    def test_adicionar_avaliacao_sem_reserva(self):
        # Remover a reserva ativa para testar o caso sem reserva
        self.reserva.is_active = False
        self.reserva.save()
        response = self.client.get(reverse('avaliacoes:adicionar_avaliacao', args=[self.campo.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('campos:detail_fields', args=[self.campo.pk]))

class AvaliacaoFormTest(TestCase):
    def setUp(self):
        self.campo = Campo.objects.create(nome='Campo Teste', preco_por_hora=100)

    def test_avaliacao_form_valid(self):
        form_data = {
            'campo': self.campo.pk,
            'estrelas': 4,
            'comentario': 'Boa avaliação',
        }
        form = AvaliacaoForm(data=form_data)
        self.assertTrue(form.is_valid())

