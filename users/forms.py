from io import BytesIO
from PIL import Image

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.files.base import ContentFile

from users.models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, label='Email')
    birth_date = forms.DateField(help_text='Обязательное поле. Формат: ДД-ММ-ГГГГ', input_formats=['%d-%m-%Y'],
                                 label='Дата рождения')
    gender = forms.ChoiceField(choices=[('male', 'Мужской'), ('female', 'Женский'), ('other', 'Другой')], label='Пол')

    class Meta:
        model = get_user_model()
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
        model = get_user_model()
        fields = ('username', 'password')


class UserUpdateForm(forms.ModelForm):
    gender = forms.ChoiceField(label='Пол', choices=[('male', 'Мужской'), ('female', 'Женский'), ('other', 'Другой')])

    class Meta:
        model = CustomUser
        fields = ['email', 'photo', 'bio', 'country', 'birth_date', 'gender']
        labels = {
            'email': 'email',
            'photo': 'Фото',
            'bio': 'Описание',
            'country': 'Страна',
            'birth_date': 'Дата рождения',
        }
        widgets = {
            'birth_date': forms.DateInput(
               # attrs={'type': 'date'},
            ),
        }

    def __init__(self, *args, **kwargs):

        super(UserUpdateForm, self).__init__(*args, **kwargs)

        self.fields['photo'].required = False
        self.fields['bio'].required = False
        self.fields['country'].required = False

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)

        # Если загружено изображение
        if 'photo' in self.files:
            photo = self.files['photo']
            if photo:
                # Открываем изображение с помощью PIL
                img = Image.open(photo)

                # Конвертируем изображение в режим RGB
                img = img.convert('RGB')

                # Определяем размеры центральной части изображения
                width, height = img.size
                min_dim = min(width, height)
                left = int((width - min_dim) / 2)
                top = int((height - min_dim) / 2)
                right = int((width + min_dim) / 2)
                bottom = int((height + min_dim) / 2)

                # Обрезаем изображение, оставляя центральную часть
                img_cropped = img.crop((left, top, right, bottom))

                # Перезаписываем изображение
                img_cropped_io = BytesIO()
                img_cropped.save(img_cropped_io, format='JPEG')

                user.photo.save(photo.name, ContentFile(img_cropped_io.getvalue()), save=False)

        if commit:
            user.save()
        return user