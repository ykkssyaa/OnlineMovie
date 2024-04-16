from django.urls import path

from reviews import views

urlpatterns = [
    path('add_review/<int:film_id>/', views.add_review, name='add_review'),
    path('add_mark/<int:film_id>/', views.add_mark, name='add_mark'),
]
