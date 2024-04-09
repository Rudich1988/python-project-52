from django import forms
from django.utils.translation import gettext_lazy as _, gettext
from django.core.validators import MinLengthValidator
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import CustomUser


class UserRegistrationForm(UserCreationForm):
    
    first_name = forms.CharField(label=gettext('Имя'))
    last_name = forms.CharField(label=gettext('Фамилия'))
    username = forms.CharField(label=gettext('Имя пользователя'),
                               help_text=_('Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.'))
    password1 = forms.CharField(label=gettext('Пароль'),
                                help_text=_('Ваш пароль должен содержать как минимум 3 символа.'), widget=forms.PasswordInput())
    password2 = forms.CharField(label=gettext('Подтверждение пароля'),
                                help_text=_('Для подтверждения введите, пожалуйста, пароль ещё раз.'),
                                widget=forms.PasswordInput(),
                                validators=[MinLengthValidator(3, message=_('Введённый пароль слишком короткий. Он должен содержать как минимум 3 символа.'))])
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': gettext('Имя'), 'required id': 'id_first_name', 'maxlength': 150})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': gettext('Фамилия'), 'required id': 'id_last_name', 'maxlength': 150})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': gettext('Имя пользователя'), 'required id': 'id_username', 'maxlength': 150})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': gettext('Пароль'), 'required id': 'id_password1', 'maxlength': 150, 'autocomplete': 'new-password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': gettext('Подтверждение пароля'), 'required id': 'id_password2', 'maxlength': 150, 'autocomplete': 'new-password'})


class UserUpdateForm(forms.ModelForm):   
    first_name = forms.CharField(label=gettext('Имя'))
    last_name = forms.CharField(label=gettext('Фамилия'))
    username = forms.CharField(label=gettext('Имя пользователя'),
                               help_text=_('Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.'))
    password1 = forms.CharField(label=gettext('Пароль'),
                                help_text=_('Ваш пароль должен содержать как минимум 3 символа.'),
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label=gettext('Подтверждение пароля'),
                                help_text=_(('Для подтверждения введите, '
                                             'пожалуйста, пароль ещё раз.')),
                                widget=forms.PasswordInput(),
                                validators=[MinLengthValidator(3,
                                message=_(('Введённый пароль слишком короткий. '
                                          'Он должен содержать как '
                                          'минимум 3 символа.')))])
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name',
                  'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control',
                                                       'placeholder': gettext('Имя'),
                                                       'required id': 'id_first_name',
                                                       'maxlength': 150})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control',
                                                      'placeholder': gettext('Фамилия'),
                                                      'required id': 'id_last_name',
                                                      'maxlength': 150})
        self.fields['username'].widget.attrs.update({'class': 'form-control',
                                                     'placeholder': gettext('Имя пользователя'),
                                                     'required id': 'id_username',
                                                     'maxlength': 150})
        self.fields['password1'].widget.attrs.update({'class': 'form-control',
                                                      'placeholder': gettext('Пароль'),
                                                      'required id': 'id_password1',
                                                      'maxlength': 150,
                                                      'autocomplete': 'new-password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control',
                                                      'placeholder': gettext('Подтверждение пароля'),
                                                      'required id': 'id_password2',
                                                      'maxlength': 150,
                                                      'autocomplete': 'new-password'})


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput())
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control',
                                                     'placeholder': gettext('Имя пользователя'),
                                                     'required id': 'id_username',
                                                     'maxlength': 150,
                                                     'autocomplete': 'username',
                                                     'autofocus autocapitalize': 'none'})
        self.fields['password'].widget.attrs.update({'class': 'form-control',
                                                     'placeholder': gettext('Пароль'),
                                                     'required id': 'id_password',
                                                     'autocomplete': 'current-password'})
