from django.db.models import Count, Avg
from django.shortcuts import render

from movies.models import Film
from reviews.models import Mark


def page_not_found(request, exception):
    return render(request, 'base/404.html', status=404)


def index(request):
    random_film = Film.objects.order_by('?').first()

    average_mark = Mark.objects.filter(movie=random_film).aggregate(Avg('value'))['value__avg']

    if average_mark is None:
        average_mark = 0

    return render(request, 'base/index.html',
                  context={'title': 'Главная страница', 'film': random_film,
                           'average_mark': round(average_mark, 1)})


def terms(request):
    return render(request, 'base/terms.html', context={'title': 'Правила использования'})


def contacts(request):
    return render(request, 'base/contacts.html', context={'title': 'Обратная связь'})
