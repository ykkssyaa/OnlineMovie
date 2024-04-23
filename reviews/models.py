from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Review(models.Model):
    movie = models.ForeignKey('movies.Film', on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    text = models.TextField(max_length=2048)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + ": " + self.movie.name


class Mark(models.Model):
    movie = models.ForeignKey('movies.Film', on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return self.user.username + ": " + self.movie.name + " " + self.value

