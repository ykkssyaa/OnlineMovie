from django.urls import path

import movies.views as views

urlpatterns = [
    path('', views.FilmListView.as_view(), name='list'),
    path('<int:pk>', views.FilmDetailView.as_view(), name='detail'),
    path('episode/<int:pk>/', views.EpisodeDetailView.as_view(), name='episode_detail'),

    path('<int:pk>/add-to-bookmarks/', views.add_to_bookmarks, name='add_to_bookmarks'),
    path('<int:pk>/remove-from-bookmarks/', views.remove_from_bookmarks, name='remove_from_bookmarks'),

]
