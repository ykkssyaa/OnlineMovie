from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from users.models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, label='Email')
    birth_date = forms.DateField(help_text='Обязательное поле. Формат: ДД-ММ-ГГГГ', input_formats=['%d-%m-%Y'],
                                 label='Дата рождения')
    gender = forms.ChoiceField(choices=[('male', 'Мужской'), ('female', 'Женский'), ('other', 'Другой')], label='Пол')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'birth_date', 'gender', 'country')
        labels = {
            'username': 'Имя пользователя',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
            'country': 'Страна',
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин", max_length=150)
    password = forms.CharField(label="Пароль", strip=False, widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'password')
