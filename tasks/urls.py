from django.urls import path

from .views import TaskCreateView, TasksShowView, TaskDeleteView, TaskTemplateDelete, TaskShowTemplateView


app_name = 'tasks'


urlpatterns = [
    path('', TasksShowView.as_view(), name='tasks_show'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/delete', TaskDeleteView.as_view(), name='task_delete'),
    path('<int:pk>/delete/', TaskTemplateDelete.as_view(), name='task_delete_template'),
    path('<int:pk>/', TaskShowTemplateView.as_view(), name='task_show_template'),
]