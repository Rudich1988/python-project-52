from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from apps.users.models import CustomUser
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
