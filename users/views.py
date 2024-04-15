from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from users.forms import LoginForm, RegisterForm, UserUpdateForm
from users.models import CustomUser


class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('index')


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    form_class = RegisterForm
    success_message = "Your profile was created successfully"
    extra_context = {'title': 'Регистрация', 'button': 'Зарегистрироваться'}


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))


class UserProfileView(DetailView):
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'user_p'

    def get_object(self, queryset=None):
        return CustomUser.objects.get(username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Профиль  " + self.kwargs['username']
        return context


class UpdateUserPage(UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Обновление профиля', 'button': 'Обновить'}

    def get_object(self, queryset=None):
        return self.request.user

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.birth_date:
            initial['birth_date'] = self.request.user.birth_date
        return initial

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'username': self.request.user.username})
