from django.db import models

from users.models import CustomUser
from statuses.models import Status
from labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Имя')
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание')
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT,
                               related_name='tasks_author',
                               verbose_name='Автор')
    status = models.ForeignKey(Status, on_delete=models.PROTECT,
                               related_name='tasks_status',
                               verbose_name='Статус')
    executor = models.ForeignKey(CustomUser, on_delete=models.PROTECT,
                                 related_name='tasks_executor', null=True,
                                 blank=True, verbose_name='Исполнитель')
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(Label, null=True, blank=True)
