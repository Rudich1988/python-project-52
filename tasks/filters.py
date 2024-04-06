import django_filters

from .models import Task
from labels.models import Label

class TaskFilter(django_filters.FilterSet):

    class Meta:
        model = Task
        fields = ['status', 'executor', 'author', 'labels']