from django import forms
from django.utils.translation import gettext

from statuses.models import Status


class StatusCreateForm(forms.ModelForm):
    name = forms.CharField(label=gettext('Имя'))

    class Meta:
        model = Status
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': gettext('Имя'), 'required id': 'id_name', 'name': 'name', })