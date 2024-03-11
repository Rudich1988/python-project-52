from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from statuses.forms import StatusCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin

from statuses.models import Status


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = kwargs.get('object').name
        return context
    

class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusCreateForm
    template_name = 'statuses/status_update.html'
    success_url = reverse_lazy('statuses:statuses_show')
    success_message = 'Статус успешно изменен'

