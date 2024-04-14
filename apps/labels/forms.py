from django import forms
from django.utils.translation import gettext

from .models import Label


class LabelCreateForm(forms.ModelForm):
    name = forms.CharField(label=gettext('Имя'))

    class Meta:
        model = Label
        fields = ['name']
