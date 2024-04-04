from django.http import HttpResponse
from django.http.request import HttpRequest as HttpRequest
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from statuses.forms import StatusCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from tasks.models import Task
from .models import Label
from .forms import LabelCreateForm


class LabelsShowView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/labels_show.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = Label.objects.all()
        return context
    

class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelCreateForm
    template_name = 'labels/label_create.html'
    success_url = reverse_lazy('labels:labels_show')
    success_message = 'Метка успешно создана'   


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelCreateForm
    template_name = 'labels/label_update.html'
    success_url = reverse_lazy('labels:labels_show')
    success_message = 'Метка успешно изменена'


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('labels:labels_show')
    success_message = 'Метка успешно удалена'

    def post(self, request, *args, **kwargs):
        label = Label.objects.get(id=kwargs.get('pk'))
        if label.task_set.all().exists():
            messages.error(request, 'Невозможно удалить метку, потому что она используется')
            return redirect(self.success_url)
        label.delete()
        messages.success(request, self.success_message)
        return redirect(self.success_url)
