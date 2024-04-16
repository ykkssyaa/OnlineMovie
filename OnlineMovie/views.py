from django.db.models import Count
from django.shortcuts import render
def page_not_found(request, exception):
    return render(request, 'base/404.html', status=404)

def index(request):
    return render(request, 'base/index.html', context={'title': 'Главная страница'})

def terms(request):
    return render(request, 'base/terms.html', context={'title': 'Правила использования'})


def contacts(request):
    return render(request, 'base/contacts.html', context={'title': 'Обратная связь'})
