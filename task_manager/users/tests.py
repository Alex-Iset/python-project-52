from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from task_manager.constants import SUCCESS_MESSAGES, ERROR_MESSAGES


User = get_user_model()


class UsersViewsTestCase(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user = User.objects.get(pk=4)
        self.other_user = User.objects.get(pk=6)
        self.client.login(username=self.user.username, password='123')

    def test_users_list_view(self):
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/list.html')
        self.assertEqual(len(response.context['users']), 2)

    def test_user_create_view_get(self):
        self.client.logout()
        response = self.client.get(reverse('user_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/form.html')

    def test_user_create_view_post(self):
        self.client.logout()
        data = {
            'first_name': 'New',
            'last_name': 'User',
            'username': 'newuser',
            'password1': '123',
            'password2': '123'
        }
        response = self.client.post(reverse('user_create'), data)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_create_view_post_invalid_data(self):
        self.client.logout()
        data = {
            'first_name': 'New',
            'last_name': 'User',
            'username': 'newuser',
            'password1': '123',
            'password2': '456'
        }
        response = self.client.post(reverse('user_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_user_update_view_get_own(self):
        url = reverse('user_update', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/form.html')

    def test_user_update_view_post_own(self):
        url = reverse('user_update', kwargs={'pk': self.user.pk})
        data = {
            'username': 'updated_username',
            'first_name': 'updated_user',
            'last_name': 'updated_name'
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('users_list'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updated_username')
        self.assertEqual(self.user.first_name, 'updated_user')

    def test_user_update_no_permission(self):
        url = reverse('user_update', kwargs={'pk': self.other_user.pk})
        response = self.client.post(url, {})
        self.assertRedirects(response, reverse('users_list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(ERROR_MESSAGES['no_permission_update'] in m.message for m in messages))

    def test_user_delete_view_get_own(self):
        url = reverse('user_delete', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete.html')

    def test_user_delete_view_post_own(self):
        url = reverse('user_delete', kwargs={'pk': self.user.pk})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('users_list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(SUCCESS_MESSAGES['user']['user_deleted'] in m.message for m in messages))
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=self.user.pk)

    def test_user_delete_no_permission(self):
        url = reverse('user_delete', kwargs={'pk': self.other_user.pk})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('users_list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(ERROR_MESSAGES['no_permission_update'], [m.message for m in messages])
        self.assertTrue(User.objects.filter(pk=self.other_user.pk).exists())

    def test_user_login_view_get(self):
        self.client.logout()
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_user_login_view_post_valid(self):
        self.client.logout()
        data = {
            'username': self.user.username,
            'password': '123'
        }
        response = self.client.post(reverse('login'), data)
        self.assertRedirects(response, reverse('homepage'))

    def test_user_login_view_post_invalid(self):
        self.client.logout()
        data = {
            'username': self.user.username,
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_user_logout_view(self):
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('homepage'))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(SUCCESS_MESSAGES['logged_out'], [m.message for m in messages])
