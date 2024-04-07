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
    executor = forms.ModelChoiceField(queryset=CustomUser.objects.all(), required=False)
    author = forms.ModelChoiceField(queryset=CustomUser.objects.all())
    labels = forms.ModelMultipleChoiceField(queryset=Label.objects.all(), required=False)

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {'name': 'Имя', 'description': gettext('Описание'), 'status': gettext('Статус'), 'executor': gettext('Испонитель'), 'label_set': gettext('Метки')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': gettext('Имя'), 'required id': 'id_name', 'max_length': 150})
        self.fields['description'].widget.attrs.update({'name': 'description', 'cols': 40, 'class': 'form-control', 'placeholder': gettext('Описание'), 'id': 'id_description'})
        self.fields['status'].widget.attrs.update({'name': 'status', 'class': 'form-select', 'required id': 'id_status'})
        self.fields['executor'].widget.attrs.update({'name': 'executor', 'class': 'form-select', 'id': 'id_executor'})
        self.labels['labels'].widget.attrs.update({'name': 'labels', 'class': 'form-select', 'id': 'id_labels'})


class TaskSearchForm(forms.Form):
    status = forms.ModelChoiceField(label=gettext('Статус'), queryset=Status.objects.all(), required=False)
    executor = forms.ModelChoiceField(label=gettext('Исполнитель'), queryset=CustomUser.objects.all(), required=False)
    labels = forms.ModelChoiceField(label=gettext('Метка'), queryset=Label.objects.all(), required=False)
    author = forms.BooleanField(label=gettext('Только свои задачи'), required=False)

    class Meta:
        model = Task
        field = ['status', 'executor', 'labels', 'author']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({'class': 'form-select', 'name': 'status', 'id': 'id_status'})
        self.fields['executor'].widget.attrs.update({'class': 'form-select', 'name': 'executor', 'id': 'id_executor'})
        self.fields['labels'].widget.attrs.update({'class': 'form-select', 'name': 'label', 'id': 'id_label'})
    