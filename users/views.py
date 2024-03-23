from django.http import HttpRequest, HttpResponse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from users.models import CustomUser
from users.forms import UserRegistrationForm
from common.views import ModificationUserMixin


class UserRegistrationView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегестрирован'


class UsersShowView(ListView):
    model = CustomUser
    template_name = 'users/users_show.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.all().order_by('created_at')
        return context
    

class UserDeleteView(ModificationUserMixin, SuccessMessageMixin, DeleteView):
    model = CustomUser
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('users:users_show')
    success_message = 'Пользователь успешно удален'


class UserDeleteTemplateView(TemplateView):
    template_name = 'users/user_delete_template.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = kwargs.get('pk')
        return context


class UserUpdateView(ModificationUserMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users:users_show')
    success_message = 'Пользователь успешно изменен'
    
