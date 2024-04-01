from django.contrib.auth.mixins import UserPassesTestMixin
from django.http.request import HttpRequest as HttpRequest
from django.shortcuts import redirect
from django.contrib import messages


class ModificationUserMixin(UserPassesTestMixin):
    permission_message = ''
    permission_url = ''

    def test_func(self):
        return self.get_object() == self.request.user
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'У вас нет прав для изменения другого пользователя.')
            return redirect(self.permission_url)
        messages.info(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect('login')


class TaskDeleteMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user
    
    def handle_no_permission(self):
        messages.error(self.request, 'Задачу может удалить только ее автор')
        return redirect('tasks:tasks_show')
