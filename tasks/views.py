from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView

from statuses.models import Status
from tasks.models import Task
from labels.models import Label
from users.models import CustomUser
from tasks.forms import TaskCreateForm, TaskSearchForm
from common.views import TaskDeleteMixin


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form = TaskCreateForm
    fields = ['name', 'description', 'status', 'executor', 'labels']
    template_name = 'tasks/task_create.html'
    success_url = reverse_lazy('tasks:tasks_show')
    success_message = 'Задача успешно создана'

    def form_valid(self, form):
        instance = form.save(commit=False)
       #if form.cleaned_data['label_set']:
           #labels = form.cleaned_data['label_set']
           #instance.label_set.set(labels)
        instance.author = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TasksShowView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/tasks_show.html'

    def get_queryset(self):
        status = self.request.GET.get('status')
        executor = self.request.GET.get('executor')
        show_user_tasks = self.request.GET.get('user_tasks')
        if show_user_tasks:
            if status and executor:
                return Task.objects.filter(author=self.request.user, status=status, executor=executor)
            if executor:
                return Task.objects.filter(author=self.request.user, executor=executor)
            if status:
                return Task.objects.filter(author=self.request.user, status=status)
            return Task.objects.filter(author=self.request.user)
        if status and executor:
            return Task.objects.filter(status=status, executor=executor)
        if executor:
            return Task.objects.filter(executor=executor)
        if status:
            return Task.objects.filter(status=status)
        return Task.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.get_queryset()
        context['form'] = TaskSearchForm(initial=self.request.GET)
        return context
    

class TaskDetailView(TemplateView):
    template_name = 'tasks/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = Task.objects.get(id=kwargs.get('pk'))
        context['labels'] = Task.objects.get(id=kwargs.get('pk')).labels.all()
        return context


class TaskDeleteView(TaskDeleteMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_delete.html'
    success_message = 'Задача успешно удалена'
    success_url = reverse_lazy('tasks:tasks_show')
   

class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    template_name = 'tasks/task_update.html'
    success_message = 'Задача успешно изменена'
    success_url = reverse_lazy('tasks:tasks_show')
    fields = ['name', 'description', 'status', 'executor', 'labels']
    