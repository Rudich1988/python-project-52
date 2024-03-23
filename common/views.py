from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http.request import HttpRequest as HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages


class ModificationUserMixin(LoginRequiredMixin):   
    def dispatch(self, request, *args, **kwargs):
        #dispatch = super().dispatch(request, *args, **kwargs)
        user = request.user
        if user.is_authenticated:
            if user.id == kwargs.get('pk') and (len(list(user.tasks_author.all())) == 0 and len(list(user.tasks_executor.all())) == 0):
                return super().dispatch(request, *args, **kwargs)#dispatch
            elif user.id == kwargs.get('pk') and (len(list(user.tasks_author.all())) != 0 or len(list(user.tasks_executor.all())) != 0):
                messages.error(request, 'Невозможно удалить пользователя, потому что он используется')
                return redirect('users:users_show')
            else:
                messages.error(request, 'У вас нет прав для изменения другого пользователя.')
                return redirect('users:users_show')
        else:
            messages.info(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('login')
        

class StatusDeleteMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        dispatch = super().dispatch(request, *args, **kwargs)
        if len(list(self.object.tasks_status.all())) == 0:
            return dispatch
        messages.error(request, 'Невозможно удалить статус, потому что он используется')
        return redirect('statuses:statuses_show')
    

class TaskDeleteMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        dispatch = super().dispatch(request, *args, **kwargs)
        user = request.user
        if self.object.author == user and user.is_authenticated:
            self.object.delete()
            messages.success( request, 'Задача успешно удалена')
            return redirect('tasks:tasks_show')
        messages.error(request, 'Задачу может удалить только ее автор')
        return redirect('tasks:tasks_show')
