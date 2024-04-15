from django.db import models


class Review(models.Model):
    movie = models.ForeignKey('movies.Film', on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    text = models.TextField(max_length=2048)
    created = models.DateTimeField(auto_now=True)


class Mark(models.Model):
    movie = models.ForeignKey('movies.Film', on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    Value = models.ValueRange(1, 5)

