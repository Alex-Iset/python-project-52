from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages

from task_manager.users.models import User
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from task_manager.constants import SUCCESS_MESSAGES, ERROR_MESSAGES


class LabelTest(TestCase):
    fixtures = ['users.json', 'labels.json', 'statuses.json']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.label = Label.objects.get(pk=1)
        cls.new_label_data = {'name': 'Метка'}

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)

    def test_label_list_view(self):
        response = self.client.get(reverse('labels_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/list.html')
        self.assertContains(response, 'Работа')

    def test_label_create_view_get(self):
        response = self.client.get(reverse('label_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/form.html')
        self.assertContains(response, 'Создать метку')

    def test_label_create_view_post(self):
        response = self.client.post(
            reverse('label_create'),
            data=self.new_label_data,
            follow=True
        )
        self.assertRedirects(response, reverse('labels_list'))
        self.assertEqual(Label.objects.count(), 2)
        self.assertTrue(Label.objects.filter(name='Метка').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(SUCCESS_MESSAGES['label']['label_created'], str(messages[0]))

    def test_label_update_view_get(self):
        response = self.client.get(reverse('label_update', args=[self.label.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/form.html')
        self.assertContains(response, 'Изменение метки')

    def test_label_update_view_post(self):
        updated_data = {'name': 'Измененная метка'}
        response = self.client.post(
            reverse('label_update', args=[self.label.pk]),
            data=updated_data,
            follow=True
        )
        self.assertRedirects(response, reverse('labels_list'))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Измененная метка')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(SUCCESS_MESSAGES['label']['label_updated'], str(messages[0]))

    def test_label_delete_view_get(self):
        response = self.client.get(reverse('label_delete', args=[self.label.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/delete.html')

    def test_label_delete_view_post(self):
        response = self.client.post(
            reverse('label_delete', args=[self.label.pk]),
            follow=True
        )
        self.assertRedirects(response, reverse('labels_list'))
        self.assertEqual(Label.objects.count(), 0)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(SUCCESS_MESSAGES['label']['label_deleted'], str(messages[0]))

    def test_label_delete_used_label(self):
        Task.objects.create(
            name='Задача',
            description='Описание',
            author=self.user,
            executor=self.user,
            status_id=1,
        ).labels.add(self.label)

        response = self.client.post(
            reverse('label_delete', args=[self.label.pk]),
            follow=True
        )
        self.assertRedirects(response, reverse('labels_list'))
        self.assertEqual(Label.objects.count(), 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(ERROR_MESSAGES['label_using'], str(messages[0]))
