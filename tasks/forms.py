from django import forms
from django.utils.translation import gettext


from tasks.models import Task
from statuses.models import Status
from users.models import CustomUser
from labels.models import Label


class TaskCreateForm(forms.ModelForm):
    name = forms.CharField(label=gettext('Имя'))
    description = forms.CharField(widget=forms.Textarea)
    status = forms.ModelChoiceField(queryset=Status.objects.all())
    executor = forms.ModelChoiceField(queryset=CustomUser.objects.all(),
                                      required=False)
    author = forms.ModelChoiceField(queryset=CustomUser.objects.all())
    labels = forms.ModelMultipleChoiceField(label='Метки',
                                            queryset=Label.objects.all(),
                                            required=False)

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']


class TaskSearchForm(forms.Form):
    status = forms.ModelChoiceField(label=gettext('Статус'),
                                    queryset=Status.objects.all(),
                                    required=False)
    executor = forms.ModelChoiceField(label=gettext('Исполнитель'),
                                      queryset=CustomUser.objects.all(),
                                      required=False)
    labels = forms.ModelChoiceField(label=gettext('Метка'),
                                    queryset=Label.objects.all(),
                                    required=False)
    author = forms.BooleanField(label=gettext('Только свои задачи'),
                                required=False)

    class Meta:
        model = Task
        field = ['status', 'executor', 'labels', 'author']
