from django.db import models

from tasks.models import Task


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tasks = models.ManyToManyField(Task)

    def __str__(self):
        return self.name
