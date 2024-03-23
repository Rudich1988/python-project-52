from django.http.request import HttpRequest as HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from statuses.forms import StatusCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from common.views import StatusDeleteMixin

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
    
class StatusDeleteErrorTemplateView(TemplateView):
    template_name = 'statuses/status_delete_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = kwargs.get('pk')
        context['name'] = Status.objects.get(id=kwargs.get('pk'))
        return context
    

class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_delete.html'
    success_url = reverse_lazy('statuses:statuses_show')
    success_message = 'Статус успешно удален'
    
    def dispatch(self, request, *args, **kwargs):
        dispatch = super().dispatch(request, *args, **kwargs)
        try:
            if len(Status.objects.get(id=kwargs.get('pk')).tasks_status.all()) > 0:
                messages.error(request, 'Невозможно удалить статус, потому что он используется')
                return redirect('statuses:statuses_show')
            else:
                return dispatch
        except Exception:
            return dispatch
    
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

