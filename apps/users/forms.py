from django import forms
from django.utils.translation import gettext_lazy as _, gettext
from django.core.validators import MinLengthValidator
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from apps.users.models import CustomUser


USERNAME_HELP_TEXT = ('Обязательное поле. Не более 150 символов. '
                      'Только буквы, цифры и символы @/./+/-/_.')
PASSWORD_ERROR_TEXT = ('Введённый пароль слишком короткий. '
                       'Он должен содержать как минимум 3 символа.')
PASSWORD_HELP_TEXT = 'Ваш пароль должен содержать как минимум 3 символа.'
PASSWORD2_HELP_TEXT = 'Для подтверждения введите, пожалуйста, пароль ещё раз.'


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
    username = forms.CharField(label=gettext('Имя пользователя'),
                               widget=forms.TextInput())
    password = forms.CharField(label=gettext('Пароль'),
                               widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ('username', 'password')
