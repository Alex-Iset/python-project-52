from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages

from task_manager.users.models import User
from task_manager.constants import SUCCESS_MESSAGES, ERROR_MESSAGES


BASE_FORM = 'base_create_update_form.html'


class UsersViewsTestCase(TestCase):
    fixtures = ['users.json', 'tasks.json', 'labels.json', 'statuses.json']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.other_user = User.objects.get(pk=2)
        cls.new_user_data = {
            'first_name': 'Новое имя',
            'last_name': 'Новая фамилия',
            'username': 'newuser',
            'password1': '123', # NOSONAR
            'password2': '123' # NOSONAR
        }

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)

    def create_new_user(self):
        return User.objects.create_user(
            first_name=self.new_user_data['first_name'],
            last_name=self.new_user_data['last_name'],
            username=self.new_user_data['username'],
            password=self.new_user_data['password1']
        )

    def test_users_list_view(self):
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/list.html')
        self.assertEqual(len(response.context['users']), 2)

    def test_user_create_view_get(self):
        self.client.logout()
        response = self.client.get(reverse('user_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, BASE_FORM)

    def test_user_create_view_post(self):
        self.client.logout()
        response = self.client.post(
            reverse('user_create'),
            data=self.new_user_data,
            follow=True
        )
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(User.objects.count(), 3)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(SUCCESS_MESSAGES['user']['user_created'], str(messages[0]))

    def test_user_update_view_get_own(self):
        url = reverse('user_update', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, BASE_FORM)

    def test_user_update_view_post_own(self):
        updated_data = {
            'first_name': 'Измененное имя',
            'last_name': 'Измененная фамилия',
            'username': 'updated_username',
            'password1': '123',  # NOSONAR
            'password2': '123'  # NOSONAR
        }
        url = reverse('user_update', kwargs={'pk': self.user.pk})
        response = self.client.post(url, data=updated_data, follow=True)
        self.assertRedirects(response, reverse('users_list'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updated_username')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(SUCCESS_MESSAGES['user']['user_updated'], str(messages[0]))

    def test_user_update_no_permission(self):
        url = reverse('user_update', kwargs={'pk': self.user.pk})
        self.client.logout()
        other_user = self.create_new_user()
        self.client.force_login(other_user)
        response = self.client.post(url, data=self.new_user_data, follow=True)
        self.assertRedirects(response, reverse('users_list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(ERROR_MESSAGES['no_permission_update'], str(messages[0]))

    def test_user_delete_view_get_own(self):
        url = reverse('user_delete', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete.html')

    def test_user_delete_view_post_own(self):
        new_user = self.create_new_user()
        self.client.force_login(new_user)
        url = reverse('user_delete', kwargs={'pk': new_user.pk})
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, reverse('users_list'))
        self.assertFalse(User.objects.filter(pk=new_user.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(SUCCESS_MESSAGES['user']['user_deleted'], str(messages[0]))

    def test_user_delete_with_tasks(self):
        url = reverse('user_delete', kwargs={'pk': self.user.pk})
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, reverse('users_list'))
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(ERROR_MESSAGES['user_has_tasks'], str(messages[0]))

    def test_user_cannot_delete_other_user(self):
        other_user = self.other_user
        url = reverse('user_delete', kwargs={'pk': other_user.pk})
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, reverse('users_list'))
        self.assertTrue(User.objects.filter(pk=other_user.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(ERROR_MESSAGES['no_permission_update'], str(messages[0]))

    def test_user_login_view_get(self):
        self.client.logout()
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/auth/login.html')

    def test_user_login_view_post_valid(self):
        self.client.logout()
        new_user = self.create_new_user()
        data = {
            'username': new_user.username,
            'password': self.new_user_data['password1']
        }
        response = self.client.post(reverse('login'), data, follow=True)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, reverse('homepage'))

    def test_user_login_view_post_invalid(self):
        self.client.logout()
        data = {
            'username': self.user.username,
            'password': '456' # NOSONAR
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_user_logout_view(self):
        response = self.client.post(reverse('logout'), follow=True)
        self.assertRedirects(response, reverse('homepage'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(SUCCESS_MESSAGES['logged_out'], str(messages[0]))
