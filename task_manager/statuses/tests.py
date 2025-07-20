from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages

from task_manager.users.models import User
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.constants import SUCCESS_MESSAGES, ERROR_MESSAGES


BASE_FORM = 'base_create_update_form.html'


class StatusTest(TestCase):
    fixtures = ['users.json', 'labels.json', 'statuses.json']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.status = Status.objects.get(pk=1)
        cls.new_status_data = {'name': 'Статус'}

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)

    def test_status_list_view(self):
        response = self.client.get(reverse('statuses_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/list.html')
        self.assertContains(response, 'В работе')

    def test_status_create_view_get(self):
        response = self.client.get(reverse('status_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, BASE_FORM)
        self.assertContains(response, 'Создать статус')

    def test_status_create_view_post(self):
        response = self.client.post(
            reverse('status_create'),
            data=self.new_status_data,
            follow=True
        )
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertEqual(Status.objects.count(), 2)
        self.assertTrue(Status.objects.filter(name='Статус').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(SUCCESS_MESSAGES['status']['status_created'], str(messages[0]))

    def test_status_update_view_get(self):
        response = self.client.get(reverse('status_update', args=[self.status.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, BASE_FORM)
        self.assertContains(response, 'Изменение статуса')

    def test_status_update_view_post(self):
        updated_data = {'name': 'Измененный статус'}
        response = self.client.post(
            reverse('status_update', args=[self.status.pk]),
            data=updated_data,
            follow=True
        )
        self.assertRedirects(response, reverse('statuses_list'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Измененный статус')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(SUCCESS_MESSAGES['status']['status_updated'], str(messages[0]))

    def test_status_delete_view_get(self):
        response = self.client.get(reverse('status_delete', args=[self.status.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/delete.html')

    def test_status_delete_view_post(self):
        response = self.client.post(
            reverse('status_delete', args=[self.status.pk]),
            follow=True
        )
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertEqual(Status.objects.count(), 0)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(SUCCESS_MESSAGES['status']['status_deleted'], str(messages[0]))

    def test_status_delete_used_status(self):
        Task.objects.create(
            name='Задача',
            description='Описание',
            author=self.user,
            executor=self.user,
            status_id=self.status.id,
        )

        response = self.client.post(
            reverse('status_delete', args=[self.status.pk]),
            follow=True
        )
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertEqual(Status.objects.count(), 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(ERROR_MESSAGES['status_using'], str(messages[0]))
