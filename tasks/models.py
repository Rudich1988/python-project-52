from django.db import models
from users.models import CustomUser
from statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='author')
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name='statuses')
    executor = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='executor')
    created_at = models.DateTimeField(auto_now_add=True)
    