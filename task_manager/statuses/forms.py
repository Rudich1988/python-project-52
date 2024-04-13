from django import forms
from django.utils.translation import gettext

from task_manager.statuses.models import Status


class StatusCreateForm(forms.ModelForm):
    name = forms.CharField(label=gettext('Имя'))

    class Meta:
        model = Status
        fields = ['name']