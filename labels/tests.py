from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser
from tasks.models import Task
from labels.models import Label


class LabelsShowTestCase(TestCase):
    fixtures = ['fixtures/labels.json', 'fixtures/users.json']

    def test_labels_show(self):
        user = CustomUser.objects.first()
        self.client.force_login(user)
        labels = Label.objects.all()
        path = reverse('labels:labels_show')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'labels/labels_show.html')
        self.assertEqual(list(response.context_data['labels']), list(labels))


class C(TestCase):
    fixtures = ['fixtures/users.json', 'fixtures/labels.json']

    def setUp(self):
        self.path = reverse('labels:label_create')
        self.user = CustomUser.objects.first()
        self.data = {'name': 'test_label'}

    def test_label_create_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('labels/label_create.html')

    def test_label_create_post(self):
        self.client.force_login(self.user)
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('labels:labels_show'))
        self.assertTrue(Label.objects.filter(name=self.data['name']).exists())
        self.assertRaisesMessage(response, 'Метка успешно создана')


class U(TestCase):
    fixtures = ['fixtures/users.json', 'fixtures/labels.json']

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
        self.assertTemplateUsed('labels/label_update.html')

    def test_label_update_post(self):
        self.client.force_login(self.user)
        response = self.client.post(self.path, self.data)
        self.assertTemplateUsed('labels/label_update.html')
        self.assertTrue(Label.objects.filter(name=self.data['name']).exists())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, '/labels/')
        self.assertRaisesMessage(response, 'Метка успешно изменена')


class D(TestCase):
    fixtures = ['fixtures/users.json', 'fixtures/statuses.json',
                'fixtures/tasks.json', 'fixtures/labels.json']

    def setUp(self):
        self.user = CustomUser.objects.first()
        self.label = Label.objects.first()
        self.path = reverse('labels:label_delete', kwargs={'pk': self.label.id})

    def test_label_delete_success(self):
        self.client.force_login(self.user)
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateUsed('labels/label_delete.html')
        self.assertRedirects(response, reverse('labels:labels_show'))
        self.assertRaisesMessage(response, 'Метка успешно удалена')
        self.assertFalse(Label.objects.filter(id=self.label.id).exists())

    def test_label_delete_error(self):
        task = Task.objects.first()
        task.labels.add(self.label)
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateUsed('labels/label_delete.html')
        self.assertRaisesMessage(response, ('Невозможно удалить метку, '
                                            'потому что она используется'))
        self.assertTrue(Task.objects.filter(id=self.label.id).exists())
