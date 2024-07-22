from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

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
        # Verifica se o usuário autenticado é redirecionado para a homepage
        self.assertRedirects(response, '/')

    def test_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)  # Checa se a visualização de login está funcionando

    def test_logout_view(self):
        self.client.login(username='testuser', password='securepassword')
        response = self.client.get(reverse('account_logout'))
        self.assertEqual(response.status_code, 200)  # Checa se a visualização de login está funcionando

    def test_password_reset_request(self):
        response = self.client.post(self.password_reset_url, {'email': 'testuser@example.com'})
        self.assertRedirects(response, reverse('account_reset_password_done'))  # Redireciona após a solicitação

    def test_password_reset_done_view(self):
        # Supondo que a mensagem de confirmação seja exibida após um reset de senha
        response = self.client.get(self.password_reset_done_url)
        self.assertContains(response, 'We have sent you an email. If you have not received it please check your spam folder. Otherwise contact us if you do not receive it in a few minutes.')

    def test_registration_view(self):
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 200)