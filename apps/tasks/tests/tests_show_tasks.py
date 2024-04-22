from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse

from apps.users.models import CustomUser
from apps.tasks.models import Task


class TasksShowTest(TestCase):
    fixtures = ['task_manager/fixtures/users.json',
                'task_manager/fixtures/statuses.json',
                'task_manager/fixtures/tasks.json']

    def test_tasks_show(self):
        user = CustomUser.objects.first()
        self.client.force_login(user)
        tasks = Task.objects.all()
        path = reverse('tasks:tasks_show')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(list(response.context_data['tasks'].qs), list(tasks))


class TaskDetailTest(TestCase):
    fixtures = ['task_manager/fixtures/tasks.json',
                'task_manager/fixtures/users.json',
                'task_manager/fixtures/statuses.json']

    def test_task_detail(self):
        task = Task.objects.first()
        user = CustomUser.objects.first()
        path = reverse('tasks:task_detail', kwargs={'pk': task.id})
        self.client.force_login(user)
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
