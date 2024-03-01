from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, FormView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic.list import ListView

from users.models import CustomUser
from users.forms import UserRegistrationForm, UserLoginForm


class UserRegistrationView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Пользователь успешно зарегестрирован'


class UserLoginView(LoginView):
    model = CustomUser
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)               
                messages.success(request, 'Вы залогинены')
                return redirect('index')
        messages.error(request, 'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.')
        return render(request, self.template_name, context={'form': form})


def logoutview(request):
    logout(request)
    messages.info(request, 'Вы разлогинены')
    return redirect('index')

class UsersShowView(SuccessMessageMixin, ListView):
    model = CustomUser
    template_name = 'users/users_show.html'
    success_message = 'проверка сообщения'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.all().order_by('created_at')
        return context
    

class UserDeleteView(SuccessMessageMixin, DeleteView):
    model = CustomUser
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('users:users_show')
    success_message = 'Пользователь успешно удален'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = kwargs.get('object')
        return context


class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users:users_show')
    success_message = 'Пользователь успешно изменен'
