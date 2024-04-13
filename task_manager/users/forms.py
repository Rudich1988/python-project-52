from django import forms
from django.utils.translation import gettext_lazy as _, gettext
from django.core.validators import MinLengthValidator
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from task_manager.users.models import CustomUser
from task_manager.users.help_error_texts import (USERNAME_HELP_TEXT, PASSWORD_ERROR_TEXT,
                                    PASSWORD_HELP_TEXT, PASSWORD2_HELP_TEXT)


class UserRegistrationForm(UserCreationForm):

    first_name = forms.CharField(label=gettext('Имя'))
    last_name = forms.CharField(label=gettext('Фамилия'))
    username = forms.CharField(label=gettext('Имя пользователя'),
                               help_text=_(USERNAME_HELP_TEXT))
    password1 = forms.CharField(label=gettext('Пароль'),
                                help_text=_(PASSWORD_HELP_TEXT),
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label=gettext('Подтверждение пароля'),
                                help_text=_(PASSWORD2_HELP_TEXT),
                                widget=forms.PasswordInput(),
                                validators=[MinLengthValidator(3,
                                                               message=_(
                                                                   PASSWORD_ERROR_TEXT))])

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label=gettext('Имя'))
    last_name = forms.CharField(label=gettext('Фамилия'))
    username = forms.CharField(label=gettext('Имя пользователя'),
                               help_text=_(USERNAME_HELP_TEXT))
    password1 = forms.CharField(label=gettext('Пароль'),
                                help_text=_(PASSWORD_HELP_TEXT),
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label=gettext('Подтверждение пароля'),
                                help_text=_(PASSWORD2_HELP_TEXT),
                                widget=forms.PasswordInput(),
                                validators=[MinLengthValidator(3,
                                                               message=_((PASSWORD_ERROR_TEXT)))])

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name',
                  'username', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput())
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ('username', 'password')
