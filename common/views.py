from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.request import HttpRequest as HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages


class ModificationUserMixin(LoginRequiredMixin):
    
    def dispatch(self, request, *args, **kwargs):
        dispatch = super().dispatch(request, *args, **kwargs)
        user = request.user
        if user.is_authenticated:
            if user.id == kwargs.get('pk'):
                return dispatch
            else:
                messages.error(request, 'У вас нет прав для изменения другого пользователя.')
                return redirect('users:users_show')
        else:
            messages.info(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('users:login')
        


