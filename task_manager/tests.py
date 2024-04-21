from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class IndexViewTest(TestCase):

    def test_index_view(self):
        path = reverse('index')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'index.html')
