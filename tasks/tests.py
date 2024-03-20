from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


from statuses.models import Status
from users.models import CustomUser
from tasks.models import Task


class TaskShowTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json']

