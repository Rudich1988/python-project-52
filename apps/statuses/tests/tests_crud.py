from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


from apps.statuses.models import Status
from apps.users.models import CustomUser
from apps.tasks.models import Task


class StatusCreateTest(TestCase):
    fixtures = ['task_manager/fixtures/statuses.json',
                'task_manager/fixtures/users.json']

    def setUp(self):
        self.path = reverse('statuses:status_create')
        self.data = {'name': 'test_status'}
        self.user = CustomUser.objects.first()

    def test_status_create_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_status_create_post(self):
        self.client.force_login(self.user)
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('statuses:statuses_show'))
        self.assertTrue(Status.objects.filter(name=self.data['name']).exists())
        self.assertRaisesMessage(response, 'Статус успешно создан')


class StatusUpdateTest(TestCase):
    fixtures = ['task_manager/fixtures/users.json',
                'task_manager/fixtures/statuses.json']

    def setUp(self):
        self.user = CustomUser.objects.first()
        self.status = Status.objects.first()
        self.path = reverse('statuses:status_update',
                            kwargs={'pk': self.status.id})
        self.data = {'name': 'try_update'}

    def test_status_update_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_status_update_post(self):
        self.client.force_login(self.user)
        response = self.client.post(self.path, self.data)
        self.assertTrue(Status.objects.filter(name=self.data['name']).exists())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('statuses:statuses_show'))
        self.assertRaisesMessage(response, 'Статус успешно изменен')


class StatusDeleteTest(TestCase):
    fixtures = ['task_manager/fixtures/users.json',
                'task_manager/fixtures/statuses.json',
                'task_manager/fixtures/tasks.json']

    def setUp(self):
        self.user = CustomUser.objects.first()
        self.status = Status.objects.first()
        self.path = reverse('statuses:status_delete',
                            kwargs={'pk': self.status.id})

    def test_status_delete(self):
        self.client.force_login(self.user)
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('statuses:statuses_show'))
        self.assertRaisesMessage(response, 'Статус успешно удален')

    def test_status_delete_error(self):
        self.client.force_login(self.user)
        task = Task.objects.first()
        self.status.tasks_status.add(task)
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(Status.objects.filter(name=self.status.name).exists())
        self.assertRedirects(response, reverse('statuses:statuses_show'))
        self.assertRaisesMessage(response, ('Невозможно удалить статус, '
                                            'потому что он используется'))
