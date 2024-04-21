from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext as _

from apps.users.models import CustomUser
from apps.users.forms import UserLoginForm


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLoginView(LoginView):
    model = CustomUser
    form_class = UserLoginForm
    template_name = 'login.html'

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
                messages.success(request, _('Вы залогинены'))
                return redirect('index')
        return render(request, self.template_name, context={'form': form})


def logoutview(request):
    logout(request)
    messages.info(request, _('Вы разлогинены'))
    return redirect('index')
