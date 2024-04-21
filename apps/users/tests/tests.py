from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


from apps.users.models import CustomUser
from apps.tasks.models import Task


class UsersShowTest(TestCase):
    fixtures = ['task_manager/fixtures/users.json']

    def test_list(self):
        users = CustomUser.objects.all()
        path = reverse('users:users_show')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(list(response.context_data['object_list']),
                         list(users))


class C(TestCase):

    def setUp(self):
        self.path = reverse('users:create_user')
        self.data = {'first_name': 'Igor', 'last_name': 'Rudich',
                     'username': 'barber_itishnik',
                     'password1': 'ya_tester',
                     'password2': 'ya_tester'}

    def test_user_registration_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_registration_post_success(self):
        response = self.client.post(self.path, self.data)
        username = self.data['username']
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(CustomUser.objects.filter(username=username).exists())
        self.assertRaisesMessage(response, ('Пользователь '
                                            'успешно зарегестрирован'))

    def test_user_registration_post_error(self):
        CustomUser.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, ('Пользователь с таким '
                                       'именем уже существует.'))


class U(TestCase):
    fixtures = ['task_manager/fixtures/users.json']

    def setUp(self):
        self.user = CustomUser.objects.get(username='test1')
        self.path = reverse('users:user_update', kwargs={'pk': self.user.id})
        self.data = {'username': 'test1_correct',
                     'password1': self.user.password,
                     'password2': self.user.password,
                     'first_name': self.user.first_name,
                     'last_name': self.user.last_name}

    def test_user_update_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_user_update_post_error_not_login(self):
        response = self.client.post(self.path, self.data)
        self.assertRedirects(response, '/login/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRaisesMessage(response, ('Вы не авторизованы! '
                                            'Пожалуйста, выполните вход.'))
        self.assertFalse(CustomUser.objects.filter(username=self.data['username']).exists())

    def test_user_update_post_success(self):
        self.client.force_login(self.user)
        response = self.client.post(self.path, self.data)
        self.assertTrue(CustomUser.objects.filter(username=self.data['username']).exists())
        self.assertFalse(CustomUser.objects.filter(username=self.user.username).exists())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, '/users/')
        self.assertRaisesMessage(response, 'Пользователь успешно изменен')

    def test_user_update_post_error_another_user(self):
        self.client.force_login(self.user)
        another_user_id = CustomUser.objects.get(username='admin').id
        path = reverse('users:user_update', kwargs={'pk': another_user_id})
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, '/users/')
        self.assertRaisesMessage(response, ('У вас нет прав для изменения '
                                            'другого пользователя.'))


class D(TestCase):
    fixtures = ['task_manager/fixtures/users.json',
                'task_manager/fixtures/statuses.json',
                'task_manager/fixtures/tasks.json']

    def setUp(self):
        self.user = CustomUser.objects.get(username='igor')
        self.path = reverse('users:user_delete', kwargs={'pk': self.user.id})

    def test_user_delete_success(self):
        self.client.force_login(self.user)
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(CustomUser.objects.filter(username=self.user.username).exists())
        self.assertRedirects(response, '/users/')
        self.assertRaisesMessage(response, 'Пользователь успешно удален')

    def test_user_delete_error(self):
        self.client.force_login(self.user)
        another_user = CustomUser.objects.first()
        path = reverse('users:user_delete', kwargs={'pk': another_user.id})
        response = self.client.post(path)
        self.assertTrue(CustomUser.objects.filter(username=self.user.username).exists())
        self.assertRedirects(response, '/users/')
        self.assertRaisesMessage(response, ('У вас нет прав для изменения '
                                            'другого пользователя.'))

    def test_user_delete_error_with_task(self):
        self.client.force_login(self.user)
        task = Task.objects.first()
        self.user.tasks_author.add(task)
        path = reverse('users:user_delete', kwargs={'pk': self.user.id})
        response = self.client.post(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(CustomUser.objects.filter(username=self.user.username).exists())
        self.assertRedirects(response, '/users/')
        self.assertRaisesMessage(response, ('Невозможно удалить пользователя, '
                                            'потому что он используется'))
