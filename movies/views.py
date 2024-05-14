from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from movies.models import Film, Episode
from reviews.forms import ReviewForm, MarkForm
from reviews.models import Review, Mark


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

        if self.request.user.is_authenticated:
            review = Review.objects.filter(movie=film, user=self.request.user).first()
        else:
            review = None

        if review:
            # Если рецензия найдена, вставляем её текст в форму
            context['form'] = ReviewForm(instance=review)
            context['my_review'] = review
        else:
            # Иначе создаем пустую форму
            context['form'] = ReviewForm()

        if self.request.user.is_authenticated:
            mark = Mark.objects.filter(movie=film, user=self.request.user).first()
        else:
            mark = None

        if mark:
            context['markForm'] = MarkForm(instance=mark)
        else:
            context['markForm'] = MarkForm()

        average_mark = Mark.objects.filter(movie=film).aggregate(Avg('value'))['value__avg']

        if average_mark is None:
            average_mark = 0

        context['average_mark'] = round(average_mark, 1)

        return context

    def render_to_response(self, context, **response_kwargs):
        film = self.get_object()

        if film.adult_content and (
                not self.request.user.is_authenticated or not self.request.user.adult_content_permission):
            confirmation_displayed = self.request.session.get('adult_content_confirmation_displayed', False)
            if not confirmation_displayed:
                self.request.session['adult_content_confirmation_displayed'] = True
                return render(self.request, 'movies/confirm_adult_content.html', context)

        return super().render_to_response(context, **response_kwargs)


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


@login_required
def add_to_bookmarks(request, pk):
    film = get_object_or_404(Film, pk=pk)
    if request.method == 'POST':
        request.user.bookmarks.add(film)
        return redirect('movies:detail', pk=pk)


def remove_from_bookmarks(request, pk):
    film = get_object_or_404(Film, pk=pk)
    if request.method == 'POST':
        request.user.bookmarks.remove(film)
        return redirect('movies:detail', pk=pk)
