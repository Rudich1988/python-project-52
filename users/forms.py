from typing import Any
from django import forms
from users.models import CustomUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       PasswordResetForm, SetPasswordForm,
                                       UserCreationForm)



class UserRegistrationForm(UserCreationForm):
    
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    username = forms.CharField(label='Имя пользователя', help_text='Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.')
    password1 = forms.CharField(label='Пароль', help_text='Ваш пароль должен содержать как минимум 3 символа.', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Подтверждение пароля', help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.', widget=forms.PasswordInput(), validators=[MinLengthValidator(3, message='Введённый пароль слишком короткий. Он должен содержать как минимум 3 символа.')])
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Имя', 'required id': 'id_first_name', 'maxlength': 150})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Фамилия', 'required id': 'id_last_name', 'maxlength': 150})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Имя пользователя', 'required id': 'id_username', 'maxlength': 150})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Пароль', 'required id': 'id_password1', 'maxlength': 150, 'autocomplete': 'new-password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Подтверждение пароля', 'required id': 'id_password2', 'maxlength': 150, 'autocomplete': 'new-password'})


'''
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя',
        'required id': 'id_username',
        'maxlength': 150,
        'autocomplete': 'username',
        'autofocus autocapitalize': 'none'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль',
        'required id': 'id_password',
        'autocomplete': 'current-password',
    }))
'''

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Имя пользователя', 'required id': 'id_username', 'maxlength': 150, 'autocomplete': 'username', 'autofocus autocapitalize': 'none'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Пароль', 'required id': 'id_password', 'autocomplete': 'current-password',})
