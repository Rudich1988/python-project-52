from django.db import models
from django.utils.translation import gettext as _

from apps.users.models import CustomUser
from apps.statuses.models import Status
from apps.labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=150, unique=True,
                            verbose_name=_('Имя'))
    description = models.TextField(blank=True, null=True,
                                   verbose_name=_('Описание'))
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT,
                               related_name='tasks_author',
                               verbose_name=_('Автор'))
    status = models.ForeignKey(Status, on_delete=models.PROTECT,
                               related_name='tasks_status',
                               verbose_name=_('Статус'))
    executor = models.ForeignKey(CustomUser, on_delete=models.PROTECT,
                                 related_name='tasks_executor', null=True,
                                 blank=True, verbose_name=_('Исполнитель'))
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(Label, verbose_name=_('Метки'))
