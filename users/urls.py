from django.urls import path
import users.views as views

urlpatterns = [
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.SignUpView.as_view(), name='register'),

    # path('users/update', views.UpdateUserPage.as_view(), name='update'),
    path('users/<str:username>', views.UserProfileView.as_view(), name='profile'),
]
