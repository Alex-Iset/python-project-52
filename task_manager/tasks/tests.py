from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages

from task_manager.users.models import User
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.constants import SUCCESS_MESSAGES, ERROR_MESSAGES


class TaskViewsTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.get(pk=1)
        cls.user2 = User.objects.get(pk=2)
        cls.status = Status.objects.get(pk=1)
        cls.label = Label.objects.get(pk=1)
        cls.task_data = {
            'name': 'Задача',
            'description': 'Описание',
            'status': cls.status.id,
            'executor': cls.user2.id,
            'labels': [cls.label.id],
        }

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user1)

    def test_task_list_view(self):
        response = self.client.get(reverse('tasks_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/list.html')
        self.assertContains(response, 'Задача 1')

    def test_task_detail_view(self):
        task = Task.objects.get(pk=1)
        response = self.client.get(reverse('task_detail', args=[task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/detail.html')
        self.assertContains(response, task.name)

    def test_task_create_view_get(self):
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/form.html')
        self.assertContains(response, 'Создать задачу')

    def test_task_create_view_post(self):
        response = self.client.post(
            reverse('task_create'),
            data=self.task_data,
            follow=True
        )
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertEqual(Task.objects.count(), 2)
        new_task = Task.objects.last()
        self.assertEqual(new_task.name, 'Задача')
        self.assertEqual(new_task.author, self.user1)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(SUCCESS_MESSAGES['task']['task_created'], str(messages[0]))

    def test_task_update_view_get(self):
        task = Task.objects.get(pk=1)
        response = self.client.get(reverse('task_update', args=[task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/form.html')
        self.assertContains(response, 'Изменение задачи')

    def test_task_update_view_post(self):
        task = Task.objects.get(pk=1)
        updated_data = self.task_data
        updated_data['name'] = 'Измененная задача'

        response = self.client.post(
            reverse('task_update', args=[task.pk]),
            data=updated_data,
            follow=True
        )
        self.assertRedirects(response, reverse('tasks_list'))
        task.refresh_from_db()
        self.assertEqual(task.name, 'Измененная задача')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(SUCCESS_MESSAGES['task']['task_updated'], str(messages[0]))

    def test_task_delete_view_get(self):
        task = Task.objects.get(pk=1)
        response = self.client.get(reverse('task_delete', args=[task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/delete.html')

    def test_task_delete_view_post(self):
        task = Task.objects.get(pk=1)
        response = self.client.post(
            reverse('task_delete', args=[task.pk]),
            follow=True
        )
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertEqual(Task.objects.count(), 0)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(SUCCESS_MESSAGES['task']['task_deleted'], str(messages[0]))

    def test_task_delete_by_non_author(self):
        self.client.force_login(self.user2)
        task = Task.objects.get(pk=1)

        response = self.client.get(reverse('task_delete', args=[task.pk]))
        self.assertRedirects(response, reverse('tasks_list'))

        response = self.client.post(
            reverse('task_delete', args=[task.pk]),
            follow=True
        )
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertEqual(Task.objects.count(), 1)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(ERROR_MESSAGES['only_author_can_delete'], str(messages[0]))
