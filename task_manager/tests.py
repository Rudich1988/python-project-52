from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


from users.models import CustomUser


class IndexViesTestCase(TestCase):

    def test_index_view(self):
        path = reverse('index')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'index.html')