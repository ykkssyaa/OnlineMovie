from django.urls import path

import movies.views as views

urlpatterns = [
    path('', views.FilmListView.as_view(), name='list'),
    path('<int:pk>', views.FilmDetailView.as_view(), name='detail'),
    path('episode/<int:pk>/', views.EpisodeDetailView.as_view(), name='episode_detail'),
]
