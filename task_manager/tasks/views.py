from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskCreateForm, TaskSearchForm
from task_manager.common.views import TaskDeleteMixin
from .filters import TaskFilter


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form = TaskCreateForm
    fields = ['name', 'description', 'status', 'executor', 'labels']
    template_name = 'tasks/task_create.html'
    success_url = reverse_lazy('tasks:tasks_show')
    success_message = 'Задача успешно создана'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TasksShowView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/tasks_show.html'

    def get_queryset(self):
        task_author = self.request.GET.get('author')
        if task_author:
            task = Task.objects.filter(author=self.request.user)
            return TaskFilter(self.request.GET,
                              queryset=task)
        return TaskFilter(self.request.GET, queryset=Task.objects.all())

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
