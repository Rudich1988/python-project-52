from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


from apps.users.models import CustomUser


class UsersShowTest(TestCase):
    fixtures = ['task_manager/fixtures/users.json']

    def test_list(self):
        users = CustomUser.objects.all()
        path = reverse('users:users_show')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(list(response.context_data['object_list']),
                         list(users))
