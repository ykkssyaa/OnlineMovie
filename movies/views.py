from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from movies.models import Film, Episode


class FilmListView(ListView):
    # model = Film
    template_name = 'movies/list.html'
    context_object_name = 'movies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список фильмов и сериалов'
        return context

    def get_queryset(self):
        media_type = self.request.GET.get('type')
        search_query = self.request.GET.get('search')
        franchise_query = self.request.GET.get('franchise')

        # Инициализируем QuerySet без фильтрации
        queryset = Film.objects.filter(publication_status=True)

        if media_type:
            queryset = queryset.filter(media_type=media_type)

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        if franchise_query:
            queryset = queryset.filter(franchise__name__icontains=franchise_query)

        return queryset


class FilmDetailView(DetailView):
    model = Film
    template_name = 'movies/film_detail.html'
    context_object_name = 'film'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.publication_status:
            raise Http404("Фильм не найден")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        film = self.get_object()
        context['title'] = film.name
        episodes_by_series = {}

        for episode in self.object.episode_set.all().order_by('number'):
            season = episode.season
            if season not in episodes_by_series:
                episodes_by_series[season] = []
            episodes_by_series[season].append(episode)
        context['episodes_by_series'] = episodes_by_series

        return context


class EpisodeDetailView(DetailView):
    model = Episode
    template_name = 'movies/episode_detail.html'
    context_object_name = 'episode'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем текущий эпизод
        current_episode = self.object

        # Получаем следующий эпизод в той же серии
        next_episode = Episode.objects.filter(series=current_episode.series, season=current_episode.season,
                                              number=current_episode.number + 1).first()

        # Получаем предыдущий эпизод в той же серии
        previous_episode = Episode.objects.filter(series=current_episode.series, season=current_episode.season,
                                                  number=current_episode.number - 1).first()

        context['next_episode'] = next_episode
        context['previous_episode'] = previous_episode
        context['title'] = current_episode.series.name + ": " + current_episode.name

        return context
