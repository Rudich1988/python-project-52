from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.views.generic.list import ListView
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from apps.users.models import CustomUser
from apps.users.forms import UserRegistrationForm, UserUpdateForm
from task_manager.common.views import ModificationUserMixin


class UserRegistrationView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('login')
    success_message = _('Пользователь успешно зарегистрирован')


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
    permission_message = (_('Невозможно удалить пользователя, '
                          'потому что он используется'))
    permission_url = reverse_lazy('users:users_show')

    def post(self, request, *args, **kwargs):
        if (self.get_object().tasks_author.all().exists()
                or self.get_object().tasks_executor.all().exists()):
            messages.error(self.request, self.permission_message)
            return redirect('users:users_show')
        return super().post(request, *args, **kwargs)


class UserUpdateView(ModificationUserMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users:users_show')
    success_message = _('Пользователь успешно изменен')
    permission_url = reverse_lazy('users:users_show')

    def form_valid(self, form):
        user = form.save(commit=True)
        password = form.cleaned_data['password1']
        user.set_password(password)
        user.save()
        logout(self.request)
        messages.success(self.request, self.success_message)
        return redirect(self.success_url)
