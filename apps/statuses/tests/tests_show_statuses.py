from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


from apps.statuses.models import Status
from apps.users.models import CustomUser


class StatusesShowTest(TestCase):
    fixtures = ['task_manager/fixtures/statuses.json',
                'task_manager/fixtures/users.json']

    def test_status_show(self):
        user = CustomUser.objects.first()
        self.client.force_login(user)
        statuses = Status.objects.all()
        path = reverse('statuses:statuses_show')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(list(response.context_data['statuses']),
                         list(statuses))
