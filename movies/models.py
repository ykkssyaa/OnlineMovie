from django.db import models
from django_countries.fields import CountryField
from taggit.managers import TaggableManager


class FilmStudio(models.Model):
    name = models.CharField(max_length=255)
    country = CountryField()
    logo = models.ImageField(upload_to='film_studio_logos/', null=True, blank=True)

    def __str__(self):
        return self.name


class Franchise(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Film(models.Model):
    name = models.CharField(max_length=2048)
    premiere_date = models.DateField(verbose_name='Дата премьеры')
    announcement_date = models.DateField(null=True, blank=True, verbose_name='Дата анонса')
    cover = models.ImageField(upload_to='film_covers/', null=True, blank=True, verbose_name='Обложка')
    annotation = models.CharField(max_length=255, blank=True, verbose_name='Аннотация')
    adult_content = models.BooleanField(verbose_name='Контент для взрослых')
    publication_status = models.BooleanField(default=False, verbose_name='Статус публикации')
    publication_datetime = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время публикации')
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)

    tags = TaggableManager()

    def __str__(self):
        return self.name


class Series(Film):
    def __str__(self):
        return self.name


class Episode(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    name = models.CharField(max_length=2048)
    description = models.CharField(max_length=2048)
    file_path = models.CharField(max_length=2048)

    def __str__(self):
        return self.name
