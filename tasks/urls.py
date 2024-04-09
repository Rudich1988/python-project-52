from django.urls import path

from .views import (TaskCreateView, TasksShowView,
                    TaskDeleteView, TaskDetailView, TaskUpdateView)


app_name = 'tasks'


urlpatterns = [
    path('', TasksShowView.as_view(), name='tasks_show'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/delete', TaskDeleteView.as_view(), name='task_delete'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
]
