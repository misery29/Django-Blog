from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from usuarios.views import profile_view

class AuthenticationTests(TestCase):
    def setUp(self):
        self.login_url = reverse('account_login')
        self.profile_url = reverse('usuarios:profile')
        self.logout_url = reverse('account_logout')
        self.password_reset_url = reverse('account_reset_password')
        self.password_reset_done_url = reverse('account_reset_password_done')
        self.registration_url = reverse('account_signup')

        self.user = get_user_model().objects.create_user(
            username='testuser', email='testuser@example.com', password='securepassword'
        )

    def test_login_redirects_authenticated_user(self):
        self.client.login(username='testuser', password='securepassword')
        response = self.client.get(self.login_url)
        self.assertRedirects(response, '/')

    def test_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        self.client.login(username='testuser', password='securepassword')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 200)

    def test_password_reset_request(self):
        response = self.client.post(self.password_reset_url, {'email': 'testuser@example.com'})
        self.assertRedirects(response, self.password_reset_done_url)

    def test_password_reset_done_view(self):
        response = self.client.get(self.password_reset_done_url)
        self.assertContains(response, 'Acabamos de enviar um e-mail com as instruções. Caso não o receba nos próximos minutos, verifique sua pasta de spam ou entre em contato conosco.')

    def test_registration_view(self):
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 200)

    def test_registration_post_creates_user(self):
        response = self.client.post(self.registration_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newsecurepassword',
            'password2': 'newsecurepassword',
        })
        self.assertEqual(response.status_code, 302)  # Redireciona após registro bem-sucedido
        self.assertTrue(get_user_model().objects.filter(username='newuser').exists())

    def test_profile_view_requires_login(self):
        response = self.client.get(self.profile_url)
        self.assertRedirects(response, f'{self.login_url}?next={self.profile_url}')

    def test_profile_view_logged_in(self):
        self.client.login(username='testuser', password='securepassword')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/profile.html')

    def test_password_reset_email_sent(self):
        response = self.client.post(self.password_reset_url, {'email': 'testuser@example.com'})
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('E-mail de Redefinição de Senha', mail.outbox[0].subject)

    def test_password_reset_confirm(self):
        token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        url = reverse('account_reset_password_from_key', kwargs={'uidb36': uid, 'key': token})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/password_reset_from_key.html')

    def test_url_resolves_to_profile_view(self):
        view = resolve('/profile/')
        self.assertEqual(view.func.__name__, profile_view.__name__)
