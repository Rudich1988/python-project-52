from django.shortcuts import redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusCreateForm


class StatusesCreateView(SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusCreateForm
    template_name = 'statuses/status_create.html'
    success_url = reverse_lazy('statuses:statuses_show')
    success_message = 'Статус успешно создан'


class StatusesShowView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses_show.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        return context


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_delete.html'
    success_url = reverse_lazy('statuses:statuses_show')
    success_message = 'Статус успешно удален'

    def post(self, request, *args, **kwargs):
        status = Status.objects.get(id=kwargs.get('pk'))
        if status.tasks_status.all().exists():
            messages.error(request, ('Невозможно удалить статус, '
                                     'потому что он используется'))
            return redirect('statuses:statuses_show')
        status.delete()
        messages.success(request, self.success_message)
        return redirect(self.success_url)


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusCreateForm
    template_name = 'statuses/status_update.html'
    success_url = reverse_lazy('statuses:statuses_show')
    success_message = 'Статус успешно изменен'
