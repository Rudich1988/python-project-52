from django import forms


from tasks.models import Task
from statuses.models import Status
from users.models import CustomUser


class TaskCreateForm(forms.ModelForm):
    name = forms.CharField(label='Имя')
    description = forms.CharField(widget=forms.Textarea)
    status = forms.ModelChoiceField(queryset=Status.objects.all())
    executor = forms.ModelChoiceField(queryset=CustomUser.objects.all(), required=False)
    author = forms.ModelChoiceField(queryset=CustomUser.objects.all())

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor']
        labels = {'name': 'Имя', 'description': 'Описание', 'status': 'Статус', 'executor': 'Испонитель'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Имя', 'required id': 'id_name', 'max_length': 150})
        self.fields['description'].widget.attrs.update({'name': 'description', 'cols': 40, 'class': 'form-control', 'placeholder': 'Описание', 'id': 'id_description'})
        self.fields['status'].widget.attrs.update({'name': 'status', 'class': 'form-select', 'required id': 'id_status'})
        self.fields['executor'].widget.attrs.update({'name': 'executor', 'class': 'form-select', 'id': 'id_executor'})


class TaskSearchForm(forms.Form):
    status = forms.ModelChoiceField(label='Статус', queryset=Status.objects.all(), required=False)
    executor = forms.ModelChoiceField(label='Исполнитель', queryset=CustomUser.objects.all(), required=False)
    user_tasks = forms.BooleanField(label='Только свои задачи', required=False)

    class Meta:
        model = Task
        field = ['status', 'executor']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({'class': 'form-select', 'name': 'status', 'id': 'id_status'})
        self.fields['executor'].widget.attrs.update({'class': 'form-select', 'name': 'executor', 'id': 'id_executor'})
    