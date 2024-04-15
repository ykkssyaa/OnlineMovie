import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField


def user_photo_path(instance, filename):
    user_id = instance.id
    user_username = instance.username
    _, file_extension = os.path.splitext(filename)
    return f'users/{user_id}_{user_username}{file_extension}'


class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to=user_photo_path, blank=True, null=True, verbose_name='photo')
    created = models.DateField(auto_now_add=True)
    bio = models.TextField(max_length=255, blank=True, null=True)
    country = CountryField()
    birth_date = models.DateField(blank=True, null=True, verbose_name='Date of Birth')
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
                              blank=True, null=True)
    adult_content_permission = models.BooleanField(default=None, null=True, verbose_name='Adult Content Permission')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return f'/users/{self.username}'
