# Generated by Django 5.0.4 on 2024-04-23 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_episode_number_episode_season'),
        ('users', '0002_customuser_adult_content_permission_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bookmarks',
            field=models.ManyToManyField(related_name='bookmarks', to='movies.film'),
        ),
    ]