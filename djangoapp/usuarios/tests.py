from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from usuarios.forms import UserProfileForm
from usuarios.models import UserProfile
from usuarios.views import index, profile_view
from campos.models import Campo
import time

class UserProfileFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        # Garantir que o perfil é criado automaticamente
        self.profile, created = UserProfile.objects.get_or_create(user=self.user)
        self.profile.phone_number = '1234567890'
        self.profile.save()

    def test_user_profile_form_initial_data(self):
        form = UserProfileForm(user=self.user)
        self.assertEqual(form.fields['username'].initial, self.user.username)
        self.assertEqual(form.fields['email'].initial, self.user.email)

    def test_user_profile_form_valid_data(self):
        form = UserProfileForm({
            'username': 'newusername',
            'email': 'newemail@example.com',
            'phone_number': '1234567890'
        }, user=self.user)
        self.assertTrue(form.is_valid())

    def test_user_profile_form_save(self):
        form = UserProfileForm({
            'username': 'newusername',
            'email': 'newemail@example.com',
            'phone_number': '1234567890'
        }, user=self.user)
        if form.is_valid():
            form.instance = self.profile
            form.save()
            self.user.refresh_from_db()
            self.assertEqual(self.user.username, 'newusername')
            self.assertEqual(self.user.email, 'newemail@example.com')
            profile = UserProfile.objects.get(user=self.user)
            self.assertEqual(profile.phone_number, '1234567890')

    def test_user_profile_form_invalid_data(self):
        form = UserProfileForm({
            'username': '__',  # Nome de usuário inválido
            'email': 'invalidemail@@',  # Email inválido
            'phone_number': '123'  # Número de telefone inválido
        }, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_user_profile_form_empty_data(self):
        form = UserProfileForm({}, user=self.user)
        self.assertFalse(form.is_valid())

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        # Garantir que o perfil é criado automaticamente
        self.profile, created = UserProfile.objects.get_or_create(user=self.user)
        self.profile.phone_number = '1234567890'
        self.profile.save()

    def test_user_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.phone_number, '1234567890')

    def test_user_profile_str_representation(self):
        self.assertEqual(str(self.profile), self.profile.user.username)

    def test_user_profile_update(self):
        self.profile.phone_number = '0987654321'
        self.profile.save()
        updated_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(updated_profile.phone_number, '0987654321')

    def test_user_profile_deletion(self):
        self.profile.delete()
        with self.assertRaises(UserProfile.DoesNotExist):
            UserProfile.objects.get(user=self.user)

class UserProfileSignalsTest(TestCase):
    def setUp(self):
        UserProfile.objects.all().delete()  # Limpar quaisquer perfis existentes

    def test_user_profile_creation_signal(self):
        user = User.objects.create_user(username='testuser28', email='test@example1.com', password='password1')
        # O perfil deve ser criado automaticamente pelo sinal
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_user_profile_save_signal(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        # Verifique se o perfil foi criado automaticamente
        profile = UserProfile.objects.get(user=user)
        profile.phone_number = '0987654321'
        profile.save()
        profile.refresh_from_db()
        self.assertEqual(profile.phone_number, '0987654321')

    def test_user_profile_update_signal(self):
        user = User.objects.create_user(username='testuser29', email='test@example2.com', password='password')
        # Verifique se o perfil foi criado automaticamente
        profile = UserProfile.objects.get(user=user)
        user.username = 'updateduser'
        user.email = 'updatedemail@example.com'
        user.save()
        profile.refresh_from_db()
        self.assertEqual(profile.user.username, 'updateduser')
        self.assertEqual(profile.user.email, 'updatedemail@example.com')

    def test_user_profile_save_signal_no_profile(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        # O perfil deve ser criado automaticamente pelo sinal
        user.username = 'updateduser'
        user.save()
        # Aguarde um momento para garantir que o sinal tenha sido processado
        self.assertTrue(UserProfile.objects.filter(user=user).exists())
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.user.username, 'updateduser')


class UserProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.client.login(username='testuser', password='password')
        self.profile, created = UserProfile.objects.get_or_create(user=self.user)
        self.profile.phone_number = '1234567890'
        self.profile.save()

    def tearDown(self):
        self.client.logout()

    def test_index_view(self):
        Campo.objects.create(nome='Campo de Futebol', cidade='São Paulo', preco_por_hora=100)
        response = self.client.get(reverse('usuarios:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Campo de Futebol')

    def test_profile_view_get(self):
        response = self.client.get(reverse('usuarios:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/profile.html')
        self.assertIsInstance(response.context['form'], UserProfileForm)

    def test_profile_view_post_valid(self):
        response = self.client.post(reverse('usuarios:profile'), {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'phone_number': '1234567890'
        }, follow=True)
        self.assertRedirects(response, reverse('usuarios:profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.user.email, 'newemail@example.com')
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.phone_number, '1234567890')

    def test_profile_view_post_invalid(self):
        response = self.client.post(reverse('usuarios:profile'), {
            'username': '',  # Nome de usuário inválido
            'email': 'invalidemail',  # Email inválido
            'phone_number': '12345'  # Número de telefone inválido
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/profile.html')
        self.assertFalse(response.context['form'].is_valid())

    def test_profile_view_get_anonymous_user(self):
        self.client.logout()
        response = self.client.get(reverse('usuarios:profile'))
        self.assertEqual(response.status_code, 302)

class UserProfileURLTest(SimpleTestCase):
    def test_index_url_resolves(self):
        url = reverse('usuarios:index')
        self.assertEqual(resolve(url).func, index)

    def test_profile_url_resolves(self):
        url = reverse('usuarios:profile')
        self.assertEqual(resolve(url).func, profile_view)
