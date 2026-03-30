from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse

from accounts.validators import LetterAndNumberValidator

User = get_user_model()


class UserModelTests(TestCase):
    def test_create_user_with_email(self):
        user = User.objects.create_user(email='test@empresa.com', password='Teste123')
        self.assertEqual(user.email, 'test@empresa.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.role, User.ROLE_MEMBER)

    def test_create_user_without_email_raises(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='Teste123')

    def test_create_superuser(self):
        user = User.objects.create_superuser(email='admin@empresa.com', password='Admin123')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.role, User.ROLE_ADMIN)

    def test_email_is_unique(self):
        User.objects.create_user(email='dup@empresa.com', password='Teste123')
        with self.assertRaises(Exception):
            User.objects.create_user(email='dup@empresa.com', password='Teste456')

    def test_default_role_is_member(self):
        user = User.objects.create_user(email='m@empresa.com', password='Teste123')
        self.assertEqual(user.role, User.ROLE_MEMBER)
        self.assertTrue(user.is_member)

    def test_role_properties(self):
        admin = User.objects.create_user(email='a@e.com', password='Teste123', role=User.ROLE_ADMIN)
        manager = User.objects.create_user(email='g@e.com', password='Teste123', role=User.ROLE_MANAGER)
        member = User.objects.create_user(email='m@e.com', password='Teste123', role=User.ROLE_MEMBER)
        self.assertTrue(admin.is_admin)
        self.assertTrue(manager.is_manager)
        self.assertTrue(member.is_member)

    def test_str_returns_email(self):
        user = User.objects.create_user(email='str@e.com', password='Teste123')
        self.assertEqual(str(user), 'str@e.com')


class PasswordValidatorTests(TestCase):
    def setUp(self):
        self.validator = LetterAndNumberValidator()

    def test_valid_password(self):
        self.validator.validate('MinhaSenh4')

    def test_password_without_number(self):
        with self.assertRaises(ValidationError):
            self.validator.validate('SenhaApenas')

    def test_password_without_letter(self):
        with self.assertRaises(ValidationError):
            self.validator.validate('12345678')


class LoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='login@empresa.com', password='Teste123', first_name='Test'
        )
        self.login_url = reverse('accounts:login')

    def test_login_page_renders(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_login_valid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'login@empresa.com',
            'password': 'Teste123',
        })
        self.assertEqual(response.status_code, 302)

    def test_login_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'login@empresa.com',
            'password': 'errada',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Credenciais inválidas')

    def test_login_nonexistent_email(self):
        response = self.client.post(self.login_url, {
            'username': 'naoexiste@empresa.com',
            'password': 'Teste123',
        })
        self.assertContains(response, 'Credenciais inválidas')

    def test_login_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(self.login_url, {
            'username': 'login@empresa.com',
            'password': 'Teste123',
        })
        self.assertContains(response, 'Conta desativada')

    def test_logout(self):
        self.client.login(email='login@empresa.com', password='Teste123')
        response = self.client.post(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)


class AdminUserManagementTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            email='admin@empresa.com', password='Admin123', role=User.ROLE_ADMIN
        )
        self.member = User.objects.create_user(
            email='membro@empresa.com', password='Membro123', role=User.ROLE_MEMBER
        )
        self.client.login(email='admin@empresa.com', password='Admin123')

    def test_admin_can_list_users(self):
        response = self.client.get(reverse('accounts:user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'admin@empresa.com')

    def test_member_cannot_list_users(self):
        self.client.login(email='membro@empresa.com', password='Membro123')
        response = self.client.get(reverse('accounts:user_list'))
        self.assertEqual(response.status_code, 403)

    def test_admin_can_create_user(self):
        response = self.client.post(reverse('accounts:user_create'), {
            'email': 'novo@empresa.com',
            'first_name': 'Novo',
            'last_name': 'Usuario',
            'role': User.ROLE_MEMBER,
            'password': 'Novo1234',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='novo@empresa.com').exists())

    def test_admin_can_edit_user(self):
        response = self.client.post(
            reverse('accounts:user_edit', args=[self.member.pk]),
            {
                'email': 'membro@empresa.com',
                'first_name': 'Atualizado',
                'last_name': 'Nome',
                'role': User.ROLE_MANAGER,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.member.refresh_from_db()
        self.assertEqual(self.member.role, User.ROLE_MANAGER)

    def test_admin_can_deactivate_user(self):
        response = self.client.post(
            reverse('accounts:user_toggle_active', args=[self.member.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.member.refresh_from_db()
        self.assertFalse(self.member.is_active)

    def test_admin_can_reactivate_user(self):
        self.member.is_active = False
        self.member.save()
        response = self.client.post(
            reverse('accounts:user_toggle_active', args=[self.member.pk])
        )
        self.member.refresh_from_db()
        self.assertTrue(self.member.is_active)

    def test_cannot_deactivate_last_admin(self):
        response = self.client.post(
            reverse('accounts:user_toggle_active', args=[self.admin.pk])
        )
        self.admin.refresh_from_db()
        self.assertTrue(self.admin.is_active)

    def test_admin_can_reset_password(self):
        response = self.client.post(
            reverse('accounts:user_reset_password', args=[self.member.pk]),
            {'password': 'NovaSenha1'},
        )
        self.assertEqual(response.status_code, 302)
        self.member.refresh_from_db()
        self.assertTrue(self.member.check_password('NovaSenha1'))

    def test_unauthenticated_redirects_to_login(self):
        self.client.logout()
        response = self.client.get(reverse('accounts:user_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)
