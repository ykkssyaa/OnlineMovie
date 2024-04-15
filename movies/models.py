from django.db import models
from django.urls import reverse
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
    MOVIE = 'movie'
    SERIES = 'series'
    MEDIA_TYPE_CHOICES = [
        (MOVIE, 'Фильм'),
        (SERIES, 'Сериал'),
    ]

    name = models.CharField(max_length=2048)
    premiere_date = models.DateField(verbose_name='Дата премьеры')
    announcement_date = models.DateField(null=True, blank=True, verbose_name='Дата анонса')
    cover = models.ImageField(upload_to='film_covers/', null=True, blank=True, verbose_name='Обложка')

    video_file = models.FileField(upload_to='film_videos/', null=True, blank=True, verbose_name='Видеофайл')

    annotation = models.CharField(max_length=255, blank=True, verbose_name='Аннотация')
    adult_content = models.BooleanField(verbose_name='Контент для взрослых')
    publication_status = models.BooleanField(default=False, verbose_name='Статус публикации')
    publication_datetime = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время публикации')
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)

    tags = TaggableManager()

    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPE_CHOICES,
        default=MOVIE,
        verbose_name='Тип медиа'
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('movies:detail', args=[str(self.id)])


class Episode(models.Model):
    series = models.ForeignKey(Film, on_delete=models.CASCADE)
    name = models.CharField(max_length=2048)
    number = models.IntegerField() # Номер в сезоне
    season = models.IntegerField() # Сезон
    description = models.CharField(max_length=2048)
    video_file = models.FileField(upload_to='episode_videos/', null=True, blank=True, verbose_name='Видеофайл')

    def __str__(self):
        return self.name
