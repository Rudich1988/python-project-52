from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from apps.users.models import CustomUser
from apps.tasks.models import Task
from apps.labels.models import Label


class LabelsShowTest(TestCase):
    fixtures = ['apps/labels/tests/fixtures/labels.json',
                'task_manager/fixtures/users.json']

    def test_labels_show(self):
        user = CustomUser.objects.first()
        self.client.force_login(user)
        labels = Label.objects.all()
        path = reverse('labels:labels_show')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(list(response.context_data['labels']), list(labels))


class C(TestCase):
    fixtures = ['task_manager/fixtures/users.json',
                'apps/labels/tests/fixtures/labels.json']

    def setUp(self):
        self.path = reverse('labels:label_create')
        self.user = CustomUser.objects.first()
        self.data = {'name': 'test_label'}

    def test_label_create_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_label_create_post(self):
        self.client.force_login(self.user)
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('labels:labels_show'))
        self.assertTrue(Label.objects.filter(name=self.data['name']).exists())
        self.assertRaisesMessage(response, 'Метка успешно создана')


class U(TestCase):
    fixtures = ['task_manager/fixtures/users.json',
                'apps/labels/tests/fixtures/labels.json']

    def setUp(self):
        self.user = CustomUser.objects.first()
        self.label = Label.objects.first()
        self.task = Task.objects.first()
        self.path = reverse('labels:label_update', kwargs={'pk': self.label.id})
        self.data = {'name': 'try_label_update'}

    def test_label_update_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_label_update_post(self):
        self.client.force_login(self.user)
        response = self.client.post(self.path, self.data)
        self.assertTrue(Label.objects.filter(name=self.data['name']).exists())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, '/labels/')
        self.assertRaisesMessage(response, 'Метка успешно изменена')


class D(TestCase):
    fixtures = ['task_manager/fixtures/users.json',
                'task_manager/fixtures/statuses.json',
                'task_manager/fixtures/tasks.json',
                'apps/labels/tests/fixtures/labels.json']

    def setUp(self):
        self.user = CustomUser.objects.first()
        self.label = Label.objects.first()
        self.path = reverse('labels:label_delete', kwargs={'pk': self.label.id})

    def test_label_delete_success(self):
        self.client.force_login(self.user)
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('labels:labels_show'))
        self.assertRaisesMessage(response, 'Метка успешно удалена')
        self.assertFalse(Label.objects.filter(id=self.label.id).exists())

    def test_label_delete_error(self):
        task = Task.objects.first()
        task.labels.add(self.label)
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRaisesMessage(response, ('Невозможно удалить метку, '
                                            'потому что она используется'))
        self.assertTrue(Task.objects.filter(id=self.label.id).exists())
