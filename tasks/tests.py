from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse

from statuses.models import Status
from users.models import CustomUser
from tasks.models import Task


class TaskShowTestCase(TestCase):
    fixtures = ['fixtures/users.json', 'fixtures/statuses.json', 'fixtures/tasks.json']

    def test_tasks_show(self):
        user = CustomUser.objects.first()
        self.client.force_login(user)
        tasks = Task.objects.all()
        path = reverse('tasks:tasks_show')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/tasks_show.html')
        self.assertEqual(list(response.context_data['tasks'].qs), list(tasks))


class TaskDetailTestCase(TestCase):
    fixtures = ['fixtures/tasks.json', 'fixtures/users.json', 'fixtures/statuses.json']

    def test_task_detail(self):
        task = Task.objects.first()
        user = CustomUser.objects.first()
        path = reverse('tasks:task_detail', kwargs={'pk': task.id})
        self.client.force_login(user)
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('tasks/task_detail.html')


class C(TestCase):
    fixtures = ['fixtures/users.json', 'fixtures/statuses.json', 'fixtures/tasks.json']

    def setUp(self):
        self.path = reverse('tasks:task_create')
        self.user = CustomUser.objects.first()
        self.status = Status.objects.first()
        self.data = {'name': 'test_task', 'description': 'test',
                     'status': self.status.id,
                     'executor': self.user.id}

    def test_task_create_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('tasks/task_create.html')

    def test_task_create_post(self):
        self.client.force_login(self.user)
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('tasks:tasks_show'))
        self.assertTrue(Task.objects.filter(name=self.data['name']).exists())
        self.assertRaisesMessage(response, 'Задача успешно создана')


class U(TestCase):
    fixtures = ['fixtures/users.json', 'fixtures/tasks.json', 'fixtures/statuses.json']

    def setUp(self):
        self.user = CustomUser.objects.first()
        self.status = Status.objects.first()
        self.task = Task.objects.first()
        self.path = reverse('tasks:task_update', kwargs={'pk': self.task.id})
        self.data = {'name': 'try_task_update',
                     'description': self.task.description,
                     'status': self.status.id, 'executor': self.user.id}

    def test_task_update_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('tasks/task_update.html')

    def test_task_update_post(self):
        self.client.force_login(self.user)
        response = self.client.post(self.path, self.data)
        self.assertTemplateUsed('tasks/task_update.html')
        self.assertTrue(Task.objects.filter(name=self.data['name']).exists())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, '/tasks/')
        self.assertRaisesMessage(response, 'Статус успешно изменен')


class D(TestCase):
    fixtures = ['fixtures/users.json', 'fixtures/statuses.json', 'fixtures/tasks.json']

    def setUp(self):
        self.user = CustomUser.objects.first()
        self.task = Task.objects.filter(author=self.user)[0]
        self.path = reverse('tasks:task_delete', kwargs={'pk': self.task.id})

    def test_task_delete_success(self):
        self.client.force_login(self.user)
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateUsed('tasks/task_delete.html')
        self.assertRedirects(response, reverse('tasks:tasks_show'))
        self.assertRaisesMessage(response, 'Задача успешно удалена')
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_task_delete_error(self):
        another_user = CustomUser.objects.get(username='test1')
        self.client.force_login(another_user)
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateUsed('tasks/task_delete.html')
        self.assertRedirects(response, reverse('tasks:tasks_show'))
        self.assertRaisesMessage(response, ('Задачу может удалить '
                                            'только ее автор'))
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())
