from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, include
from django.views.generic import RedirectView

from django.conf import settings
from django.conf.urls.static import static

import views

urlpatterns = [
    path('', views.index, name='index'),

    path('admin/', admin.site.urls),
    path("terms/", views.terms, name="terms"),

    path('movies/', include(('movies.urls', 'movies'))),
    path('reviews/', include(('reviews.urls', 'reviews'))),
    path('', include(('users.urls', 'users'))),


    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("img/icon.png")),
        name="favicon"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.page_not_found
