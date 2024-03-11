from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


from statuses.models import Status
from users.models import CustomUser


class StatusShowTestCase(TestCase):
    fixtures = ['statuses.json', 'users.json']

    def test_status_show(self):
        user = CustomUser.objects.first()
        self.client.force_login(user)
        statuses = Status.objects.all()
        path = reverse('statuses:statuses_show')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'statuses/statuses_show.html')
        self.assertEqual(list(response.context_data['statuses']), list(statuses))


class C(TestCase):
    fixtures = ['statuses.json', 'users.json']
    
    def setUp(self):
        self.path = reverse('statuses:status_create')
        self.data = {'name': 'test_status'}
        self.user = CustomUser.objects.first()
    
    def test_status_create_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('statuses/status_create.html')

    def test_status_create_post(self):
        self.client.force_login(self.user)
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('statuses:statuses_show'))
        self.assertTrue(Status.objects.filter(name=self.data['name']).exists())
        self.assertRaisesMessage(response, 'Статус успешно создан')


class U(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        self.user = CustomUser.objects.first()
        self.status = Status.objects.first()
        self.path = reverse('statuses:status_update', kwargs={'pk': self.status.id})
        self.data = {'name': 'try_update'}

    def test_status_update_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('statuses/status_update.html')

    def test_status_update_post(self):
        self.client.force_login(self.user)
        response = self.client.post(self.path, self.data)
        self.assertTemplateUsed('statuses/statuses_update.html')
        self.assertTrue(Status.objects.filter(name=self.data['name']).exists())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('statuses:statuses_show'))
        self.assertRaisesMessage(response, 'Статус успешно изменен')


class D(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        self.user = CustomUser.objects.first()
        self.status = Status.objects.first()
        self.path = reverse('statuses:status_delete', kwargs={'pk': self.status.id})

    def test_status_delete(self):
        self.client.force_login(self.user)
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateUsed('statuses/status_delete.html')
        self.assertFalse(Status.objects.filter(name=self.status.name).exists())
        self.assertRedirects(response, reverse('statuses:statuses_show'))
        self.assertRaisesMessage(response, 'Статус успешно удален')
